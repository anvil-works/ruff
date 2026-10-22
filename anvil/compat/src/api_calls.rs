//! String arguments to calls; ty decides which functions are Anvil APIs.
use crate::positions::Positions;
use ruff_python_ast::visitor::{Visitor, walk_expr, walk_stmt};
use ruff_python_ast::{Expr, PySourceType, Stmt, StringFlags};
use ruff_python_parser::parse_unchecked_source;
use ruff_text_size::{Ranged, TextSize};
use serde_json::{Value, json};
use wasm_bindgen::prelude::*;

#[wasm_bindgen(js_name = apiCalls)]
pub fn api_calls(source: &str) -> String {
    json!(collect(source).calls).to_string()
}

#[wasm_bindgen(js_name = callFacts)]
pub fn call_facts(source: &str) -> String {
    let facts = collect(source);
    json!({ "imports": facts.imports, "arguments": facts.arguments, "assignments": facts.assignments }).to_string()
}

fn collect(source: &str) -> Calls<'_> {
    let parsed = parse_unchecked_source(source, PySourceType::Python);
    let positions = Positions::new(source);
    let imports = positions.imports(&parsed.syntax().body);
    let mut facts = Calls {
        source,
        positions,
        imports,
        calls: Vec::new(),
        arguments: Vec::new(),
        assignments: Vec::new(),
    };
    facts.visit_body(&parsed.syntax().body);
    facts
}

struct Calls<'a> {
    source: &'a str,
    positions: Positions<'a>,
    imports: Value,
    calls: Vec<Value>,
    arguments: Vec<Value>,
    assignments: Vec<Value>,
}

impl Calls<'_> {
    fn reference_range(&self, expression: &Expr) -> Option<Value> {
        let range = match expression {
            Expr::Name(name) => name.range(),
            Expr::Attribute(attribute) => attribute.attr.range(),
            _ => return None,
        };
        Some(
            json!({ "start": self.positions.at(range.start()), "end": self.positions.at(range.end()) }),
        )
    }

    fn literal(&self, expression: &Expr) -> Option<Value> {
        let Expr::StringLiteral(string) = expression else {
            return None;
        };
        let literal = string.value.as_slice().first()?;
        let last = string.value.as_slice().last()?;
        Some(json!({ "value": string.value.to_str(),
            "range": { "start": self.positions.at(literal.content_range().start()), "end": self.positions.at(last.content_range().end()) },
            "literalRange": { "start": self.positions.at(string.start()), "end": self.positions.at(string.end()) },
            "quote": literal.flags.quote_style().as_char(),
            "raw": literal.flags.prefix().is_raw() || string.value.as_slice().len() > 1 }))
    }
}

impl<'ast> Visitor<'ast> for Calls<'_> {
    fn visit_stmt(&mut self, statement: &'ast Stmt) {
        if let Stmt::Assign(assignment) = statement {
            for target in &assignment.targets {
                if let Expr::Attribute(attribute) = target {
                    self.assignments.push(json!({ "position": self.positions.at(attribute.attr.start()),
                        "range": { "start": self.positions.at(assignment.value.start()), "end": self.positions.at(assignment.value.end()) },
                        "literal": self.literal(&assignment.value) }));
                }
            }
        }
        walk_stmt(self, statement);
    }
    fn visit_expr(&mut self, expression: &'ast Expr) {
        if let Expr::Call(call) = expression {
            let target = match call.func.as_ref() {
                Expr::Attribute(attribute) => attribute.attr.start(),
                expression => expression.start(),
            };
            let start = call.arguments.l_paren_range().end();
            let mut end = call.arguments.end();
            if self.source[..usize::from(end)].ends_with(')') {
                end -= TextSize::of(')');
            }
            let values: Vec<_> = call
                .arguments
                .args
                .iter()
                .enumerate()
                .map(|(index, value)| json!({ "index": index, "start": self.positions.at(value.start()), "end": self.positions.at(value.end()), "isIdentifier": matches!(value, Expr::Name(_)), "referenceRange": self.reference_range(value), "literal": self.literal(value) }))
                .chain(call.arguments.keywords.iter().map(|keyword| json!({ "argumentStart": self.positions.at(keyword.start()), "keyword": keyword.arg.as_ref().map(|name| name.as_str()), "start": self.positions.at(keyword.value.start()), "end": self.positions.at(keyword.value.end()), "isIdentifier": false, "referenceRange": keyword.arg.as_ref().and_then(|_| self.reference_range(&keyword.value)), "literal": self.literal(&keyword.value) })))
                .collect();
            let keywords: Vec<_> = call
                .arguments
                .keywords
                .iter()
                .filter_map(|keyword| keyword.arg.as_ref().map(|name| name.as_str()))
                .collect();
            self.arguments.push(json!({
                "position": self.positions.at(target),
                "callee": { "start": self.positions.at(call.func.start()), "end": self.positions.at(call.func.end()) },
                "range": { "start": self.positions.at(start), "end": self.positions.at(end) },
                "values": values, "keywords": keywords,
            }));
            let argument = call.arguments.args.first().or_else(|| {
                call.arguments
                    .keywords
                    .iter()
                    .find(|keyword| {
                        keyword.arg.as_ref().is_some_and(|name| {
                            matches!(
                                name.as_str(),
                                "component_name" | "form" | "fn_or_name" | "name"
                            )
                        })
                    })
                    .map(|keyword| &keyword.value)
            });
            if let Some(Expr::StringLiteral(string)) = argument
                && let Some(literal) = string.value.as_slice().first()
                && let Some(last) = string.value.as_slice().last()
            {
                let contents = literal.content_range();
                self.calls.push(json!({
                    "value": string.value.to_str(),
                    "position": self.positions.at(target),
                    "range": { "start": self.positions.at(contents.start()), "end": self.positions.at(last.content_range().end()) },
                    "literalRange": { "start": self.positions.at(string.start()), "end": self.positions.at(string.end()) },
                    "quote": literal.flags.quote_style().as_char(), "raw": literal.flags.prefix().is_raw() || string.value.as_slice().len() > 1,
                }));
            } else if call.arguments.is_empty() {
                self.calls.push(json!({
                    "position": self.positions.at(target), "empty": true,
                    "range": { "start": self.positions.at(start), "end": self.positions.at(end) },
                }));
            }
        }
        walk_expr(self, expression);
    }
}
