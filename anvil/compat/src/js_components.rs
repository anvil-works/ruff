//! Designer-registered JavaScript components, without replacing Python package sources.
use std::collections::{BTreeMap, BTreeSet};

use ruff_python_stdlib::identifiers::is_identifier;
use serde_json::Value;

#[derive(Default)]
pub(crate) struct Declarations {
    pub stubs: BTreeMap<String, String>,
    pub exports: BTreeMap<String, BTreeSet<String>>,
    pub packages: BTreeSet<String>,
}

fn parameters(args: &[Value]) -> String {
    let mut parameters = Vec::new();
    let mut keyword_only = false;
    for arg in args {
        let Some(name) = arg["name"]
            .as_str()
            .filter(|name| is_identifier(name) && *name != "self")
        else {
            continue;
        };
        let kind = arg["type"].as_str();
        if kind == Some("keyword") && !keyword_only {
            parameters.push("*".to_owned());
            keyword_only = true;
        }
        if matches!(kind, Some("varargs" | "kwargs")) {
            parameters.push(format!(
                "{}{name}: Any",
                if kind == Some("varargs") { "*" } else { "**" }
            ));
            keyword_only = true;
        } else {
            parameters.push(format!(
                "{name}: Any{}",
                if arg["optional"] == true {
                    " = ..."
                } else {
                    ""
                }
            ));
        }
    }
    if parameters.is_empty() {
        String::new()
    } else {
        format!(", {}", parameters.join(", "))
    }
}

fn description(stub: &mut String, value: &Value, indent: &str) {
    if let Some(text) = value.as_str() {
        stub.push_str(&format!(
            "{indent}{}\n",
            serde_json::to_string(text).unwrap()
        ));
    }
}

fn properties(component: &Value, key: &str) -> Vec<Value> {
    component[key]
        .as_array()
        .into_iter()
        .flatten()
        .filter(|property| property["name"].as_str().is_some_and(is_identifier))
        .cloned()
        .collect()
}

fn keyword_parameters(properties: &[Value]) -> String {
    let parameters: Vec<_> = properties
        .iter()
        .filter_map(|property| property["name"].as_str().filter(|name| *name != "self"))
        .map(|name| format!("{name}: Any = ..."))
        .collect();
    if parameters.is_empty() {
        String::new()
    } else {
        format!(", *, {}", parameters.join(", "))
    }
}

pub(crate) fn declarations(metadata: &Value, packages: &BTreeMap<String, String>) -> Declarations {
    let mut output = Declarations::default();
    // Generated stubs and canonical app packages share Python search roots.
    let mut namespace = "_anvil_js_components".to_owned();
    while packages.contains_key(&namespace) {
        namespace.push('_');
    }
    for component in metadata["components"].as_array().into_iter().flatten() {
        let Some(name) = component["name"].as_str() else {
            continue;
        };
        let parts: Vec<_> = name.split('.').collect();
        if parts.len() < 2
            || !packages.contains_key(parts[0])
            || !parts.iter().all(|part| is_identifier(part))
        {
            continue;
        }
        let class = parts.last().unwrap();
        let module = parts.join("/");
        let mut stub = format!(
            "from typing import Any\nimport anvil\n\nclass {class}(anvil.{}):\n",
            if component["container"] == true {
                "Container"
            } else {
                "Component"
            }
        );
        stub.push_str("    \"\"\"JavaScript component registered in the Designer.\"\"\"\n");
        let fields = properties(component, "properties");
        for field in &fields {
            stub.push_str(&format!("    {}: Any\n", field["name"].as_str().unwrap()));
            description(&mut stub, &field["description"], "    ");
        }
        stub.push_str(&format!(
            "    def __init__(self{}, **kwargs: Any) -> None: ...\n",
            keyword_parameters(&fields)
        ));
        for method in component["methods"].as_array().into_iter().flatten() {
            let Some(name) = method["name"].as_str().filter(|name| is_identifier(name)) else {
                continue;
            };
            let args = method["args"].as_array().map_or_else(
                || ", *args: Any, **kwargs: Any".to_owned(),
                |args| parameters(args),
            );
            stub.push_str(&format!("    def {name}(self{args}) -> Any:\n"));
            description(&mut stub, &method["description"], "        ");
            stub.push_str("        ...\n");
        }
        if component["container"] == true {
            stub.push_str(&format!("    def add_component(self, component: anvil.Component, /{}, **kwargs: Any) -> None: ...\n", keyword_parameters(&properties(component, "layoutProperties"))));
        }
        output
            .stubs
            .insert(format!("{namespace}/{module}.pyi"), stub);
        output
            .exports
            .entry(module)
            .or_default()
            .insert(format!("from {namespace}.{name} import {class} as {class}"));
        for end in 1..parts.len() {
            let parent = parts[..end].join("/");
            output.packages.insert(parent.clone());
            output.exports.entry(parent).or_default().insert(format!(
                "import {} as {}",
                parts[..=end].join("."),
                parts[end]
            ));
        }
        for end in 0..parts.len() {
            let parent = parts[..end].join("/");
            let directory = if parent.is_empty() {
                namespace.clone()
            } else {
                format!("{namespace}/{parent}")
            };
            output
                .stubs
                .entry(format!("{directory}/__init__.pyi"))
                .or_default();
        }
    }
    output
}
