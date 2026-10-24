//! Row-model discovery and type-check-only attribute bases, without engine hooks.
use std::collections::{BTreeMap, HashSet};

use ruff_python_ast::visitor::{Visitor, walk_expr, walk_stmt};
use ruff_python_ast::{Expr, ExprAttribute, ExprContext, PySourceType, Stmt, StmtClassDef};
use ruff_python_parser::parse_unchecked_source;
use ruff_text_size::{Ranged, TextRange};

use crate::Source;

#[derive(Clone, PartialEq, Eq)]
pub struct Model {
    pub name: String,
    pub module: String,
}

#[derive(Clone, Default, PartialEq, Eq)]
pub struct Registry {
    pub(crate) client: BTreeMap<String, Model>,
    pub(crate) server: BTreeMap<String, Model>,
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
            let parsed = parse_unchecked_source(&source.text, PySourceType::Python);
            let module = crate::imports::module_name(package, &source.relative);
            let bindings = TableImports::names(&parsed.syntax().body);
            let mut visitor = Discovery {
                module: &module,
                models,
                bindings: &bindings,
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

struct RowBase<'a> {
    expression: &'a ExprAttribute,
    table: String,
    attrs: bool,
}

fn row_base<'a>(class: &'a StmtClassDef, bindings: &HashSet<String>) -> Option<RowBase<'a>> {
    let arguments = class.arguments.as_ref()?;
    for base in &arguments.args {
        let Expr::Attribute(expression) = base else {
            continue;
        };
        let Some(name) = dotted(base) else { continue };
        let (name, binding) = name
            .strip_prefix("tables.")
            .map_or((name.as_str(), "app_tables"), |name| (name, "tables"));
        if !bindings.contains(binding) {
            continue;
        }
        if let Some(table) = name
            .strip_prefix("app_tables.")
            .and_then(|s| s.strip_suffix(".Row"))
            && crate::identifier(table)
        {
            return Some(RowBase {
                expression,
                table: table.to_owned(),
                attrs: arguments.keywords.iter().any(|keyword| {
                    keyword.arg.as_ref().is_some_and(|name| name == "attrs")
                        && matches!(&keyword.value, Expr::BooleanLiteral(value) if value.value)
                }),
            });
        }
    }
    None
}

struct Discovery<'a> {
    module: &'a str,
    models: &'a mut BTreeMap<String, Model>,
    bindings: &'a HashSet<String>,
}

impl<'ast> Visitor<'ast> for Discovery<'_> {
    fn visit_stmt(&mut self, stmt: &'ast Stmt) {
        if let Stmt::ClassDef(class) = stmt
            && let Some(base) = row_base(class, self.bindings)
        {
            self.models.insert(
                base.table,
                Model {
                    name: class.name.to_string(),
                    module: self.module.to_owned(),
                },
            );
        }
        if !matches!(stmt, Stmt::ClassDef(_) | Stmt::FunctionDef(_)) {
            walk_stmt(self, stmt);
        }
    }
}

/// Only attrs=True models inherit column attributes. A global Row base would
/// leak one app's flag into dependency models using the same table. The table
/// stub's private `_AR` alias selects the attribute-bearing base for this class.
/// Replacing the ASCII `Row` token with `_AR` preserves every source position;
/// original sources remain unchanged for editing and read-only previews.
pub fn analysis_source(source: &str, schema: &serde_json::Value) -> String {
    let Some(schema) = schema.as_object() else {
        return source.to_owned();
    };
    if schema.is_empty() {
        return source.to_owned();
    }
    let tables: HashSet<_> = schema
        .iter()
        .map(|(name, table)| table["python_name"].as_str().unwrap_or(name).to_owned())
        .collect();
    let parsed = parse_unchecked_source(source, PySourceType::Python);
    let bindings = TableImports::names(&parsed.syntax().body);
    let mut bases = AttributeBases {
        bindings: &bindings,
        tables: &tables,
        ranges: Vec::new(),
    };
    bases.visit_body(&parsed.syntax().body);
    let mut projected = source.to_owned();
    for range in bases.ranges {
        projected.replace_range(std::ops::Range::<usize>::from(range), "_AR");
    }
    projected
}

struct AttributeBases<'a> {
    bindings: &'a HashSet<String>,
    tables: &'a HashSet<String>,
    ranges: Vec<TextRange>,
}

impl<'ast> Visitor<'ast> for AttributeBases<'_> {
    fn visit_stmt(&mut self, stmt: &'ast Stmt) {
        if let Stmt::ClassDef(class) = stmt
            && let Some(base) = row_base(class, self.bindings)
            && base.attrs
            && self.tables.contains(&base.table)
        {
            self.ranges.push(base.expression.attr.range());
        }
        if !matches!(stmt, Stmt::ClassDef(_) | Stmt::FunctionDef(_)) {
            walk_stmt(self, stmt);
        }
    }
}

// Only direct, unshadowed Anvil imports establish these model spellings. Class
// bases execute in their enclosing scope; nested classes/functions have their
// own bindings and are not module-level model registrations.
#[derive(Default)]
struct TableImports(BTreeMap<String, bool>);

impl TableImports {
    fn bind(&mut self, name: &str, anvil: bool) {
        if !matches!(name, "app_tables" | "tables") {
            return;
        }
        self.0
            .entry(name.to_owned())
            .and_modify(|value| *value &= anvil)
            .or_insert(anvil);
    }

    fn names(body: &[Stmt]) -> HashSet<String> {
        let mut imports = Self::default();
        imports.visit_body(body);
        imports
            .0
            .into_iter()
            .filter_map(|(name, anvil)| anvil.then_some(name))
            .collect()
    }
}

impl<'ast> Visitor<'ast> for TableImports {
    fn visit_stmt(&mut self, stmt: &'ast Stmt) {
        match stmt {
            Stmt::ClassDef(class) => self.bind(&class.name, false),
            Stmt::FunctionDef(function) => self.bind(&function.name, false),
            Stmt::Import(import) => {
                for alias in &import.names {
                    let name = alias.asname.as_ref().map_or_else(
                        || alias.name.split('.').next().unwrap_or(""),
                        |name| name.as_str(),
                    );
                    self.bind(
                        name,
                        alias.name.as_str() == "anvil.tables" && name == "tables",
                    );
                }
            }
            Stmt::ImportFrom(import) => {
                for alias in &import.names {
                    let name = alias.asname.as_ref().unwrap_or(&alias.name).as_str();
                    let anvil = import.level == 0
                        && matches!(
                            (
                                import.module.as_ref().map(|name| name.as_str()),
                                alias.name.as_str(),
                                name,
                            ),
                            (Some("anvil.tables"), "app_tables", "app_tables")
                                | (Some("anvil"), "tables", "tables")
                        );
                    self.bind(name, anvil);
                }
            }
            _ => walk_stmt(self, stmt),
        }
    }

    fn visit_expr(&mut self, expression: &'ast Expr) {
        match expression {
            Expr::Name(name) if matches!(name.ctx, ExprContext::Store | ExprContext::Del) => {
                self.bind(&name.id, false)
            }
            Expr::Lambda(_)
            | Expr::ListComp(_)
            | Expr::SetComp(_)
            | Expr::DictComp(_)
            | Expr::Generator(_) => return,
            _ => {}
        }
        walk_expr(self, expression);
    }
}
