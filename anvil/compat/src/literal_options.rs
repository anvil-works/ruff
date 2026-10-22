//! Read literal suggestions from the declaration resolved by ty, before broad
//! string alternatives erase the suggested values during type simplification.
use std::collections::{BTreeMap, BTreeSet};

#[cfg(feature = "browser")]
use ruff_python_ast::PySourceType;
#[cfg(feature = "browser")]
use ruff_python_ast::visitor::{Visitor, walk_stmt};
use ruff_python_ast::{Expr, ModModule, Stmt};
#[cfg(feature = "browser")]
use ruff_python_parser::parse_unchecked_source;
#[cfg(feature = "browser")]
use ruff_text_size::Ranged;
#[cfg(feature = "browser")]
use wasm_bindgen::prelude::*;

#[cfg(feature = "browser")]
use crate::positions::Positions;

#[cfg(feature = "browser")]
#[wasm_bindgen(js_name = literalOptions)]
pub fn literal_options(source: &str, line: u32, parameter: Option<String>) -> String {
    let parsed = parse_unchecked_source(source, PySourceType::Stub);
    let mut options = LiteralOptions {
        positions: Positions::new(source),
        line,
        literals: LiteralTypes::new(parsed.syntax()),
        names: BTreeSet::new(),
        parameter,
    };
    options.visit_body(&parsed.syntax().body);
    serde_json::json!(options.names).to_string()
}

#[cfg(feature = "browser")]
struct LiteralOptions<'a> {
    positions: Positions<'a>,
    line: u32,
    literals: LiteralTypes<'a>,
    names: BTreeSet<String>,
    parameter: Option<String>,
}

pub(crate) struct LiteralTypes<'a> {
    aliases: BTreeMap<&'a str, &'a Expr>,
}

impl<'a> LiteralTypes<'a> {
    pub(crate) fn new(module: &'a ModModule) -> Self {
        let aliases = module
            .body
            .iter()
            .filter_map(|statement| {
                let Stmt::Assign(assignment) = statement else {
                    return None;
                };
                let [Expr::Name(name)] = assignment.targets.as_slice() else {
                    return None;
                };
                Some((name.id.as_str(), assignment.value.as_ref()))
            })
            .collect();
        Self { aliases }
    }

    pub(crate) fn names(&self, expression: &Expr) -> BTreeSet<String> {
        let mut names = BTreeSet::new();
        self.collect(expression, &mut names, &mut BTreeSet::new());
        names
    }

    fn collect(
        &self,
        expression: &Expr,
        names: &mut BTreeSet<String>,
        seen: &mut BTreeSet<String>,
    ) {
        match expression {
            Expr::Name(name) if seen.insert(name.id.to_string()) => {
                if let Some(alias) = self.aliases.get(name.id.as_str()) {
                    self.collect(alias, names, seen);
                }
            }
            Expr::BinOp(union) => {
                self.collect(&union.left, names, seen);
                self.collect(&union.right, names, seen);
            }
            Expr::Subscript(literal) if matches!(literal.value.as_ref(), Expr::Name(name) if name.id == "Literal") => {
                match literal.slice.as_ref() {
                    Expr::StringLiteral(value) => {
                        names.insert(value.value.to_string());
                    }
                    Expr::Tuple(tuple) => {
                        for value in &tuple.elts {
                            if let Expr::StringLiteral(value) = value {
                                names.insert(value.value.to_string());
                            }
                        }
                    }
                    _ => {}
                }
            }
            _ => {}
        }
    }
}

#[cfg(feature = "browser")]
impl<'ast> Visitor<'ast> for LiteralOptions<'_> {
    fn visit_stmt(&mut self, statement: &'ast Stmt) {
        if let Stmt::FunctionDef(function) = statement {
            if self.positions.at(function.name.start())["line"] == self.line {
                if self.parameter.is_none() {
                    if let Some(annotation) = &function.returns {
                        self.names.extend(self.literals.names(annotation));
                    }
                    return;
                }
                for parameter in function.parameters.iter_non_variadic_params() {
                    if Some(parameter.name().as_str()) == self.parameter.as_deref()
                        && let Some(annotation) = parameter.annotation()
                    {
                        self.names.extend(self.literals.names(annotation));
                    }
                }
            }
        } else {
            walk_stmt(self, statement);
        }
    }
}
