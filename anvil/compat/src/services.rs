//! Service declarations ported from the baseline's users/Drive metadata policy.
use anyhow::{Result, ensure};
use serde_json::Value;

use crate::identifier;

pub fn users(
    config: &Value,
    base: &str,
    models: &crate::models::Registry,
    environment: &str,
) -> Result<Option<String>> {
    let Some(service) = config["services"]
        .as_array()
        .into_iter()
        .flatten()
        .find(|service| {
            service["source"]
                .as_str()
                .is_some_and(|source| source.contains("anvil/users"))
        })
    else {
        return Ok(None);
    };
    let Some(schema) = config["db_schema"].as_object() else {
        return Ok(None);
    };
    let name = service["server_config"]["user_table"].as_str().or_else(|| {
        schema
            .keys()
            .find(|name| name.eq_ignore_ascii_case("users"))
            .map(String::as_str)
    });
    let Some((name, table)) = name.and_then(|name| schema.get(name).map(|table| (name, table)))
    else {
        return Ok(None);
    };
    let python = table["python_name"].as_str().unwrap_or(name);
    ensure!(
        identifier(python),
        "unsupported user table Python name: {python}"
    );
    // Preserve imports, parameter types and optionality. Only return annotations
    // acquire the app's row type, as in generateAnvilUsersStub.
    let import = if let Some(model) = models.get(name, environment) {
        format!(
            "from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n    from {} import {} as _AnvilUser\n",
            model.module, model.name
        )
    } else {
        format!("from anvil.tables import _Row_{python} as _AnvilUser\n")
    };
    Ok(Some(format!(
        "{import}{}",
        base.replace("-> Row", "-> _AnvilUser")
    )))
}

pub fn drive(config: &Value, base: &str) -> Result<Option<String>> {
    let Some(service) = config["services"]
        .as_array()
        .into_iter()
        .flatten()
        .find(|service| {
            service["source"]
                .as_str()
                .is_some_and(|source| source.contains("google"))
        })
    else {
        return Ok(None);
    };
    let mut attributes = String::new();
    let mut sheets = false;
    for file in service["client_config"]["app_files"]
        .as_array()
        .into_iter()
        .flatten()
    {
        let (Some(name), Some(mime), Some(_id)) = (
            file["python_name"].as_str(),
            file["mimeType"].as_str(),
            file["id"].as_str(),
        ) else {
            continue;
        };
        ensure!(
            identifier(name),
            "unsupported Drive file Python name: {name}"
        );
        let kind = match mime {
            "application/vnd.google-apps.spreadsheet" => {
                sheets = true;
                "Spreadsheet"
            }
            "application/vnd.google-apps.folder" => "Folder",
            _ => "File",
        };
        attributes.push_str(&format!("    {name}: {kind}\n"));
    }
    if attributes.is_empty() {
        return Ok(None);
    }
    let marker = "    ...\n\napp_files: _AppFiles = ...";
    ensure!(
        base.contains(marker),
        "static Drive stub lacks app_files marker"
    );
    let output = base.replace(marker, &format!("{attributes}\napp_files: _AppFiles = ..."));
    Ok(Some(if sheets {
        format!("from anvil.google.sheets import Spreadsheet\n{output}")
    } else {
        output
    }))
}
