//! Original Python name ranges for refactoring. Ty resolves their identities.
use crate::positions::Positions;
use ruff_python_ast::visitor::{Visitor, walk_expr, walk_stmt};
use ruff_python_ast::{Alias, Expr, Identifier, PySourceType, Stmt};
use ruff_python_parser::parse_unchecked_source;
use ruff_python_stdlib::identifiers::is_identifier;
use ruff_text_size::{Ranged, TextRange, TextSize};
use serde_json::{Value, json};
use wasm_bindgen::prelude::*;

#[wasm_bindgen(js_name = validRenameName)]
pub fn valid_rename_name(name: &str) -> bool {
    is_identifier(name)
}

#[wasm_bindgen(js_name = parseAnvilData)]
pub fn parse_anvil_data(source: &str, is_html: bool) -> Result<String, JsValue> {
    crate::forms::parse_template(source, is_html)
        .map(|value| value.to_string())
        .map_err(|error| JsValue::from_str(&format!("{error:#}")))
}

#[wasm_bindgen(js_name = renameNames)]
pub fn rename_names(source: &str) -> String {
    let parsed = parse_unchecked_source(source, PySourceType::Python);
    let mut names = Names {
        positions: Positions::new(source),
        items: Vec::new(),
    };
    names.visit_body(&parsed.syntax().body);
    json!(names.items).to_string()
}

struct Names<'a> {
    positions: Positions<'a>,
    items: Vec<Value>,
}

impl Names<'_> {
    fn add(&mut self, name: &str, range: TextRange, imported: bool) {
        self.items
            .push(json!({ "name": name, "imported": imported, "range": {
            "start": self.positions.at(range.start()), "end": self.positions.at(range.end())
        } }));
    }

    fn module(&mut self, name: &Identifier) {
        let mut offset = name.start();
        for part in name.split('.') {
            let end = offset + TextSize::of(part);
            self.add(part, TextRange::new(offset, end), true);
            offset = end + TextSize::of('.');
        }
    }
}

impl<'ast> Visitor<'ast> for Names<'_> {
    fn visit_stmt(&mut self, statement: &'ast Stmt) {
        if let Stmt::ImportFrom(import) = statement
            && let Some(module) = &import.module
        {
            self.module(module);
        }
        walk_stmt(self, statement);
    }

    fn visit_alias(&mut self, alias: &'ast Alias) {
        self.module(&alias.name);
        if let Some(name) = &alias.asname {
            self.items.push(json!({ "name": name.as_str(), "alias": true,
                "importRange": { "start": self.positions.at(alias.name.start()), "end": self.positions.at(alias.name.end()) },
                "range": { "start": self.positions.at(name.start()), "end": self.positions.at(name.end()) } }));
        }
    }

    fn visit_expr(&mut self, expression: &'ast Expr) {
        match expression {
            Expr::Name(name) => self.add(&name.id, name.range(), false),
            Expr::Attribute(attribute) => self.add(&attribute.attr, attribute.attr.range(), false),
            _ => {}
        }
        walk_expr(self, expression);
    }
}
