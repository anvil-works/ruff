//! Structural outlines for the browser API; Python semantics remain in ty.
use crate::positions::Positions;
use ruff_python_ast::visitor::{Visitor, walk_stmt};
use ruff_python_ast::{Expr, Identifier, PySourceType, Stmt};
use ruff_python_parser::parse_unchecked_source;
use ruff_text_size::{Ranged, TextRange};
use serde_json::{Value, json};
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn symbols(source: &str) -> String {
    let parsed = parse_unchecked_source(source, PySourceType::Python);
    let mut outline = Outline {
        positions: Positions::new(source),
        scope: Vec::new(),
        in_class: false,
        assignments: true,
        items: Vec::new(),
    };
    outline.visit_body(&parsed.syntax().body);
    json!(outline.items).to_string()
}

struct Outline<'a> {
    positions: Positions<'a>,
    scope: Vec<String>,
    in_class: bool,
    assignments: bool,
    items: Vec<Value>,
}

impl Outline<'_> {
    fn add(&mut self, name: &str, range: TextRange, kind: u8) {
        if name.is_empty() {
            return;
        }
        let mut item = json!({ "name": name, "kind": kind,
            "range": { "start": self.positions.at(range.start()), "end": self.positions.at(range.end()) } });
        if !self.scope.is_empty() {
            item["containerName"] = json!(self.scope.join("."));
        }
        self.items.push(item);
    }

    fn binding(&mut self, target: &Expr) {
        match target {
            Expr::Name(name) => self.add(name.id.as_str(), name.range(), 13),
            Expr::Tuple(tuple) => {
                for target in &tuple.elts {
                    self.binding(target);
                }
            }
            Expr::List(list) => {
                for target in &list.elts {
                    self.binding(target);
                }
            }
            _ => {}
        }
    }

    fn body(&mut self, name: &Identifier, body: &[Stmt], in_class: bool) {
        let previous = (self.in_class, self.assignments);
        self.scope.push(name.to_string());
        self.in_class = in_class;
        self.assignments = in_class;
        self.visit_body(body);
        (self.in_class, self.assignments) = previous;
        self.scope.pop();
    }
}

impl<'ast> Visitor<'ast> for Outline<'_> {
    fn visit_stmt(&mut self, stmt: &'ast Stmt) {
        match stmt {
            Stmt::ClassDef(class) => {
                self.add(class.name.as_str(), class.name.range(), 5);
                self.body(&class.name, &class.body, true);
            }
            Stmt::FunctionDef(function) => {
                self.add(
                    function.name.as_str(),
                    function.name.range(),
                    if self.in_class { 6 } else { 12 },
                );
                self.body(&function.name, &function.body, false);
            }
            Stmt::Assign(assign) if self.assignments => {
                for target in &assign.targets {
                    self.binding(target);
                }
            }
            Stmt::AnnAssign(assign) if self.assignments => self.binding(&assign.target),
            _ => walk_stmt(self, stmt),
        }
    }
}
