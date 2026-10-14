//! Bounded validation proof: native preparation and in-process ty, outside the engine fork.
mod callables;
mod checks;
mod dependencies;
mod dom;
mod environments;
mod forms;
mod handles;
mod imports;
mod models;
mod policy;
mod services;
mod suppressions;
mod system;
mod tables;

use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::Instant;

use anyhow::{Context, Result, bail, ensure};
use clap::Parser;
use ruff_db::diagnostic::{Diagnostic, Severity, UnifiedFile};
use ruff_db::source::{line_index, source_text};
use ruff_db::system::{MemoryFileSystem, SystemPath, SystemPathBuf};
use ruff_python_ast::PythonVersion;
use ruff_ranged_value::ValueSource;
use ruff_source_file::PositionEncoding;
use serde_json::{Value, json};
use ty_module_resolver::{ModuleName, TypeshedVersions};
use ty_project::metadata::options::Options;
use ty_project::{Db, ProjectDatabase, ProjectMetadata};
use walkdir::WalkDir;

#[derive(Parser)]
struct Args {
    #[arg(long)]
    version: bool,
    #[arg(long)]
    outputjson: bool,
    #[arg(long, default_value = "warning", value_parser = ["error", "warning"])]
    level: String,
    #[arg(long)]
    project: Option<PathBuf>,
    files: Vec<PathBuf>,
}

struct Source {
    path: PathBuf,
    relative: PathBuf,
    text: String,
}

fn identifier(value: &str) -> bool {
    let mut chars = value.chars();
    chars
        .next()
        .is_some_and(|c| c == '_' || c.is_ascii_alphabetic())
        && chars.all(|c| c == '_' || c.is_ascii_alphanumeric())
}

fn yaml(path: &Path) -> Result<Value> {
    serde_yaml::from_str(&fs::read_to_string(path)?)
        .with_context(|| format!("parsing {}", path.display()))
}

fn populated(value: &Value) -> bool {
    match value {
        Value::Null => false,
        Value::Array(items) => !items.is_empty(),
        Value::Object(items) => !items.is_empty(),
        Value::Bool(value) => *value,
        _ => true,
    }
}

fn sources(root: &Path) -> Result<Vec<Source>> {
    let mut sources = Vec::new();
    if !root.exists() {
        return Ok(sources);
    }
    for entry in WalkDir::new(root).into_iter().filter_entry(|entry| {
        !entry.file_name().to_string_lossy().starts_with('.') && entry.file_name() != "__pycache__"
    }) {
        let entry = entry?;
        if entry.file_type().is_file()
            && matches!(
                entry.path().extension().and_then(|s| s.to_str()),
                Some("py" | "pyi")
            )
        {
            sources.push(Source {
                path: entry.path().to_path_buf(),
                relative: entry.path().strip_prefix(root)?.to_path_buf(),
                text: fs::read_to_string(entry.path())?,
            });
        }
    }
    sources.sort_by(|a, b| a.path.cmp(&b.path));
    Ok(sources)
}

fn utf8(path: &Path) -> Result<&str> {
    path.to_str().context("native proof requires UTF-8 paths")
}

fn stdlib_root(path: &Path, versions: &TypeshedVersions, python_version: PythonVersion) -> bool {
    path.components()
        .next()
        .and_then(|component| Path::new(component.as_os_str()).file_stem())
        .and_then(|stem| stem.to_str())
        .and_then(ModuleName::new)
        .and_then(|name| versions.exact(&name))
        .is_some_and(|range| range.contains(python_version))
}

fn mount(fs: &MemoryFileSystem, path: &SystemPath, text: &str) -> Result<()> {
    fs.write_file_all(path, text)?;
    Ok(())
}

fn diagnostic(
    db: &ProjectDatabase,
    item: Diagnostic,
    origins: &HashMap<SystemPathBuf, PathBuf>,
    baseline_rule: Option<&str>,
) -> Result<Value> {
    let severity = match item.severity() {
        Severity::Fatal | Severity::Error => "error",
        Severity::Warning => "warning",
        Severity::Info => "information",
    };
    let mut output = json!({"severity": severity, "message": format!("{}: {}", item.id(), item.concise_message()), "rule": item.id().to_string()});
    if let Some(span) = item.primary_span() {
        let UnifiedFile::Ty(file) = span.file() else {
            bail!("unexpected Ruff diagnostic")
        };
        if let Some(path) = file
            .path(db)
            .as_system_path()
            .and_then(|path| origins.get(path))
        {
            output["file"] = json!(path);
            if let Some(range) = span.range() {
                if let Some(rule) = baseline_rule {
                    output["_baseline_rule"] = json!(rule);
                }
                let text = source_text(db, *file);
                let index = line_index(db, *file);
                let start =
                    index.source_location(range.start(), text.as_str(), PositionEncoding::Utf16);
                let end =
                    index.source_location(range.end(), text.as_str(), PositionEncoding::Utf16);
                output["range"] = json!({
                    "start": {"line": start.line.to_zero_indexed(), "character": start.character_offset.to_zero_indexed()},
                    "end": {"line": end.line.to_zero_indexed(), "character": end.character_offset.to_zero_indexed()}
                });
            }
        }
    }
    Ok(output)
}

fn anvil_typeshed() -> Result<PathBuf> {
    if let Ok(path) = std::env::var("ANVIL_API_STUBS_PATH")
        && !path.trim().is_empty()
    {
        return Ok(PathBuf::from(path.trim()));
    }
    let executable = std::env::current_exe()?;
    let bundle = executable
        .parent()
        .and_then(Path::parent)
        .context("checker executable needs a parent directory")?;
    let bundled = bundle.join("share/anvil-typeshed");
    if bundled.is_dir() {
        return Ok(bundled);
    }
    Ok(PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../api-stubs"))
}

fn validate(app: &Path, files: &[PathBuf]) -> Result<Vec<Value>> {
    let policy = policy::Policy::load(app)?;
    let config = yaml(&app.join("anvil.yaml"))?;
    let package = config["package_name"]
        .as_str()
        .context("anvil.yaml needs package_name")?;
    ensure!(
        identifier(package),
        "package_name must be a Python identifier"
    );
    let stubs = anvil_typeshed()?;
    let api = fs::read_to_string(stubs.join("client/anvil/__init__.pyi"))
        .with_context(|| format!("reading Anvil API stubs from {}", stubs.display()))?;
    let client = sources(&app.join("client_code"))?;
    let server = sources(&app.join("server_code"))?;
    let stdlib_versions: TypeshedVersions = ty_vendored::file_system()
        .read_to_string("stdlib/VERSIONS")?
        .parse()?;
    let project_stubs = sources(&policy.stub_path(app))?;
    let cached = dependencies::resolve(app, &config)?;
    // Physical search paths must retain the same client/server ownership as the
    // projected namespaces, including server modules in cached dependencies.
    let server_roots: Vec<_> = std::iter::once(app)
        .chain(cached.iter().map(|dependency| dependency.root.as_path()))
        .filter_map(|root| root.join("server_code").canonicalize().ok())
        .collect();
    let mut handles = handles::Registry::default();
    let mut output = Vec::new();
    let dependencies = cached
        .iter()
        .map(|dependency| {
            let client = sources(&dependency.root.join("client_code"))?;
            let server = sources(&dependency.root.join("server_code"))?;
            let mut models = models::Registry::default();
            models.collect(&client, &server, &dependency.package);
            let forms = forms::designers(
                forms::ClientCode {
                    root: &dependency.root.join("client_code"),
                    sources: &client,
                    package: &dependency.package,
                },
                &api,
                &models,
                &cached,
                &mut handles,
                &mut output,
            )?;
            Ok((dependency.package.clone(), client, server, forms))
        })
        .collect::<Result<Vec<_>>>()?;
    let mut models = models::Registry::default();
    models.collect(&client, &server, package);
    let forms = forms::designers(
        forms::ClientCode {
            root: &app.join("client_code"),
            sources: &client,
            package,
        },
        &api,
        &models,
        &cached,
        &mut handles,
        &mut output,
    )?;
    // Preparation diagnostics belong to the same selected Python sources as
    // semantic checks; unrelated app/dependency forms must not fail a file target.
    output.retain(|item| {
        let path = Path::new(item["file"].as_str().unwrap());
        client.iter().any(|source| source.path == path)
            && policy.selected(path, !files.is_empty())
            && (files.is_empty() || files.iter().any(|file| file == path))
    });
    let mut callables = callables::Registry::default();
    // Server registration must be available even when only a client file is checked.
    for (environment, selected) in [("server", &server), ("client", &client)] {
        let selected: Vec<_> = selected
            .iter()
            .filter(|source| {
                source.path.extension().is_some_and(|ext| ext == "py")
                    && policy.selected(&source.path, !files.is_empty())
                    && (files.is_empty() || files.contains(&source.path))
            })
            .collect();
        if selected.is_empty() && (environment == "client" || client.is_empty()) {
            continue;
        }
        let python_version = if environment == "server" {
            policy.server_python_version(&config)?
        } else {
            PythonVersion::PY310
        };
        let root = std::path::absolute(format!("/anvil/{environment}"))?;
        let root = SystemPathBuf::from(utf8(&root)?);
        let system = system::ValidationSystem::new(root.clone());
        let code = root.join(package);
        let fs = system.memory_file_system().clone();
        fs.create_directory_all(&code)?;
        let mut origins = HashMap::new();
        for source in client.iter().chain(if environment == "server" {
            server.iter()
        } else {
            [].iter()
        }) {
            let path = code.join(utf8(&source.relative)?);
            mount(&fs, &path, &source.text)?;
            // Anvil's Pyright resolver permits package-local absolute fallback
            // before reporting its runtime restriction. ty's existing fallback
            // includes package directories carrying project metadata.
            mount(&fs, &path.parent().unwrap().join("ty.toml"), "")?;
            origins.insert(path, source.path.clone());
        }
        if !fs.is_file(code.join("__init__.py")) {
            mount(&fs, &code.join("__init__.py"), "")?;
        }
        for (relative, stub) in &forms {
            mount(&fs, &code.join(utf8(relative)?), stub)?;
        }
        // Pyright prefers stdlib stubs to app modules for absolute imports.
        // Keep the qualified namespace intact for relative imports and source
        // checks, and expose other bare imports through a separate search root.
        let bare = root.join("bare-imports");
        fs.create_directory_all(&bare)?;
        for source in client
            .iter()
            .chain(if environment == "server" {
                server.iter()
            } else {
                [].iter()
            })
            .filter(|source| !stdlib_root(&source.relative, &stdlib_versions, python_version))
        {
            let path = bare.join(utf8(&source.relative.with_extension("pyi"))?);
            // Re-export the canonical definitions: copying source here creates
            // distinct nominal types for bare and relative imports.
            mount(
                &fs,
                &path,
                &imports::alias(package, &source.relative, &source.text),
            )?;
        }
        for (relative, stub) in &forms {
            if !stdlib_root(relative, &stdlib_versions, python_version) {
                mount(
                    &fs,
                    &bare.join(utf8(relative)?),
                    &imports::alias(package, relative, stub),
                )?;
            }
        }
        // Pyright resolves checkout-directory imports before reporting the runtime
        // restriction. Preserve their types so an illegal spelling adds no false
        // missing-import error and does not hide errors in its use.
        let checkout = root.join("client_code");
        fs.create_directory_all(&checkout)?;
        for source in &client {
            let path = checkout.join(utf8(&source.relative)?);
            mount(&fs, &path, &source.text)?;
            origins.insert(path, source.path.clone());
        }
        for (relative, stub) in &forms {
            mount(&fs, &checkout.join(utf8(relative)?), stub)?;
        }
        for (package, client, server, forms) in &dependencies {
            let code = root.join(package);
            fs.create_directory_all(&code)?;
            for source in client.iter().chain(if environment == "server" {
                server.iter()
            } else {
                [].iter()
            }) {
                let path = code.join(utf8(&source.relative)?);
                mount(&fs, &path, &source.text)?;
                origins.insert(path, source.path.clone());
            }
            if !fs.is_file(code.join("__init__.py")) {
                mount(&fs, &code.join("__init__.py"), "")?;
            }
            for (relative, stub) in forms {
                mount(&fs, &code.join(utf8(relative)?), stub)?;
            }
        }
        for entry in WalkDir::new(stubs.join(environment)) {
            let entry = entry?;
            if entry.file_type().is_file() {
                let relative = entry.path().strip_prefix(stubs.join(environment))?;
                let mut text = fs::read_to_string(entry.path())?;
                if relative == Path::new("anvil/tables/__init__.pyi")
                    && let Some(stub) =
                        tables::stub(&config["db_schema"], &text, &models, environment)?
                {
                    text = stub;
                }
                if relative == Path::new("anvil/users/__init__.pyi")
                    && let Some(stub) = services::users(&config, &text, &models, environment)?
                {
                    text = stub;
                }
                if relative == Path::new("anvil/google/drive.pyi")
                    && let Some(stub) = services::drive(&config, &text)?
                {
                    text = stub;
                }
                mount(&fs, &root.join("stubs").join(utf8(relative)?), &text)?;
            }
        }
        let user_stubs = root.join("user-stubs");
        fs.create_directory_all(&user_stubs)?;
        for source in &project_stubs {
            mount(&fs, &user_stubs.join(utf8(&source.relative)?), &source.text)?;
        }
        let mut roots = vec![root.join("stubs"), root.clone()];
        for path in policy.extra_paths() {
            roots.push(SystemPathBuf::from(utf8(&path)?));
        }
        roots.push(bare.clone());
        let python = policy.python_environment()?;
        if python.is_none()
            && let Some(user_site) = environments::user_site(&system)
        {
            roots.push(user_site);
        }
        let options = Options::deserialize_with(
            ValueSource::Cli,
            json!({"environment": {"python-version": python_version.to_string(), "root": roots, "extra-paths": [user_stubs], "python": python},
                "analysis": {"respect-type-ignore-comments": policy.type_ignores()},
                "rules": policy.ty_rules()}),
        )?;
        let mut metadata = ProjectMetadata::new(environment, root.clone());
        metadata.set_override_options(options);
        let mut db = ProjectDatabase::fallible(metadata, system)?;
        let paths = selected
            .iter()
            .map(|source| Ok(code.join(utf8(&source.relative)?)))
            .collect::<Result<Vec<_>>>()?;
        db.project().set_included_paths(&mut db, paths);
        // Match ty's one-shot CLI: immutable inputs and no incremental query eviction.
        ruff_db::disable_lru(&mut db);
        db.freeze_open_files();
        db.freeze();
        if environment == "server" {
            for path in origins.keys().filter(|path| path.extension() == Some("py")) {
                callables.collect(&db, path, &root.join("stubs/anvil/server.pyi"))?;
            }
        }
        if !selected.is_empty() {
            let diagnostics = db.check();
            let rules = policy::contextual_rules(&db, &diagnostics);
            for (item, rule) in diagnostics.into_iter().zip(rules) {
                output.push(diagnostic(&db, item, &origins, rule)?);
            }
        }
        for source in &selected {
            output.extend(callables.check(
                &db,
                &code.join(utf8(&source.relative)?),
                &source.path,
                &root.join("stubs/anvil/server.pyi"),
            )?);
        }
        for source in selected {
            output.extend(handles.check(
                &db,
                &code.join(utf8(&source.relative)?),
                &source.path,
                &root.join("stubs/anvil/__init__.pyi"),
            )?);
            output.extend(checks::imports(
                &db,
                &code.join(utf8(&source.relative)?),
                &source.path,
                &root,
                &server_roots,
                package,
                environment == "client",
            )?);
            suppressions::apply(
                &db,
                &code.join(utf8(&source.relative)?),
                &source.path,
                &mut output,
                policy.type_ignores(),
            )?;
        }
    }
    policy.apply(&mut output);
    Ok(output)
}

fn main() {
    let args = Args::parse();
    if args.version {
        println!(
            "anvil-ty native {}; built from the Anvil Ruff fork",
            env!("CARGO_PKG_VERSION")
        );
        return;
    }
    let started = Instant::now();
    let result = (|| -> Result<Vec<Value>> {
        ensure!(args.outputjson, "native proof requires --outputjson");
        let app = std::path::absolute(args.project.context("native proof requires --project")?)?;
        let files = args
            .files
            .iter()
            .map(std::path::absolute)
            .collect::<std::io::Result<Vec<_>>>()?;
        validate(&app, &files)
    })();
    let mut diagnostics = match result {
        Ok(items) => items,
        Err(error) => {
            eprintln!("{error:#}");
            std::process::exit(2);
        }
    };
    if args.level == "error" {
        diagnostics.retain(|item| item["severity"] == "error");
    }
    let errors = diagnostics
        .iter()
        .filter(|item| item["severity"] == "error")
        .count();
    let warnings = diagnostics
        .iter()
        .filter(|item| item["severity"] == "warning")
        .count();
    println!(
        "{}",
        json!({"version": "anvil-ty-native-proof", "generalDiagnostics": diagnostics,
        "summary": {"errorCount": errors, "warningCount": warnings, "timeInSec": started.elapsed().as_secs_f64()}})
    );
    std::process::exit(i32::from(errors > 0));
}
