//! Explicit diagnostic configuration shared by the two validation backends.
use std::collections::{BTreeMap, HashMap, HashSet};
use std::fs;
use std::path::{Path, PathBuf};

use anyhow::{Context, Result, ensure};
use globset::{GlobBuilder, GlobSet, GlobSetBuilder};
use ruff_db::diagnostic::{Diagnostic, UnifiedFile};
use ruff_db::files::File;
use ruff_db::parsed::parsed_module;
use ruff_db::system::SystemPath;
use ruff_python_ast::{
    Expr, PythonVersion, Stmt,
    visitor::{Visitor, walk_expr, walk_stmt},
};
use ruff_text_size::{Ranged, TextRange, TextSize};
use serde_json::{Map, Value};
use ty_project::ProjectDatabase;
use ty_python_semantic::types::Type;
use ty_python_semantic::{Db, HasType, SemanticModel};

// The current Pyright config reader exposes only this Anvil diagnostic in
// getDiagLevelDiagnosticRules(). Handle checks deliberately extend the CLI
// contract and expose their own severity settings here.
const RULES: &[(&str, &str)] = &[
    (
        "reportAnvilFalseCallableDecorator",
        "reportAnvilFalseCallableDecorator",
    ),
    ("reportAnvilUnknownComponent", "reportAnvilUnknownComponent"),
    ("reportAnvilInvalidEvent", "reportAnvilInvalidEvent"),
    ("invalid-assignment", "reportAssignmentType"),
    ("invalid-argument-type", "reportArgumentType"),
    ("invalid-parameter-default", "reportArgumentType"),
    ("invalid-return-type", "reportReturnType"),
    ("unresolved-import", "reportMissingImports"),
    ("unresolved-attribute", "reportAttributeAccessIssue"),
    ("missing-argument", "reportCallIssue"),
    ("too-many-positional-arguments", "reportCallIssue"),
    ("unknown-argument", "reportCallIssue"),
    ("call-non-callable", "reportCallIssue"),
    ("not-subscriptable", "reportIndexIssue"),
    ("not-iterable", "reportGeneralTypeIssues"),
    (
        "invalid-method-override",
        "reportIncompatibleMethodOverride",
    ),
    ("unresolved-reference", "reportUndefinedVariable"),
    (
        "unused-type-ignore-comment",
        "reportUnnecessaryTypeIgnoreComment",
    ),
];

// These ty lints cover independently configurable Pyright rules.
const CONTEXTUAL_RULES: &[(&str, &[&str])] = &[
    (
        "invalid-assignment",
        &["reportAssignmentType", "reportAttributeAccessIssue"],
    ),
    (
        "call-non-callable",
        &["reportCallIssue", "reportAbstractUsage"],
    ),
];

pub(crate) fn baseline_rule(rule: &str) -> &str {
    RULES
        .iter()
        .find(|(native, _)| *native == rule)
        .map_or(rule, |(_, baseline)| baseline)
}

pub(crate) fn diagnostic_rule(item: &Value) -> &str {
    item["_baseline_rule"]
        .as_str()
        .unwrap_or_else(|| baseline_rule(item["rule"].as_str().unwrap_or("")))
}

/// Walk each affected file once, indexing reported diagnostic starts so a
/// statement or call examines only spans that it could contain.
pub(crate) fn contextual_rules(
    db: &ProjectDatabase,
    diagnostics: &[Diagnostic],
) -> Vec<Option<&'static str>> {
    struct ContextDiagnostic {
        index: usize,
        rule: &'static str,
        range: TextRange,
    }
    let mut files: HashMap<File, BTreeMap<TextSize, Vec<ContextDiagnostic>>> = HashMap::new();
    for (index, diagnostic) in diagnostics.iter().enumerate() {
        let id = diagnostic.id().to_string();
        let Some((rule, _)) = CONTEXTUAL_RULES.iter().find(|(rule, _)| *rule == id) else {
            continue;
        };
        if let Some(span) = diagnostic.primary_span()
            && let UnifiedFile::Ty(file) = span.file()
            && let Some(range) = span.range()
        {
            files
                .entry(*file)
                .or_default()
                .entry(range.start())
                .or_default()
                .push(ContextDiagnostic { index, rule, range });
        }
    }
    struct RuleContext<'db, 'output> {
        diagnostics: BTreeMap<TextSize, Vec<ContextDiagnostic>>,
        baselines: &'output mut [Option<&'static str>],
        expression_ranges: &'output mut [Option<TextRange>],
        model: SemanticModel<'db>,
    }
    impl<'ast> Visitor<'ast> for RuleContext<'_, '_> {
        fn visit_stmt(&mut self, stmt: &'ast Stmt) {
            let binding = match stmt {
                Stmt::Assign(assign) if assign.targets.len() == 1 => {
                    Some((&assign.targets[0], Some(assign.value.as_ref())))
                }
                Stmt::AnnAssign(assign) => Some((assign.target.as_ref(), assign.value.as_deref())),
                Stmt::AugAssign(assign) => {
                    Some((assign.target.as_ref(), Some(assign.value.as_ref())))
                }
                _ => None,
            };
            if let Some((Expr::Attribute(target), value)) = binding {
                for diagnostic in self
                    .diagnostics
                    .range(stmt.start()..=stmt.end())
                    .flat_map(|(_, diagnostics)| diagnostics)
                {
                    // Descriptor writes may point at the value instead of the target.
                    if diagnostic.rule == "invalid-assignment"
                        && (target.range().contains_range(diagnostic.range)
                            || value.is_some_and(|value| {
                                value.range().contains_range(diagnostic.range)
                            }))
                    {
                        self.baselines[diagnostic.index] = Some("reportAttributeAccessIssue");
                    }
                }
            }
            walk_stmt(self, stmt);
        }
        fn visit_expr(&mut self, expr: &'ast Expr) {
            if let Expr::Call(call) = expr {
                let mut abstract_call = None;
                for diagnostic in self
                    .diagnostics
                    .range(expr.start()..=expr.end())
                    .flat_map(|(_, diagnostics)| diagnostics)
                {
                    if diagnostic.rule == "call-non-callable"
                        && expr.range().contains_range(diagnostic.range)
                        && self.expression_ranges[diagnostic.index]
                            .is_none_or(|previous| expr.range().len() <= previous.len())
                    {
                        // Prefer the smallest call: an outer call can contain an error
                        // in an argument. Infer its function only when needed.
                        let is_abstract = *abstract_call.get_or_insert_with(|| {
                            matches!(
                                call.func.inferred_type(&self.model),
                                Some(Type::ClassLiteral(_))
                            )
                        });
                        self.expression_ranges[diagnostic.index] = Some(expr.range());
                        self.baselines[diagnostic.index] =
                            is_abstract.then_some("reportAbstractUsage");
                    }
                }
            }
            walk_expr(self, expr);
        }
    }
    let mut baselines = vec![None; diagnostics.len()];
    let mut expression_ranges = vec![None; diagnostics.len()];
    for (file, diagnostics) in files {
        let parsed = parsed_module(db, db.program_file(file).python_file(db)).load(db);
        let mut context = RuleContext {
            diagnostics,
            baselines: &mut baselines,
            expression_ranges: &mut expression_ranges,
            model: SemanticModel::new(db, db.program_file(file)),
        };
        context.visit_body(parsed.suite());
    }
    baselines
}

pub struct Policy {
    config: Value,
    ignore: GlobSet,
    exclude: GlobSet,
    include: GlobSet,
}

impl Policy {
    pub fn load(app: &Path) -> Result<Self> {
        let mut path = app.join("pyrightconfig.json");
        if !path.is_file() {
            path = find_above(app, "pyproject.toml").unwrap_or_else(|| app.join("pyproject.toml"));
        }
        let mut visited = HashSet::new();
        let mut chain = Vec::new();
        while path.exists() && visited.insert(fs::canonicalize(&path)?) {
            let Some(config) = read_config(&path)? else {
                // An unrelated pyproject does not mask an ancestor config.
                // Only primary discovery falls back; an empty extends file ends
                // inheritance, as in the baseline service.
                if chain.is_empty()
                    && let Some(parent) = path.parent().and_then(Path::parent)
                    && let Some(next) = find_above(parent, "pyrightconfig.json")
                        .or_else(|| find_above(parent, "pyproject.toml"))
                {
                    path = next;
                    continue;
                }
                break;
            };
            let base = config["extends"]
                .as_str()
                .map(|base| path.parent().unwrap().join(base));
            chain.push((config, path.parent().unwrap().to_owned()));
            let Some(base) = base else { break };
            path = base;
        }
        // Base files are applied before their descendants. Repeated paths stop
        // the chain, matching the baseline's handling of circular inheritance.
        let mut merged = Map::new();
        let mut ignore = None;
        let mut exclude = None;
        let mut include = None;
        for (mut config, directory) in chain.into_iter().rev() {
            for key in ["stubPath", "venvPath"] {
                if let Some(path) = config.get(key) {
                    let path = path
                        .as_str()
                        .with_context(|| format!("{key} must be a string"))?;
                    config[key] = serde_json::json!(directory.join(path));
                }
            }
            if let Some(paths) = config.get("extraPaths") {
                let paths = paths.as_array().context("extraPaths must be an array")?;
                config["extraPaths"] = Value::Array(
                    paths
                        .iter()
                        .map(|path| {
                            let path = path
                                .as_str()
                                .context("extraPaths entries must be strings")?;
                            Ok(serde_json::json!(directory.join(path)))
                        })
                        .collect::<Result<Vec<_>>>()?,
                );
            }
            if let Some(patterns) = config.get("ignore") {
                ignore = Some((directory.clone(), patterns.clone()));
            }
            if let Some(patterns) = config.get("exclude") {
                exclude = Some((directory.clone(), patterns.clone()));
            }
            if let Some(patterns) = config.get("include") {
                include = Some((directory, patterns.clone()));
            }
            if let Value::Object(config) = config {
                merged.extend(config);
            }
        }
        let config = Value::Object(merged);
        for rule in RULES.iter().map(|(_, rule)| *rule).chain(
            CONTEXTUAL_RULES
                .iter()
                .flat_map(|(_, rules)| rules.iter().copied()),
        ) {
            if let Some(level) = config.get(rule) {
                ensure!(
                    level.is_boolean()
                        || matches!(
                            level.as_str(),
                            Some("none" | "information" | "warning" | "error")
                        ),
                    "invalid diagnostic level for {rule}: {level}"
                );
            }
        }
        Ok(Self {
            config,
            ignore: file_specs(ignore)?,
            exclude: file_specs(exclude)?,
            include: file_specs(include)?,
        })
    }

    pub fn apply(&self, diagnostics: &mut Vec<Value>) {
        diagnostics.retain_mut(|item| {
            if item["file"]
                .as_str()
                .is_some_and(|path| self.ignore.is_match(path))
            {
                return false;
            }
            if self.off()
                && matches!(
                    item["rule"].as_str(),
                    Some("reportAnvilUnknownCallable" | "reportAnvilUnknownBackgroundTask")
                )
            {
                return false;
            }
            let Some((_, rule)) = RULES
                .iter()
                .find(|(native, _)| item["rule"].as_str() == Some(*native))
            else {
                return true;
            };
            let rule = item
                .as_object_mut()
                .unwrap()
                .remove("_baseline_rule")
                .and_then(|value| value.as_str().map(str::to_owned))
                .unwrap_or_else(|| (*rule).to_owned());
            let level = match self.config.get(&rule) {
                Some(Value::Bool(true)) => "error",
                Some(Value::Bool(false)) => "none",
                Some(level) => level.as_str().unwrap(), // Validated at load time.
                // Pyright's standard/default mode does not report unused type
                // ignores. Honor an explicit override rather than ty's default.
                None if rule == "reportUnnecessaryTypeIgnoreComment" || self.off() => "none",
                None => return true,
            };
            if level == "none" {
                return false;
            }
            item["severity"] = Value::String(level.to_owned());
            true
        });
    }

    pub fn stub_path(&self, app: &Path) -> PathBuf {
        self.config["stubPath"]
            .as_str()
            .map_or_else(|| app.join("typings"), PathBuf::from)
    }

    pub fn extra_paths(&self) -> Vec<PathBuf> {
        self.config["extraPaths"]
            .as_array()
            .into_iter()
            .flatten()
            .filter_map(Value::as_str)
            .map(PathBuf::from)
            .collect()
    }

    pub fn python_environment(&self) -> Result<Option<PathBuf>> {
        let Some(venv) = self.config.get("venv") else {
            return Ok(None);
        };
        let venv = venv.as_str().context("venv must be a string")?;
        let root = self.config["venvPath"]
            .as_str()
            .context("venv requires venvPath")?;
        Ok(Some(Path::new(root).join(venv)))
    }

    pub fn server_python_version(&self, app: &Value) -> Result<PythonVersion> {
        // Private deployments can redefine image IDs. An explicit version also
        // lets their existing Pyright configuration describe custom images.
        if let Some(value) = self.config.get("pythonVersion") {
            let version: PythonVersion = value
                .as_str()
                .context("pythonVersion must be a string")?
                .parse()
                .context("invalid pythonVersion")?;
            ensure!(
                PythonVersion::iter().any(|supported| supported == version),
                "unsupported pythonVersion: {version}"
            );
            return Ok(version);
        }
        let base = &app["runtime_options"]["server_spec"]["base"];
        Ok(match base.as_str() {
            // Public image IDs from deployments/anvil.works/conf.clj.
            Some("python312") => PythonVersion::PY312,
            Some("python313") => PythonVersion::PY313,
            Some("python314") => PythonVersion::PY314,
            Some(
                "python310-minimal"
                | "python310-standard"
                | "python310-datascience"
                | "python310-machine-learning",
            ) => PythonVersion::PY310,
            Some("python37-legacy" | "python37-google-new-legacy") => PythonVersion::PY37,
            Some(base) => anyhow::bail!(
                "cannot determine Python version for server image {base:?}; set pythonVersion in pyrightconfig.json or pyproject.toml"
            ),
            // Preserve the migration baseline for apps without image metadata.
            // This is an approximation for legacy runtimes, not their exact version.
            None if base.is_null() => PythonVersion::PY310,
            None => anyhow::bail!("runtime_options.server_spec.base must be a string"),
        })
    }

    pub fn type_ignores(&self) -> bool {
        self.config["enableTypeIgnoreComments"]
            .as_bool()
            .unwrap_or(true)
    }

    pub fn selected(&self, path: &Path, explicit: bool) -> bool {
        !self.exclude.is_match(path)
            && (explicit || self.include.is_empty() || self.include.is_match(path))
    }

    fn off(&self) -> bool {
        self.config["typeCheckingMode"] == "off"
    }

    pub fn ty_rules(&self) -> Value {
        let mut rules = Map::new();
        if self.off() {
            rules.insert("all".to_owned(), Value::String("ignore".to_owned()));
        }
        for (native, baseline) in RULES.iter().filter(|(native, _)| {
            !native.starts_with("reportAnvil")
                && !CONTEXTUAL_RULES
                    .iter()
                    .any(|(contextual, _)| native == contextual)
        }) {
            if let Some(level) = self.config.get(*baseline) {
                let level = match level {
                    Value::Bool(true) => "error",
                    Value::Bool(false) => "ignore",
                    Value::String(level) if level == "none" => "ignore",
                    Value::String(level) if level == "error" => "error",
                    _ => "warn", // Information is filtered by the CLI after policy.apply.
                };
                rules.insert((*native).to_owned(), Value::String(level.to_owned()));
            }
        }
        // Keep enough diagnostics for each setting in a shared ty lint, then
        // distinguish their contexts before applying policy and suppressions.
        for (native, baseline_rules) in CONTEXTUAL_RULES {
            if self.off()
                || baseline_rules
                    .iter()
                    .any(|rule| self.config.get(*rule).is_some())
            {
                let levels: Vec<_> = baseline_rules
                    .iter()
                    .map(|rule| match self.config.get(*rule) {
                        Some(Value::Bool(true)) => "error",
                        Some(Value::Bool(false)) => "none",
                        Some(value) => value.as_str().unwrap(),
                        None if self.off() => "none",
                        None => "error",
                    })
                    .collect();
                let level = if levels.contains(&"error") {
                    "error"
                } else if levels.iter().any(|level| *level != "none") {
                    "warn"
                } else {
                    "ignore"
                };
                rules.insert((*native).to_owned(), Value::String(level.to_owned()));
            }
        }
        Value::Object(rules)
    }
}

fn find_above(directory: &Path, name: &str) -> Option<PathBuf> {
    directory
        .ancestors()
        .map(|dir| dir.join(name))
        .find(|path| path.is_file())
}

fn read_config(path: &Path) -> Result<Option<Value>> {
    let source = fs::read_to_string(path)?;
    if path.extension().is_some_and(|ext| ext == "toml") {
        let config: Value =
            toml::from_str(&source).with_context(|| format!("parsing {}", path.display()))?;
        Ok(["anvil-pyright", "basedpyright", "pyright"]
            .into_iter()
            .find_map(|section| config["tool"].get(section).cloned()))
    } else {
        jsonc_parser::parse_to_serde_value(&source, &Default::default())
            .map(Some)
            .with_context(|| format!("parsing {}", path.display()))
    }
}

fn file_specs(specification: Option<(PathBuf, Value)>) -> Result<GlobSet> {
    let mut builder = GlobSetBuilder::new();
    if let Some((directory, patterns)) = specification {
        for pattern in patterns
            .as_array()
            .into_iter()
            .flatten()
            .filter_map(Value::as_str)
        {
            let absolute = SystemPath::absolute(pattern, crate::utf8(&directory)?);
            for pattern in [absolute.to_string(), format!("{absolute}/**")] {
                builder.add(GlobBuilder::new(&pattern).literal_separator(true).build()?);
            }
        }
    }
    Ok(builder.build()?)
}
