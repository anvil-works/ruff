//! Native form preparation. Generated stubs preserve source apps and use ty normally.
use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};

use anyhow::{Context, Result, ensure};
use serde_json::{Value, json};
use walkdir::WalkDir;

use crate::identifier;

/// A client package's directory, Python modules and public import name.
pub struct ClientCode<'a> {
    pub root: &'a Path,
    pub sources: &'a [crate::Source],
    pub package: &'a str,
}

pub fn designers(
    client: ClientCode<'_>,
    api: &str,
    models: &crate::models::Registry,
    dependencies: &[crate::dependencies::Dependency],
    handles: &mut crate::handles::Registry,
    diagnostics: &mut Vec<Value>,
) -> Result<Vec<(PathBuf, String)>> {
    let ClientCode {
        root,
        sources,
        package,
    } = client;
    let mut output = BTreeMap::<PathBuf, String>::new();
    let component_api = anvil_ty_compat::forms::ComponentApi::parse(api);
    if !root.exists() {
        return Ok(Vec::new());
    }
    for entry in WalkDir::new(root).into_iter().filter_entry(|entry| {
        !entry.file_name().to_string_lossy().starts_with('.') && entry.file_name() != "__pycache__"
    }) {
        let entry = entry?;
        let Some(format @ ("yaml" | "html")) =
            entry.path().extension().and_then(|ext| ext.to_str())
        else {
            continue;
        };
        // Anvil prefers YAML when both template formats exist for a Python file.
        if format == "html" && entry.path().with_extension("yaml").is_file() {
            continue;
        }
        let directory = entry.path().parent().unwrap();
        let name = if matches!(
            entry.file_name().to_str(),
            Some("form_template.yaml" | "form_template.html")
        ) {
            ensure!(
                directory.join("__init__.py").is_file(),
                "native proof requires package forms"
            );
            directory.file_name().unwrap()
        } else if entry.path().with_extension("py").is_file() {
            entry.path().file_stem().unwrap()
        } else {
            continue;
        };
        let name = name.to_str().context("non-UTF8 form name")?;
        ensure!(identifier(name), "invalid form identifier: {name}");
        let source = if matches!(
            entry.file_name().to_str(),
            Some("form_template.yaml" | "form_template.html")
        ) {
            directory.join("__init__.py")
        } else {
            entry.path().with_extension("py")
        };
        let prepared = (|| -> Result<String> {
            let code = sources
                .iter()
                .find(|code| code.path == source)
                .map_or("", |code| code.text.as_str());
            let template = anvil_ty_compat::forms::parse_template(
                &fs::read_to_string(entry.path())?,
                format == "html",
            )?;
            let rendered = anvil_ty_compat::forms::render(
                &template,
                anvil_ty_compat::forms::TemplateContext {
                    root,
                    package,
                    name,
                    api: &component_api,
                    code,
                    models,
                    dependencies,
                    exists: &Path::is_file,
                    inferred_item_type: None,
                },
            )?;
            handles.collect(
                source.clone(),
                root,
                package,
                name,
                &template,
                rendered.components,
            );
            Ok(rendered.stub)
        })();
        let stub = match prepared {
            Ok(stub) => stub,
            Err(error) => {
                diagnostics.push(json!({
                    "file": source,
                    "severity": "error",
                    "rule": "invalid-form-template",
                    "message": format!("Cannot prepare {}: {error:#}", entry.path().display()),
                }));
                // Report the failed preparation once, without missing-designer
                // import/member cascades. The form's own Python is still checked.
                format!("from typing import Any\n{name}Template = Any\n")
            }
        };
        output
            .entry(directory.strip_prefix(root)?.join("_anvil_designer.pyi"))
            .or_default()
            .push_str(&format!("{stub}\n"));
    }
    Ok(output.into_iter().collect())
}
