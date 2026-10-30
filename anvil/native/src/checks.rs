//! Anvil runtime checks, separate from ty's generic checker.
use std::path::{Path, PathBuf};

use anyhow::Result;
use ruff_db::Db;
use ruff_db::files::{File, system_path_to_file};
use ruff_db::parsed::parsed_module;
use ruff_db::source::{line_index, source_text};
use ruff_db::system::SystemPath;
use ruff_python_ast::Stmt;
use ruff_python_ast::visitor::{Visitor, walk_stmt};
use ruff_source_file::PositionEncoding;
use ruff_text_size::{Ranged, TextRange};
use serde_json::{Value, json};
use ty_project::ProjectDatabase;
use ty_python_semantic::types::TypeDefinition;
use ty_python_semantic::{Db as SemanticDb, HasType, SemanticModel};

pub(crate) fn issue(
    db: &dyn Db,
    file: File,
    origin: &Path,
    range: TextRange,
    rule: &str,
    severity: &str,
    message: String,
) -> Value {
    let text = source_text(db, file);
    let index = line_index(db, file);
    let start = index.source_location(range.start(), text.as_str(), PositionEncoding::Utf16);
    let end = index.source_location(range.end(), text.as_str(), PositionEncoding::Utf16);
    json!({"file": origin, "rule": rule, "severity": severity, "message": message,
    "range": {
        "start": {"line": start.line.to_zero_indexed(), "character": start.character_offset.to_zero_indexed()},
        "end": {"line": end.line.to_zero_indexed(), "character": end.character_offset.to_zero_indexed()}
    }})
}

struct Imports<'db> {
    db: &'db dyn Db,
    file: File,
    origin: &'db Path,
    model: SemanticModel<'db>,
    root: &'db SystemPath,
    server_roots: &'db [PathBuf],
    package: &'db str,
    client: bool,
    client_runtime: &'db anvil_ty_compat::skulpt::ClientRuntime,
    issues: Vec<Value>,
}

impl Imports<'_> {
    fn check(&mut self, name: &str, range: TextRange) {
        let resolved = self
            .model
            .resolve_module(Some(name), 0)
            .and_then(|module| module.file(self.model.db()));
        if self.client
            && resolved
                .and_then(|file| file.path(self.db).as_system_path())
                .and_then(|path| std::fs::canonicalize(path.as_std_path()).ok())
                .is_some_and(|path| self.server_roots.iter().any(|root| path.starts_with(root)))
        {
            self.issues.push(issue(
                self.db, self.file, self.origin, range,
                "reportAnvilImportRestriction", "error",
                format!("Client code cannot import server module '{name}'. Use anvil.server.call to call a server function."),
            ));
            return;
        }
        if self.client && !self.client_runtime.module_supported(name) {
            self.issues.push(issue(
                self.db, self.file, self.origin, range,
                "reportAnvilUnsupportedSkulptImport", "error",
                format!("Module '{name}' is not available in Skulpt. Anvil client code runs in the browser using Skulpt, which only supports a subset of Python's standard library. Consider moving this code to server_code/ or using a supported alternative."),
            ));
        }
        if name == "client_code" || name.starts_with("client_code.") {
            self.issues.push(issue(self.db, self.file, self.origin, range,
                "reportAnvilImportRestriction", "error",
                "The \"client_code\" directory is not an importable Anvil package. Use a relative import instead.".to_owned()));
        } else if self.client
            && name != self.package
            && !name.starts_with(&format!("{}.", self.package))
            && resolved
                .and_then(|file| file.path(self.db).as_system_path())
                .is_some_and(|path| {
                    path.starts_with(self.root.join("bare-imports"))
                        || path.starts_with(self.root.join(self.package))
                })
        {
            self.issues.push(issue(self.db, self.file, self.origin, range,
                "reportAnvilImportRestriction", "error",
                format!("Client modules must use relative imports for modules in the same app. Absolute import \"{name}\" would fail at runtime.")));
        }
    }
}

impl<'ast> Visitor<'ast> for Imports<'_> {
    fn visit_stmt(&mut self, stmt: &'ast Stmt) {
        match stmt {
            Stmt::Import(import) => {
                for alias in &import.names {
                    self.check(alias.name.as_str(), alias.name.range());
                }
            }
            Stmt::ImportFrom(import) if import.level == 0 => {
                if let Some(module) = &import.module {
                    self.check(module.as_str(), module.range());
                    // Resolve imported children as modules before applying module
                    // restrictions; ordinary exports (e.g. namedtuple) are not modules.
                    let namespace = self
                        .model
                        .resolve_module(Some(module.as_str()), 0)
                        .is_some_and(|module| module.file(self.model.db()).is_none());
                    for alias in &import.names {
                        let child = format!("{module}.{}", alias.name);
                        if namespace
                            || self.client_runtime.module_supported(module.as_str())
                                && self.model.resolve_module(Some(&child), 0).is_some()
                        {
                            self.check(&child, alias.name.range());
                        }
                    }
                }
            }
            _ => {}
        }
        walk_stmt(self, stmt);
    }
}

pub fn imports(
    db: &ProjectDatabase,
    path: &SystemPath,
    origin: &Path,
    root: &SystemPath,
    server_roots: &[PathBuf],
    package: &str,
    client: bool,
    client_runtime: &anvil_ty_compat::skulpt::ClientRuntime,
) -> Result<Vec<Value>> {
    let file = system_path_to_file(db, path)?;
    let parsed = parsed_module(db, db.program_file(file).python_file(db)).load(db);
    let mut visitor = Imports {
        db,
        file,
        origin,
        model: SemanticModel::new(db, db.program_file(file)),
        root,
        server_roots,
        package,
        client,
        client_runtime,
        issues: Vec::new(),
    };
    for stmt in &parsed.syntax().body {
        visitor.visit_stmt(stmt);
    }
    if client {
        visitor.issues.extend(
            anvil_ty_compat::skulpt::syntax_diagnostics(source_text(db, file).as_str())
                .into_iter()
                .map(|diagnostic| {
                    issue(
                        db,
                        file,
                        origin,
                        diagnostic.range,
                        "reportAnvilUnsupportedSkulptSyntax",
                        "warning",
                        diagnostic.message,
                    )
                }),
        );
    }
    Ok(visitor.issues)
}

pub fn runtime(
    db: &ProjectDatabase,
    path: &SystemPath,
    origin: &Path,
    api_root: &SystemPath,
    context: &anvil_ty_compat::diagnostics::Context,
) -> Result<Vec<Value>> {
    let file = system_path_to_file(db, path)?;
    let model = SemanticModel::new(db, db.program_file(file));
    let parsed = parsed_module(db, model.python_file()).load(db);
    let diagnostics =
        anvil_ty_compat::diagnostics::check(&parsed.syntax().body, context, |expression| {
            let TypeDefinition::Function(definition) = expression
                .inferred_type(&model)?
                .definition(db, &model.program_environment())?
            else {
                return None;
            };
            let name = definition.name(db)?;
            let module = match name.as_str() {
                "portable_class" | "callable" | "background_task" => "server.pyi",
                "open_form" | "handle" => "__init__.pyi",
                _ => return None,
            };
            (definition.file(db) == system_path_to_file(db, &api_root.join(module)).ok()?)
                .then_some(name)
        });
    Ok(diagnostics
        .into_iter()
        .map(|diagnostic| {
            issue(
                db,
                file,
                origin,
                diagnostic.range,
                diagnostic.rule,
                "warning",
                diagnostic.message,
            )
        })
        .collect())
}
