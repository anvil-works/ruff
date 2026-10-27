//! Runtime callable names, resolved through ty so aliases and shadowing retain meaning.
use std::collections::{HashMap, HashSet};
use std::path::Path;

use anyhow::Result;
use ruff_db::files::{File, system_path_to_file};
use ruff_db::parsed::parsed_module;
use ruff_db::system::SystemPath;
use ruff_python_ast::visitor::{Visitor, walk_expr, walk_stmt};
use ruff_python_ast::{Expr, Stmt};
use ruff_text_size::Ranged;
use serde_json::Value;
use ty_project::ProjectDatabase;
use ty_python_semantic::types::TypeDefinition;
use ty_python_semantic::{Db, HasType, SemanticModel};

#[derive(Default)]
pub struct Registry {
    names: HashSet<String>,
    tasks: HashSet<String>,
    callable_counts: HashMap<String, usize>,
    task_counts: HashMap<String, usize>,
}

impl Registry {
    pub fn duplicates(&self) -> (HashSet<String>, HashSet<String>) {
        let repeated = |counts: &HashMap<String, usize>| {
            counts
                .iter()
                .filter(|(_, count)| **count > 1)
                .map(|(name, _)| name.clone())
                .collect()
        };
        (repeated(&self.callable_counts), repeated(&self.task_counts))
    }

    pub fn collect(
        &mut self,
        db: &ProjectDatabase,
        path: &SystemPath,
        api: &SystemPath,
        server_module: bool,
    ) -> Result<()> {
        let file = system_path_to_file(db, path)?;
        let model = SemanticModel::new(db, db.program_file(file));
        let parsed = parsed_module(db, model.python_file()).load(db);
        let mut visitor = Registrations {
            model,
            api: system_path_to_file(db, api)?,
            registry: self,
            module_registration: server_module,
        };
        for stmt in &parsed.syntax().body {
            visitor.visit_stmt(stmt);
        }
        Ok(())
    }

    pub fn check(
        &self,
        db: &ProjectDatabase,
        path: &SystemPath,
        origin: &Path,
        api: &SystemPath,
    ) -> Result<Vec<Value>> {
        let file = system_path_to_file(db, path)?;
        let model = SemanticModel::new(db, db.program_file(file));
        let parsed = parsed_module(db, model.python_file()).load(db);
        let mut visitor = Calls {
            model,
            api: system_path_to_file(db, api)?,
            origin,
            registry: self,
            issues: Vec::new(),
        };
        for stmt in &parsed.syntax().body {
            visitor.visit_stmt(stmt);
        }
        Ok(visitor.issues)
    }
}

struct Registrations<'db, 'r> {
    model: SemanticModel<'db>,
    api: File,
    registry: &'r mut Registry,
    module_registration: bool,
}

impl<'ast> Visitor<'ast> for Registrations<'_, '_> {
    fn visit_stmt(&mut self, stmt: &'ast Stmt) {
        if let Stmt::FunctionDef(function) = stmt {
            for decorator in &function.decorator_list {
                let expr = match &decorator.expression {
                    Expr::Call(call) => call.func.as_ref(),
                    expression => expression,
                };
                let registration_name = anvil_ty_compat::diagnostics::registration_name(
                    &decorator.expression,
                    function.name.as_str(),
                );
                // Keep the existing gradual fallback for known-name discovery;
                // only statically named registrations can establish duplicates.
                let name = registration_name.unwrap_or(function.name.as_str());
                let Some(ty) = expr.inferred_type(&self.model) else {
                    continue;
                };
                let Some(TypeDefinition::Function(definition)) =
                    ty.definition(self.model.db(), &self.model.program_environment())
                else {
                    continue;
                };
                if definition.file(self.model.db()) == self.api {
                    match definition.name(self.model.db()).as_deref() {
                        Some("callable") => {
                            self.registry.names.insert(name.to_owned());
                            if self.module_registration && registration_name.is_some() {
                                *self
                                    .registry
                                    .callable_counts
                                    .entry(name.to_owned())
                                    .or_default() += 1;
                            }
                        }
                        Some("background_task") => {
                            self.registry.tasks.insert(name.to_owned());
                            if self.module_registration && registration_name.is_some() {
                                *self
                                    .registry
                                    .task_counts
                                    .entry(name.to_owned())
                                    .or_default() += 1;
                            }
                        }
                        _ => {}
                    }
                }
            }
        }
        // Preserve existing known-name discovery. Duplicate warnings use the
        // IDE catalogue's ownership: module-level Server Module functions.
        let module_registration = self.module_registration;
        if matches!(stmt, Stmt::FunctionDef(_) | Stmt::ClassDef(_)) {
            self.module_registration = false;
        }
        walk_stmt(self, stmt);
        self.module_registration = module_registration;
    }
}

fn string(expr: &Expr) -> Option<&str> {
    if let Expr::StringLiteral(literal) = expr {
        Some(literal.value.to_str())
    } else {
        None
    }
}

// Mirror serverCallDetection.ts: qualified and server shorthand methods.
// Broader alias recognition at call sites would change the existing validation policy.
fn server_method(expr: &Expr) -> Option<&str> {
    let Expr::Attribute(method) = expr else {
        return None;
    };
    if !matches!(
        method.attr.as_str(),
        "call" | "call_s" | "launch_background_task"
    ) {
        return None;
    }
    let matches = match method.value.as_ref() {
        Expr::Name(name) => name.id == "server",
        Expr::Attribute(server) if server.attr.as_str() == "server" => {
            matches!(server.value.as_ref(), Expr::Name(name) if name.id == "anvil")
        }
        _ => false,
    };
    matches.then(|| method.attr.as_str())
}

struct Calls<'db, 'r> {
    model: SemanticModel<'db>,
    api: File,
    origin: &'r Path,
    registry: &'r Registry,
    issues: Vec<Value>,
}

impl<'ast> Visitor<'ast> for Calls<'_, '_> {
    fn visit_stmt(&mut self, stmt: &'ast Stmt) {
        if let Stmt::FunctionDef(function) = stmt {
            for decorator in &function.decorator_list {
                let expr = match &decorator.expression {
                    Expr::Call(call) => call.func.as_ref(),
                    expr => expr,
                };
                let Some(name) = dotted_name(expr) else {
                    continue;
                };
                let expected = match name.as_str() {
                    "anvil.server.callable" | "server.callable" | "callable" => "callable",
                    "anvil.server.background_task"
                    | "server.background_task"
                    | "background_task" => "background_task",
                    _ => continue,
                };
                let valid = expr
                    .inferred_type(&self.model)
                    .and_then(|ty| {
                        ty.definition(self.model.db(), &self.model.program_environment())
                    })
                    .is_some_and(|definition| {
                        if let TypeDefinition::Function(definition) = definition {
                            definition.file(self.model.db()) == self.api
                                && definition.name(self.model.db()).as_deref() == Some(expected)
                        } else {
                            false
                        }
                    });
                if !valid {
                    let suffix = if expected == "callable" {
                        " This function will not be available via anvil.server.call()."
                    } else {
                        ""
                    };
                    self.issues.push(crate::checks::issue(
                        self.model.db(), self.model.file(), self.origin, decorator.range(),
                        "reportAnvilFalseCallableDecorator", "warning",
                        format!("Decorator '{name}' does not resolve to anvil.server.{expected}.{suffix}"),
                    ));
                }
            }
        }
        walk_stmt(self, stmt);
    }

    fn visit_expr(&mut self, expr: &'ast Expr) {
        if let Expr::Call(call) = expr
            && let Some(method) = server_method(&call.func)
            && let Some(argument) = call.arguments.args.first()
            && let Some(name) = string(argument).filter(|name| !name.is_empty())
        {
            let (registered, rule, kind, decorator) = if method == "launch_background_task" {
                (
                    &self.registry.tasks,
                    "reportAnvilUnknownBackgroundTask",
                    "background task",
                    "background_task",
                )
            } else {
                (
                    &self.registry.names,
                    "reportAnvilUnknownCallable",
                    "server callable",
                    "callable",
                )
            };
            if !registered.contains(name) {
                self.issues.push(crate::checks::issue(
                    self.model.db(), self.model.file(), self.origin, argument.range(), rule, "warning",
                    format!("Unknown {kind} '{name}'. No @anvil.server.{decorator} function with this name was found."),
                ));
            }
        }
        walk_expr(self, expr);
    }
}

fn dotted_name(expr: &Expr) -> Option<String> {
    match expr {
        Expr::Name(name) => Some(name.id.to_string()),
        Expr::Attribute(attribute) => Some(format!(
            "{}.{}",
            dotted_name(&attribute.value)?,
            attribute.attr
        )),
        _ => None,
    }
}
