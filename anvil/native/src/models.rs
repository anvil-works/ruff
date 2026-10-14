//! Syntactic row-model discovery, matching trackAnvilModel without engine hooks.
use std::collections::{BTreeMap, HashSet};

use ruff_python_ast::visitor::{Visitor, walk_stmt};
use ruff_python_ast::{Expr, Stmt};
use ruff_python_parser::parse_module;

use crate::Source;

pub struct Model {
    pub name: String,
    pub module: String,
}

#[derive(Default)]
pub struct Registry {
    client: BTreeMap<String, Model>,
    server: BTreeMap<String, Model>,
}

impl Registry {
    pub fn collect(&mut self, client: &[Source], server: &[Source], package: &str) {
        self.collect_environment(client, "client", package);
        let server_paths: HashSet<_> = server.iter().map(|source| &source.relative).collect();
        self.collect_environment(
            client
                .iter()
                .filter(|source| !server_paths.contains(&source.relative)),
            "server",
            package,
        );
        self.collect_environment(server, "server", package);
    }

    fn collect_environment<'a>(
        &mut self,
        sources: impl IntoIterator<Item = &'a Source>,
        environment: &str,
        package: &str,
    ) {
        let models = if environment == "client" {
            &mut self.client
        } else {
            &mut self.server
        };
        for source in sources
            .into_iter()
            .filter(|source| source.relative.extension().is_some_and(|ext| ext == "py"))
        {
            // Syntax errors are reported by the checker on selected files.
            let Ok(parsed) = parse_module(&source.text) else {
                continue;
            };
            let module = crate::imports::module_name(package, &source.relative);
            let mut visitor = Discovery {
                module: &module,
                models,
            };
            for stmt in &parsed.syntax().body {
                visitor.visit_stmt(stmt);
            }
        }
    }

    pub fn get(&self, table: &str, environment: &str) -> Option<&Model> {
        if environment == "server" {
            self.server.get(table)
        } else {
            self.client.get(table)
        }
    }
}

fn dotted(expr: &Expr) -> Option<String> {
    match expr {
        Expr::Name(name) => Some(name.id.to_string()),
        Expr::Attribute(attr) => Some(format!("{}.{}", dotted(&attr.value)?, attr.attr)),
        _ => None,
    }
}

struct Discovery<'a> {
    module: &'a str,
    models: &'a mut BTreeMap<String, Model>,
}

impl<'ast> Visitor<'ast> for Discovery<'_> {
    fn visit_stmt(&mut self, stmt: &'ast Stmt) {
        if let Stmt::ClassDef(class) = stmt
            && let Some(arguments) = &class.arguments
        {
            for base in &arguments.args {
                let Some(name) = dotted(base) else { continue };
                let name = name.strip_prefix("tables.").unwrap_or(&name);
                if let Some(table) = name
                    .strip_prefix("app_tables.")
                    .and_then(|s| s.strip_suffix(".Row"))
                    && crate::identifier(table)
                {
                    self.models.insert(
                        table.to_owned(),
                        Model {
                            name: class.name.to_string(),
                            module: self.module.to_owned(),
                        },
                    );
                    break;
                }
            }
        }
        walk_stmt(self, stmt);
    }
}
