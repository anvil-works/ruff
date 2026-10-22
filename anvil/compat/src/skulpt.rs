//! Client-runtime import policy, shared by native validation and the IDE.
use ruff_python_stdlib::sys::is_known_standard_library;

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
