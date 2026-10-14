//! Anvil runtime checks, separate from ty's generic checker.
use std::path::{Path, PathBuf};

use anyhow::Result;
use ruff_db::Db;
use ruff_db::files::{File, system_path_to_file};
use ruff_db::parsed::parsed_module;
use ruff_db::source::{line_index, source_text};
use ruff_db::system::SystemPath;
use ruff_python_ast::Stmt;
use ruff_python_ast::visitor::{Visitor, walk_stmt};
use ruff_source_file::PositionEncoding;
use ruff_text_size::{Ranged, TextRange};
use serde_json::{Value, json};
use ty_project::ProjectDatabase;
use ty_python_semantic::{Db as SemanticDb, SemanticModel};

// Ported from anvil-pyright/src/anvil/skulptModules.ts. This is the existing
// runtime policy (known stdlib minus the supported set), not Python's stdlib list.
const UNSUPPORTED_SKULPT: &[&str] = &[
    "os",
    "subprocess",
    "socket",
    "threading",
    "multiprocessing",
    "sqlite3",
    "pathlib",
    "shutil",
    "tempfile",
    "glob",
    "fnmatch",
    "io",
    "struct",
    "codecs",
    "csv",
    "configparser",
    "argparse",
    "logging",
    "unittest",
    "doctest",
    "pdb",
    "profile",
    "timeit",
    "trace",
    "abc",
    "contextlib",
    "decimal",
    "numbers",
    "cmath",
    "statistics",
    "secrets",
    "hashlib",
    "hmac",
    "ssl",
    "http",
    "xmlrpc",
    "ftplib",
    "poplib",
    "imaplib",
    "smtplib",
    "email",
    "html",
    "xml",
    "webbrowser",
    "cgi",
    "wsgiref",
    "asyncio",
    "concurrent",
    "select",
    "selectors",
    "mmap",
    "ctypes",
    "pickle",
    "shelve",
    "marshal",
    "dbm",
    "gzip",
    "bz2",
    "lzma",
    "zipfile",
    "tarfile",
    "zlib",
    "copy",
    "pprint",
    "textwrap",
    "difflib",
    "enum",
    "dataclasses",
    "weakref",
    "inspect",
    "dis",
    "importlib",
    "pkgutil",
    "modulefinder",
    "ast",
    "symtable",
    "token",
    "tokenize",
    "compileall",
    "sysconfig",
    "site",
    "venv",
    "ensurepip",
    "distutils",
    "setuptools",
    "warnings",
    "traceback",
    "atexit",
    "gc",
    "resource",
    "posixpath",
    "ntpath",
    "posix",
    "nt",
    "gettext",
    "locale",
    "base64",
    "binascii",
    "quopri",
    "uu",
    "queue",
    "heapq",
    "bisect",
];

pub(crate) fn issue(
    db: &dyn Db,
    file: File,
    origin: &Path,
    range: TextRange,
    rule: &str,
    severity: &str,
    message: String,
) -> Value {
    let text = source_text(db, file);
    let index = line_index(db, file);
    let start = index.source_location(range.start(), text.as_str(), PositionEncoding::Utf16);
    let end = index.source_location(range.end(), text.as_str(), PositionEncoding::Utf16);
    json!({"file": origin, "rule": rule, "severity": severity, "message": message,
    "range": {
        "start": {"line": start.line.to_zero_indexed(), "character": start.character_offset.to_zero_indexed()},
        "end": {"line": end.line.to_zero_indexed(), "character": end.character_offset.to_zero_indexed()}
    }})
}

struct Imports<'db> {
    db: &'db dyn Db,
    file: File,
    origin: &'db Path,
    model: SemanticModel<'db>,
    root: &'db SystemPath,
    server_roots: &'db [PathBuf],
    package: &'db str,
    client: bool,
    issues: Vec<Value>,
}

impl Imports<'_> {
    fn check(&mut self, name: &str, range: TextRange) {
        let resolved = self
            .model
            .resolve_module(Some(name), 0)
            .and_then(|module| module.file(self.model.db()));
        if self.client
            && resolved
                .and_then(|file| file.path(self.db).as_system_path())
                .and_then(|path| std::fs::canonicalize(path.as_std_path()).ok())
                .is_some_and(|path| self.server_roots.iter().any(|root| path.starts_with(root)))
        {
            self.issues.push(issue(
                self.db, self.file, self.origin, range,
                "reportAnvilImportRestriction", "error",
                format!("Client code cannot import server module '{name}'. Use anvil.server.call to call a server function."),
            ));
            return;
        }
        if self.client && UNSUPPORTED_SKULPT.contains(&name.split('.').next().unwrap()) {
            self.issues.push(issue(
                self.db, self.file, self.origin, range,
                "reportAnvilUnsupportedSkulptImport", "error",
                format!("Module '{name}' is not available in Skulpt. Anvil client code runs in the browser using Skulpt, which only supports a subset of Python's standard library. Consider moving this code to server_code/ or using a supported alternative."),
            ));
        }
        if name == "client_code" || name.starts_with("client_code.") {
            self.issues.push(issue(self.db, self.file, self.origin, range,
                "reportAnvilImportRestriction", "error",
                "The \"client_code\" directory is not an importable Anvil package. Use a relative import instead.".to_owned()));
        } else if self.client
            && name != self.package
            && !name.starts_with(&format!("{}.", self.package))
            && resolved
                .and_then(|file| file.path(self.db).as_system_path())
                .is_some_and(|path| {
                    path.starts_with(self.root.join("bare-imports"))
                        || path.starts_with(self.root.join(self.package))
                })
        {
            self.issues.push(issue(self.db, self.file, self.origin, range,
                "reportAnvilImportRestriction", "error",
                format!("Client modules must use relative imports for modules in the same app. Absolute import \"{name}\" would fail at runtime.")));
        }
    }
}

impl<'ast> Visitor<'ast> for Imports<'_> {
    fn visit_stmt(&mut self, stmt: &'ast Stmt) {
        match stmt {
            Stmt::Import(import) => {
                for alias in &import.names {
                    self.check(alias.name.as_str(), alias.name.range());
                }
            }
            Stmt::ImportFrom(import) if import.level == 0 => {
                if let Some(module) = &import.module {
                    self.check(module.as_str(), module.range());
                    // A namespace package has no source file to establish ownership.
                    // Its imported children do, e.g. `from server_code import Secret`.
                    if self
                        .model
                        .resolve_module(Some(module.as_str()), 0)
                        .is_some_and(|module| module.file(self.model.db()).is_none())
                    {
                        for alias in &import.names {
                            self.check(&format!("{module}.{}", alias.name), alias.name.range());
                        }
                    }
                }
            }
            _ => {}
        }
        walk_stmt(self, stmt);
    }
}

pub fn imports(
    db: &ProjectDatabase,
    path: &SystemPath,
    origin: &Path,
    root: &SystemPath,
    server_roots: &[PathBuf],
    package: &str,
    client: bool,
) -> Result<Vec<Value>> {
    let file = system_path_to_file(db, path)?;
    let parsed = parsed_module(db, db.program_file(file).python_file(db)).load(db);
    let mut visitor = Imports {
        db,
        file,
        origin,
        model: SemanticModel::new(db, db.program_file(file)),
        root,
        server_roots,
        package,
        client,
        issues: Vec::new(),
    };
    for stmt in &parsed.syntax().body {
        visitor.visit_stmt(stmt);
    }
    Ok(visitor.issues)
}
