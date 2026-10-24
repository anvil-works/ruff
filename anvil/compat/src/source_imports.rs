//! Import positions for the browser's inferred-declaration input tracking.
//! Ty resolves the modules; this visitor only supplies Python syntax.
use crate::positions::Positions;
use ruff_python_ast::visitor::{Visitor, walk_stmt};
use ruff_python_ast::{Expr, Identifier, PySourceType, PythonVersion, Stmt};
use ruff_python_parser::parse_unchecked_source;
use ruff_python_stdlib::sys::is_known_standard_library;
use ruff_text_size::{Ranged, TextSize};
use serde_json::{Value, json};
use wasm_bindgen::prelude::*;

#[wasm_bindgen(js_name = sourceImports)]
pub fn source_imports(source: &str) -> String {
    let parsed = parse_unchecked_source(source, PySourceType::Python);
    let mut imports = Imports {
        positions: Positions::new(source),
        items: Vec::new(),
    };
    imports.visit_body(&parsed.syntax().body);
    json!(imports.items).to_string()
}

struct Imports<'a> {
    positions: Positions<'a>,
    items: Vec<Value>,
}

fn stdlib_module(name: &str) -> bool {
    let root = name.split('.').next().unwrap_or_default();
    // Removed stdlib modules must remain import errors on newer runtimes,
    // rather than looking like third-party libraries without declarations.
    PythonVersion::iter().any(|version| is_known_standard_library(version.minor, root))
}

impl Imports<'_> {
    fn names(&self, name: &Identifier) -> Vec<Value> {
        let mut offset = name.start();
        name.split('.')
            .filter(|part| *part != "*")
            .map(|part| {
                let position = self.positions.at(offset);
                offset += TextSize::of(part) + TextSize::of(".");
                position
            })
            .collect()
    }
}

impl<'ast> Visitor<'ast> for Imports<'_> {
    fn visit_stmt(&mut self, statement: &'ast Stmt) {
        match statement {
            Stmt::Import(import) => {
                for alias in &import.names {
                    self.items.push(json!({ "module": alias.name.as_str(),
                        "relative": false, "stdlib": stdlib_module(&alias.name),
                        "positions": self.names(&alias.name) }));
                }
            }
            Stmt::ImportFrom(import) => {
                let bindings: Vec<_> = import
                    .names
                    .iter()
                    .map(|alias| {
                        json!({
                            "name": alias.name.as_str(),
                            "alias": alias.asname.as_ref().unwrap_or(&alias.name).as_str(),
                        })
                    })
                    .collect();
                let positions: Vec<_> = import
                    .module
                    .iter()
                    .flat_map(|module| self.names(module))
                    .chain(
                        import
                            .names
                            .iter()
                            .flat_map(|alias| self.names(&alias.name)),
                    )
                    .collect();
                self.items.push(
                    json!({ "module": import.module.as_ref().map(|name| name.as_str()),
                    "stdlib": import.module.as_ref().is_some_and(|name| stdlib_module(name)),
                    "relative": import.level > 0, "positions": positions, "bindings": bindings }),
                );
            }
            _ => walk_stmt(self, statement),
        }
    }

    fn visit_expr(&mut self, _expression: &'ast Expr) {}
}
