//! Assignment syntax for RepeatingPanel item inference. Ty resolves identities.
use ruff_python_ast::visitor::{Visitor, walk_expr, walk_stmt};
use ruff_python_ast::{Expr, PySourceType, Stmt};
use ruff_python_parser::parse_unchecked_source;
use ruff_text_size::{Ranged, TextSize};
use serde_json::{Value, json};
use wasm_bindgen::prelude::*;

use crate::positions::Positions;

#[wasm_bindgen(js_name = itemAssignments)]
pub fn item_assignments(source: &str) -> String {
    let parsed = parse_unchecked_source(source, PySourceType::Python);
    let mut assignments = Assignments {
        positions: Positions::new(source),
        values: Vec::new(),
        statement: TextSize::new(0),
    };
    assignments.visit_body(&parsed.syntax().body);
    json!(assignments.values).to_string()
}

struct Assignments<'a> {
    positions: Positions<'a>,
    values: Vec<Value>,
    statement: TextSize,
}

impl<'ast> Visitor<'ast> for Assignments<'_> {
    fn visit_stmt(&mut self, statement: &'ast Stmt) {
        let previous = self.statement;
        self.statement = statement.start();
        if let Stmt::Assign(assignment) = statement {
            for target in &assignment.targets {
                let Expr::Attribute(items) = target else {
                    continue;
                };
                if items.attr.as_str() != "items" {
                    continue;
                }
                let Expr::Attribute(component) = items.value.as_ref() else {
                    continue;
                };
                let Expr::Name(receiver) = component.value.as_ref() else {
                    continue;
                };
                if receiver.id.as_str() != "self" {
                    continue;
                }
                self.values.push(json!({ "target": {
                    "component": component.attr.as_str(), "position": self.positions.at(component.attr.start())
                }, "value": {
                    "statement": self.positions.at(statement.start()),
                    "start": self.positions.at(assignment.value.start()),
                    "end": self.positions.at(assignment.value.end())
                } }));
            }
        }
        walk_stmt(self, statement);
        self.statement = previous;
    }

    fn visit_expr(&mut self, expression: &'ast Expr) {
        if matches!(expression, Expr::Lambda(_)) {
            return;
        }
        if let Expr::Call(call) = expression {
            for keyword in &call.arguments.keywords {
                if !keyword.arg.as_ref().is_some_and(|name| name == "item") {
                    continue;
                }
                let target = match call.func.as_ref() {
                    Expr::Attribute(attribute) => attribute.attr.start(),
                    expression => expression.start(),
                };
                self.values.push(
                    json!({ "target": { "constructorPosition": self.positions.at(target) },
                    "value": { "statement": self.positions.at(self.statement),
                        "start": self.positions.at(keyword.value.start()),
                        "end": self.positions.at(keyword.value.end()) } }),
                );
            }
        }
        walk_expr(self, expression);
    }
}

/// Literal dictionary shapes need standard TypedDict declarations to survive
/// inference across a Form boundary. Supply syntax only; ty infers every value.
#[wasm_bindgen(js_name = dictionaryProbes)]
pub fn dictionary_probes(source: &str) -> String {
    let parsed = parse_unchecked_source(source, PySourceType::Python);
    let mut dictionaries = Dictionaries {
        positions: Positions::new(source),
        statement: TextSize::new(0),
        values: Vec::new(),
    };
    dictionaries.visit_body(&parsed.syntax().body);
    json!({ "imports": dictionaries.positions.imports(&parsed.syntax().body), "dictionaries": dictionaries.values })
        .to_string()
}

struct Dictionaries<'a> {
    positions: Positions<'a>,
    statement: TextSize,
    values: Vec<Value>,
}

impl<'ast> Visitor<'ast> for Dictionaries<'_> {
    fn visit_stmt(&mut self, statement: &'ast Stmt) {
        let previous = self.statement;
        self.statement = statement.start();
        walk_stmt(self, statement);
        self.statement = previous;
    }

    fn visit_expr(&mut self, expression: &'ast Expr) {
        // A lambda owns its walrus bindings; exports in the enclosing statement
        // cannot expose those values. Leave it to ordinary ty inference.
        if matches!(expression, Expr::Lambda(_)) {
            return;
        }
        if let Expr::Dict(dictionary) = expression {
            let fields: Option<Vec<_>> = dictionary
                .items
                .iter()
                .map(|item| {
                    let Expr::StringLiteral(key) = item.key.as_ref()? else {
                        return None;
                    };
                    Some(json!({ "key": key.value.to_string(),
                    "start": self.positions.at(item.value.start()),
                    "end": self.positions.at(item.value.end()) }))
                })
                .collect();
            if let Some(fields) = fields.filter(|fields| !fields.is_empty()) {
                let keys: std::collections::BTreeSet<_> = fields
                    .iter()
                    .map(|field| field["key"].clone().to_string())
                    .collect();
                if keys.len() == fields.len() {
                    self.values
                        .push(json!({ "start": self.positions.at(dictionary.start()),
                        "end": self.positions.at(dictionary.end()),
                        "statement": self.positions.at(self.statement), "fields": fields }));
                }
            }
        }
        walk_expr(self, expression);
    }
}
