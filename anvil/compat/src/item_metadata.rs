//! Syntax facts for IDE metadata. The worker resolves decorator identities through ty.
use std::collections::BTreeMap;

use crate::positions::Positions;
use ruff_python_ast::visitor::{Visitor, walk_stmt};
use ruff_python_ast::{Expr, PySourceType, Stmt};
use ruff_python_parser::parse_unchecked_source;
use ruff_text_size::Ranged;
use serde_json::{Value, json};
use wasm_bindgen::prelude::*;

#[wasm_bindgen(js_name = itemFacts)]
pub fn item_facts(source: &str) -> String {
    let parsed = parse_unchecked_source(source, PySourceType::Python);
    let mut facts = Facts {
        positions: Positions::new(source),
        owner: None,
        functions: Vec::new(),
        classes: Vec::new(),
    };
    facts.visit_body(&parsed.syntax().body);
    json!({ "functions": facts.functions, "classes": facts.classes }).to_string()
}

struct Facts<'a> {
    positions: Positions<'a>,
    owner: Option<u32>,
    functions: Vec<Value>,
    classes: Vec<Value>,
}

impl Facts<'_> {
    fn target(&self, expression: &Expr) -> Value {
        let offset = match expression {
            Expr::Attribute(attribute) => attribute.attr.start(),
            _ => expression.start(),
        };
        self.positions.at(offset)
    }

    fn decorator(&self, expression: &Expr) -> Value {
        let (target, call) = match expression {
            Expr::Call(call) => (call.func.as_ref(), Some(call)),
            expression => (expression, None),
        };
        let mut args = Vec::new();
        let mut keywords = BTreeMap::new();
        if let Some(call) = call {
            for argument in &call.arguments.args {
                args.push(string(argument));
            }
            for argument in &call.arguments.keywords {
                if let Some(name) = &argument.arg {
                    keywords.insert(name.as_str(), string(&argument.value));
                }
            }
        }
        let none_args: Vec<_> = call
            .into_iter()
            .flat_map(|call| call.arguments.args.iter().enumerate())
            .filter_map(|(index, value)| matches!(value, Expr::NoneLiteral(_)).then_some(index))
            .collect();
        let none_keywords: Vec<_> = call
            .into_iter()
            .flat_map(|call| &call.arguments.keywords)
            .filter(|keyword| matches!(keyword.value, Expr::NoneLiteral(_)))
            .filter_map(|keyword| keyword.arg.as_ref().map(|name| name.as_str()))
            .collect();
        json!({ "noneArgs": none_args, "noneKeywords": none_keywords, "position": self.target(target), "call": call.is_some(), "args": args, "keywords": keywords })
    }
}

fn string(expression: &Expr) -> Option<&str> {
    match expression {
        Expr::StringLiteral(literal) => Some(literal.value.to_str()),
        _ => None,
    }
}

impl<'ast> Visitor<'ast> for Facts<'_> {
    fn visit_stmt(&mut self, statement: &'ast Stmt) {
        match statement {
            Stmt::ClassDef(class) => {
                let id = u32::from(class.start());
                self.classes.push(json!({
                    "id": id, "name": class.name.as_str(), "owner": self.owner,
                    "range": { "start": self.positions.at(class.name.start()), "end": self.positions.at(class.name.end()) },
                    "bases": class.arguments.as_ref().map(|arguments| arguments.args.iter().map(|base| self.target(base)).collect::<Vec<_>>()).unwrap_or_default(),
                    "bodyStart": class.body.first().map(|statement| self.positions.at(statement.start())),
                    "bodyEnd": class.body.last().map(|statement| self.positions.at(statement.end())),
                }));
                let previous = self.owner.replace(id);
                self.visit_body(&class.body);
                self.owner = previous;
            }
            Stmt::FunctionDef(function) => {
                let decorators: Vec<_> = function
                    .decorator_list
                    .iter()
                    .map(|decorator| self.decorator(&decorator.expression))
                    .collect();
                let parameters: Vec<_> = function.parameters.iter_non_variadic_params().map(|parameter| {
                    json!({ "name": parameter.name().as_str(), "annotated": parameter.annotation().is_some(),
                        "end": self.positions.at(parameter.name().end()) })
                }).collect();
                self.functions.push(json!({ "name": function.name.as_str(), "isAsync": function.is_async, "owner": self.owner, "decorators": decorators,
                    "parameters": parameters,
                    "kwarg": function.parameters.kwarg.as_ref().map(|parameter| json!({
                        "name": parameter.name.as_str(), "annotated": parameter.annotation.is_some(),
                        "end": self.positions.at(parameter.name.end()),
                    })),
                    "range": { "start": self.positions.at(function.name.start()), "end": self.positions.at(function.name.end()) } }));
                // Nested functions do not register endpoints or Form methods.
            }
            _ => walk_stmt(self, statement),
        }
    }
}
