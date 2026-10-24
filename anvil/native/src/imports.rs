//! Alternate import spellings re-export canonical definitions, preserving nominal types.
use std::collections::BTreeSet;
use std::path::Path;

use ruff_python_ast::visitor::{Visitor, walk_expr, walk_stmt};
use ruff_python_ast::{Alias, Expr, ExprContext, Stmt};
use ruff_python_parser::parse_module;

pub use anvil_ty_compat::imports::module_name;

pub fn alias(package: &str, relative: &Path, source: &str) -> String {
    let module = module_name(package, relative);
    let mut output = format!("from {module} import *\n");
    // Star imports alone omit private names and names excluded by __all__.
    // Explicit re-exports retain the direct-import contract too.
    if let Ok(parsed) = parse_module(source) {
        let mut bindings = Bindings::default();
        bindings.visit_body(&parsed.syntax().body);
        for name in bindings.names {
            output.push_str(&format!("from {module} import {name} as {name}\n"));
        }
    }
    output
}

#[derive(Default)]
struct Bindings {
    names: BTreeSet<String>,
}

impl<'ast> Visitor<'ast> for Bindings {
    fn visit_stmt(&mut self, stmt: &'ast Stmt) {
        match stmt {
            Stmt::FunctionDef(function) => {
                self.names.insert(function.name.to_string());
            }
            Stmt::ClassDef(class) => {
                self.names.insert(class.name.to_string());
            }
            _ => walk_stmt(self, stmt),
        }
    }

    fn visit_expr(&mut self, expr: &'ast Expr) {
        match expr {
            Expr::Name(name) if name.ctx == ExprContext::Store => {
                self.names.insert(name.id.to_string());
            }
            // These introduce nested scopes; their local names are not exports.
            Expr::Lambda(_)
            | Expr::ListComp(_)
            | Expr::SetComp(_)
            | Expr::DictComp(_)
            | Expr::Generator(_) => {}
            _ => walk_expr(self, expr),
        }
    }

    fn visit_alias(&mut self, alias: &'ast Alias) {
        if alias.name.as_str() != "*" {
            let name = alias.asname.as_ref().map_or_else(
                || alias.name.split('.').next().unwrap(),
                |name| name.as_str(),
            );
            self.names.insert(name.to_owned());
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn nested_aliases_use_python_module_names_on_both_platforms() {
        for path in ["cards/Card/__init__.py", r"cards\Card\__init__.py"] {
            assert_eq!(
                alias("App", Path::new(path), "class Card: pass\n"),
                "from App.cards.Card import *\nfrom App.cards.Card import Card as Card\n"
            );
        }
        for path in ["cards/helpers.py", r"cards\helpers.py"] {
            assert_eq!(
                alias("App", Path::new(path), ""),
                "from App.cards.helpers import *\n"
            );
        }
        assert_eq!(
            alias("App", Path::new("__init__.py"), ""),
            "from App import *\n"
        );
    }
}
