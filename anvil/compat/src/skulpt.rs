//! Client-runtime import policy, shared by native validation and the IDE.
use ruff_python_ast::visitor::{Visitor, walk_comprehension, walk_expr, walk_stmt};
use ruff_python_ast::{
    Comprehension, Expr, InterpolatedStringElements, PySourceType, PythonVersion, Stmt,
};
use ruff_python_parser::{ParseOptions, parse_unchecked};
use ruff_python_stdlib::sys::is_known_standard_library;
use ruff_source_file::LineIndex;
use ruff_text_size::{Ranged, TextRange};

#[cfg(feature = "browser")]
use wasm_bindgen::prelude::*;

// Verified against Anvil's bundled skulpt.min.js and skulpt-stdlib.js, using
// read-builtin-files.ts's lazy chunk loader. base64 is preloaded by
// load-modules.ts. Recheck this list when updating that runtime. Unknown roots
// remain available to app/dependency packages; this only restricts stdlib.
const SUPPORTED: &[&str] = &[
    "antigravity",
    "array",
    "base64",
    "bisect",
    "calendar",
    "collections",
    "copy",
    "datetime",
    "fractions",
    "functools",
    "itertools",
    "json",
    "keyword",
    "math",
    "numbers",
    "operator",
    "platform",
    "random",
    "re",
    "signal",
    "string",
    "sys",
    "this",
    "time",
    "token",
    "tokenize",
    "turtle",
    "types",
    "urllib",
    "urllib.request",
    "uuid",
    "webbrowser",
];

#[cfg_attr(feature = "browser", wasm_bindgen(js_name = skulptModuleSupported))]
pub fn module_supported(name: &str) -> bool {
    let top = name.split('.').next().unwrap_or(name);
    !is_known_standard_library(10, top) || SUPPORTED.contains(&name)
}

pub struct SyntaxDiagnostic {
    pub range: TextRange,
    pub message: String,
}

/// Use the parser's version checks for newer Python grammar, then add Skulpt's
/// restrictions that a CPython version target cannot express (notably async).
pub fn syntax_diagnostics(source: &str) -> Vec<SyntaxDiagnostic> {
    let parsed = parse_unchecked(
        source,
        ParseOptions::from(PySourceType::Python).with_target_version(PythonVersion::PY37),
    )
    .try_into_module()
    .unwrap();
    let mut checks = SyntaxChecks {
        diagnostics: Vec::new(),
    };
    for error in parsed.unsupported_syntax_errors() {
        checks.diagnostics.push(SyntaxDiagnostic {
            range: error.range(),
            message: format!("{error}. This syntax is not supported in Anvil client code."),
        });
    }
    checks.visit_body(&parsed.syntax().body);
    let lines = LineIndex::from_source_text(source);
    checks
        .diagnostics
        .sort_by_key(|diagnostic| diagnostic.range.start());
    checks
        .diagnostics
        .dedup_by_key(|diagnostic| lines.line_index(diagnostic.range.start()));
    checks.diagnostics
}

struct SyntaxChecks {
    diagnostics: Vec<SyntaxDiagnostic>,
}

impl SyntaxChecks {
    fn warn(&mut self, range: TextRange, message: &'static str) {
        self.diagnostics.push(SyntaxDiagnostic {
            range,
            message: message.to_owned(),
        });
    }
}

impl<'ast> Visitor<'ast> for SyntaxChecks {
    fn visit_stmt(&mut self, statement: &'ast Stmt) {
        let asynchronous = match statement {
            Stmt::FunctionDef(function) => function.is_async,
            Stmt::For(statement) => statement.is_async,
            Stmt::With(statement) => statement.is_async,
            _ => false,
        };
        if asynchronous {
            let range = match statement {
                Stmt::FunctionDef(function) => function.name.range(),
                _ => statement.range(),
            };
            self.warn(
                range,
                "Async/await syntax is not supported in Anvil client code.",
            );
        }
        walk_stmt(self, statement);
    }

    fn visit_expr(&mut self, expression: &'ast Expr) {
        if matches!(expression, Expr::Await(_)) {
            self.warn(
                expression.range(),
                "Async/await syntax is not supported in Anvil client code.",
            );
        }
        if let Expr::FString(string) = expression {
            for part in string.value.f_strings() {
                if debug_fstring(&part.elements) {
                    self.warn(
                        part.range(),
                        "Debug expressions in f-strings are not supported in Anvil client code.",
                    );
                }
            }
        }
        walk_expr(self, expression);
    }

    fn visit_comprehension(&mut self, comprehension: &'ast Comprehension) {
        if comprehension.is_async {
            self.warn(
                comprehension.range(),
                "Async/await syntax is not supported in Anvil client code.",
            );
        }
        walk_comprehension(self, comprehension);
    }
}

fn debug_fstring(elements: &InterpolatedStringElements) -> bool {
    elements.interpolations().any(|field| {
        field.debug_text.is_some()
            || field
                .format_spec
                .as_ref()
                .is_some_and(|spec| debug_fstring(&spec.elements))
    })
}

#[cfg(feature = "browser")]
#[wasm_bindgen(js_name = clientSyntaxDiagnostics)]
pub fn client_syntax_diagnostics(source: &str) -> String {
    let positions = crate::positions::Positions::new(source);
    serde_json::json!(syntax_diagnostics(source).into_iter().map(|diagnostic| {
        serde_json::json!({ "range": { "start": positions.at(diagnostic.range.start()), "end": positions.at(diagnostic.range.end()) },
            "message": diagnostic.message })
    }).collect::<Vec<_>>()).to_string()
}

#[cfg(feature = "browser")]
#[wasm_bindgen(js_name = clientImportFacts)]
pub fn client_import_facts(source: &str) -> String {
    use crate::positions::Positions;
    use ruff_python_ast::visitor::{Visitor, walk_stmt};
    use ruff_python_ast::{PySourceType, Stmt};
    use ruff_python_parser::parse_unchecked_source;
    use ruff_text_size::Ranged;
    use serde_json::{Value, json};

    struct Imports<'a> {
        positions: Positions<'a>,
        imports: Vec<Value>,
        from_imports: Vec<Value>,
    }
    impl Imports<'_> {
        fn check(&mut self, name: &ruff_python_ast::Identifier) {
            if !module_supported(name.as_str()) {
                self.imports.push(json!({ "name": name.as_str(), "range": {
                    "start": self.positions.at(name.start()), "end": self.positions.at(name.end()),
                }}));
            }
        }
    }
    impl<'ast> Visitor<'ast> for Imports<'_> {
        fn visit_stmt(&mut self, statement: &'ast Stmt) {
            match statement {
                Stmt::Import(import) => {
                    for alias in &import.names {
                        self.check(&alias.name);
                    }
                }
                Stmt::ImportFrom(import) if import.level == 0 => {
                    if let Some(module) = &import.module {
                        self.from_imports.push(json!({ "module": module.as_str(),
                            "moduleEnd": self.positions.at(module.end()),
                            "range": { "start": self.positions.at(import.start()), "end": self.positions.at(import.end()) },
                        }));
                        if module_supported(module.as_str()) {
                            for alias in &import.names {
                                let name = format!("{module}.{}", alias.name);
                                if !module_supported(&name) {
                                    self.imports.push(json!({ "name": name, "resolve": true, "range": {
                                        "start": self.positions.at(alias.name.start()), "end": self.positions.at(alias.name.end()),
                                    }}));
                                }
                            }
                        } else {
                            self.check(module);
                        }
                    }
                }
                _ => walk_stmt(self, statement),
            }
        }
    }
    let parsed = parse_unchecked_source(source, PySourceType::Python);
    let mut imports = Imports {
        positions: Positions::new(source),
        imports: Vec::new(),
        from_imports: Vec::new(),
    };
    imports.visit_body(&parsed.syntax().body);
    json!({ "imports": imports.imports, "fromImports": imports.from_imports }).to_string()
}
