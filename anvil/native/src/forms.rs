//! Native form preparation. Generated stubs preserve source apps and use ty normally.
use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::{Path, PathBuf};

use anyhow::{Context, Result, ensure};
use ruff_python_ast::visitor::{Visitor, walk_stmt};
use ruff_python_ast::{Expr, Stmt};
use ruff_python_parser::parse_module;
use scraper::{ElementRef, Html};
use serde_json::{Value, json};
use walkdir::WalkDir;

use crate::{identifier, populated, yaml};

// A canonical type name identifies the component for event validation; the stub
// annotation may instead be an import alias local to the generated designer file.
struct ComponentType {
    name: String,
    annotation: String,
}

/// A client package's directory, Python modules and public import name.
pub struct ClientCode<'a> {
    pub root: &'a Path,
    pub sources: &'a [crate::Source],
    pub package: &'a str,
}

struct ComponentTypes<'a> {
    root: &'a Path,
    package: &'a str,
    api: &'a str,
    form: &'a str,
    dependencies: &'a [crate::dependencies::Dependency],
    imports: BTreeMap<String, String>,
    components: BTreeMap<String, String>,
}

impl ComponentTypes<'_> {
    fn resolve(&mut self, value: &Value) -> Result<ComponentType> {
        let name = value.as_str().context("form component needs a type")?;
        if identifier(name) && self.api.contains(&format!("class {name}(")) {
            return Ok(ComponentType {
                name: format!("anvil.{name}"),
                annotation: format!("anvil.{name}"),
            });
        }
        let (root, package, local) = if let Some(form) = name.strip_prefix("form:") {
            if let Some((id, local)) = form.rsplit_once(':') {
                let dependency = self
                    .dependencies
                    .iter()
                    .find(|dependency| dependency.ids.iter().any(|value| value == id))
                    .context(format!("referenced dependency is missing: {id}"))?;
                (
                    dependency.root.join("client_code"),
                    dependency.package.as_str(),
                    local,
                )
            } else {
                (self.root.to_owned(), self.package, form)
            }
        } else if let Some(local) = name
            .strip_prefix(self.package)
            .and_then(|s| s.strip_prefix('.'))
        {
            (self.root.to_owned(), self.package, local)
        } else {
            self.dependencies
                .iter()
                .find_map(|dependency| {
                    name.strip_prefix(&dependency.package)
                        .and_then(|s| s.strip_prefix('.'))
                        .map(|local| {
                            (
                                dependency.root.join("client_code"),
                                dependency.package.as_str(),
                                local,
                            )
                        })
                })
                .context(format!("unsupported form component type: {name}"))?
        };
        ensure!(
            local.split('.').all(identifier),
            "unsupported form reference: {name}"
        );
        let path = root.join(local.replace('.', "/"));
        ensure!(
            path.with_extension("py").is_file() || path.join("__init__.py").is_file(),
            "referenced form is missing: {name}"
        );
        let module = format!("{package}.{local}");
        let next = self.imports.len();
        let annotation = self
            .imports
            .entry(module.clone())
            .or_insert_with(|| format!("_{}Component{next}", self.form))
            .clone();
        Ok(ComponentType {
            name: module,
            annotation,
        })
    }
}

fn components(
    items: &Value,
    types: &mut ComponentTypes<'_>,
    output: &mut String,
    handlers: &mut BTreeSet<String>,
) -> Result<()> {
    if let Some(items) = items.as_array() {
        for item in items {
            // The baseline designer parser does not analyze binding expressions.
            // anvil-cli retains responsibility for template structure validation.
            let kind = types.resolve(&item["type"])?;
            event_handlers(&item["event_bindings"], handlers)?;
            // Anonymous runtime names such as `$component_1` are not Python
            // attributes. Their children and event metadata still participate.
            if let Some(name) = item["name"].as_str().filter(|name| !name.is_empty()) {
                if identifier(name) {
                    output.push_str(&format!("    {name}: {}\n", kind.annotation));
                }
                types.components.insert(name.to_owned(), kind.name);
            }
            components(&item["components"], types, output, handlers)?;
        }
    } else {
        ensure!(!populated(items), "components must be a sequence");
    }
    Ok(())
}

fn event_handlers(bindings: &Value, handlers: &mut BTreeSet<String>) -> Result<()> {
    if let Some(bindings) = bindings.as_object() {
        for handler in bindings.values() {
            let handler = handler
                .as_str()
                .context("event binding needs a handler name")?;
            ensure!(
                identifier(handler),
                "unsupported event handler name: {handler}"
            );
            handlers.insert(handler.to_owned());
        }
    } else {
        ensure!(!populated(bindings), "event bindings must be a mapping");
    }
    Ok(())
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
            let owned = sources
                .iter()
                .find(|code| code.path == source)
                .map(|code| defined_members(&code.text, name))
                .unwrap_or_default();
            let mut template = if format == "html" {
                html_template(&fs::read_to_string(entry.path())?)?
            } else {
                yaml(entry.path())?
            };
            if template["container"]["type"] == "HtmlTemplate"
                && let Some(html) = template["container"]["properties"]["html"].as_str()
            {
                template["dom_nodes"] = dom_nodes(&Html::parse_fragment(html), "anvil-name");
            }
            let mut types = ComponentTypes {
                root,
                package,
                api,
                form: name,
                dependencies,
                imports: BTreeMap::new(),
                components: BTreeMap::new(),
            };
            let layout = if populated(&template["layout"]) {
                let layout = types.resolve(&template["layout"]["type"])?;
                types.components.insert("layout".to_owned(), layout.name);
                Some(layout.annotation)
            } else {
                None
            };
            let base = if layout.is_some() {
                "anvil.WithLayout".to_owned()
            } else {
                types.resolve(&template["container"]["type"])?.annotation
            };
            let mut attributes = String::new();
            let mut handlers = BTreeSet::new();
            event_handlers(&template["layout"]["form_event_bindings"], &mut handlers)?;
            components(
                &template["container"]["components"],
                &mut types,
                &mut attributes,
                &mut handlers,
            )?;
            components(
                &template["components"],
                &mut types,
                &mut attributes,
                &mut handlers,
            )?;
            if let Some(slots) = template["components_by_slot"].as_object() {
                for items in slots.values() {
                    components(items, &mut types, &mut attributes, &mut handlers)?;
                }
            }
            let properties = template["properties"].as_array().filter(|properties| {
                !properties.is_empty()
                    && (template["custom_component"] == true || populated(&template["slots"]))
            });
            let mut stub = "from typing import Any, Literal, TypedDict\nfrom typing_extensions import Unpack\nimport anvil\n".to_owned();
            let item_type = if let Some(table) = template["item_type"]["table_name"]
                .as_str()
                .filter(|name| !name.is_empty())
            {
                ensure!(identifier(table), "unsupported item table name: {table}");
                if let Some(model) = models.get(table, "client") {
                    stub.push_str(&format!(
                        "from {} import {} as _{name}Item\n",
                        model.module, model.name
                    ));
                } else {
                    stub.push_str(&format!(
                        "from anvil.tables import _Row_{table} as _{name}Item\n"
                    ));
                }
                format!("_{name}Item")
            } else {
                "Any".to_owned()
            };
            let (event_types, event_methods) = custom_events(&template["events"], name)?;
            stub.push_str(&event_types);
            if !handlers.is_empty() {
                stub.push_str("from abc import ABC, abstractmethod\n");
            }
            for (module, alias) in types.imports {
                let class = module.rsplit('.').next().unwrap();
                stub.push_str(&format!("from {module} import {class} as {alias}\n"));
            }
            if let Some(properties) = properties {
                stub.push_str(&format!(
                    "class _{name}Properties(TypedDict, total=False):\n"
                ));
                for property in properties {
                    let property_name = property["name"]
                        .as_str()
                        .context("form property needs a name")?;
                    ensure!(
                        identifier(property_name),
                        "invalid property identifier: {property_name}"
                    );
                    stub.push_str(&format!(
                        "    {property_name}: {}\n",
                        if owned.contains(property_name) {
                            "Any".to_owned()
                        } else {
                            property_type(property)?
                        }
                    ));
                }
            }
            if let Some(nodes) = template["dom_nodes"]
                .as_array()
                .filter(|nodes| !nodes.is_empty())
            {
                stub.push_str("import anvil.js.window as _dom\n");
                let mut entries = Vec::new();
                for node in nodes {
                    let key = node["name"].as_str().context("DOM node needs a name")?;
                    let tag = node["tagName"]
                        .as_str()
                        .context("DOM node needs a tagName")?;
                    entries.push(format!(
                        "{}: _dom.{}",
                        serde_json::to_string(key)?,
                        crate::dom::python_type(tag)
                    ));
                }
                stub.push_str(&format!(
                    "_{name}DomNodes = TypedDict(\"_{name}DomNodes\", {{{}}})\n",
                    entries.join(", ")
                ));
            }
            let inheritance = if handlers.is_empty() {
                base
            } else {
                format!("{base}, ABC")
            };
            stub.push_str(&format!("\nclass {name}Template({inheritance}):\n"));
            if let Some(layout) = layout {
                stub.push_str(&format!("    @property\n    def layout(self) -> {layout}: ...\n    @layout.setter\n    def layout(self, value: anvil.Component) -> None: ...\n"));
            }
            if let Some(properties) = properties {
                for property in properties {
                    let property_name = property["name"].as_str().unwrap();
                    // Designer input formats are not base-class promises for members supplied
                    // by Python. Keep their keyword names, but leave runtime value checking to
                    // the author's property and constructor annotations.
                    if owned.contains(property_name) {
                        continue;
                    }
                    let kind = property_type(property)?;
                    stub.push_str(&format!("    @property\n    def {property_name}(self) -> {kind}: ...\n    @{property_name}.setter\n    def {property_name}(self, value: {kind}) -> None: ...\n"));
                }
            }
            if template["dom_nodes"]
                .as_array()
                .is_some_and(|nodes| !nodes.is_empty())
            {
                stub.push_str(&format!("    dom_nodes: _{name}DomNodes\n"));
            }
            stub.push_str(&attributes);
            if populated(&template["slots"]) {
                ensure!(template["slots"].is_object(), "slots must be a mapping");
                stub.push_str("    slots: dict[str, anvil.Slot]\n");
            }
            stub.push_str(&event_methods);
            if !properties.is_some_and(|properties| {
                properties.iter().any(|property| property["name"] == "item")
            }) {
                stub.push_str(&format!("    @property\n    def item(self) -> {item_type}: ...\n    @item.setter\n    def item(self, value: {item_type}) -> None: ...\n"));
            }
            stub.push_str("    def refresh_data_bindings(self) -> None: ...\n");
            for handler in handlers {
                // Anvil accepts explicit sender/event parameters and **event_args.
                // A gradual base signature permits either override; calls to
                // concrete user methods retain their actual signatures.
                stub.push_str(&format!(
                "    @abstractmethod\n    def {handler}(self, *args: Any, **event_args: Any) -> Any: ...\n"
            ));
            }
            let property_args = if properties.is_some() {
                format!("Unpack[_{name}Properties]")
            } else {
                "Any".to_owned()
            };
            stub.push_str(&format!("    def __init__(self, **properties: {property_args}) -> None: ...\n    def init_components(self, **properties: {property_args}) -> None: ...\n"));
            handles.collect(
                source.clone(),
                root,
                package,
                name,
                &template,
                types.components,
            );
            Ok(stub)
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

fn custom_events(events: &Value, form: &str) -> Result<(String, String)> {
    let mut declarations = String::new();
    let mut methods = String::new();
    if let Some(events) = events.as_array() {
        for (index, event) in events.iter().enumerate() {
            let name = event["name"]
                .as_str()
                .context("custom event needs a name")?;
            ensure!(identifier(name), "unsupported custom event name: {name}");
            let parameters = event["parameters"]
                .as_array()
                .filter(|items| !items.is_empty());
            let args = if let Some(parameters) = parameters {
                let kind = format!("_{form}Event{index}Args");
                declarations.push_str(&format!(
                    "class {kind}(TypedDict):\n    sender: {form}Template\n    event_name: str\n"
                ));
                for parameter in parameters {
                    let name = parameter["name"]
                        .as_str()
                        .context("event parameter needs a name")?;
                    ensure!(identifier(name), "invalid event parameter: {name}");
                    declarations.push_str(&format!("    {name}: Any\n"));
                }
                format!("Unpack[{kind}]")
            } else {
                "Any".to_owned()
            };
            if parameters.is_some() {
                methods.push_str(&format!(
                    "    def {name}(self, **event_args: {args}) -> None: ...\n"
                ));
            } else {
                // Untyped event metadata does not constrain a user callback's
                // explicit sender, positional arguments or return value.
                methods.push_str(&format!(
                    "    def {name}(self, *args: Any, **event_args: Any) -> Any: ...\n"
                ));
            }
        }
    } else {
        ensure!(!populated(events), "events must be a sequence");
    }
    Ok((declarations, methods))
}

fn defined_members(source: &str, class_name: &str) -> BTreeSet<String> {
    struct Members(BTreeSet<String>);
    impl<'a> Visitor<'a> for Members {
        fn visit_stmt(&mut self, stmt: &'a Stmt) {
            match stmt {
                Stmt::FunctionDef(function) => {
                    self.0.insert(function.name.to_string());
                }
                Stmt::ClassDef(class) => {
                    self.0.insert(class.name.to_string());
                }
                Stmt::Assign(assign) => {
                    for target in &assign.targets {
                        if let Expr::Name(name) = target {
                            self.0.insert(name.id.to_string());
                        }
                    }
                }
                Stmt::AnnAssign(assign) => {
                    if let Expr::Name(name) = assign.target.as_ref() {
                        self.0.insert(name.id.to_string());
                    }
                }
                _ => walk_stmt(self, stmt),
            }
        }
    }
    // The checker reports malformed Python; preparation can still expose metadata-only members.
    let Ok(parsed) = parse_module(source) else {
        return BTreeSet::new();
    };
    let mut members = Members(BTreeSet::new());
    for stmt in &parsed.syntax().body {
        if let Stmt::ClassDef(class) = stmt
            && class.name.as_str() == class_name
        {
            for stmt in &class.body {
                members.visit_stmt(stmt);
            }
        }
    }
    members.0
}

fn property_type(property: &Value) -> Result<String> {
    let kind = property["type"]
        .as_str()
        .context("form property needs a type")?
        .to_ascii_lowercase();
    Ok(match kind.as_str() {
        "enum" => {
            let mut options: Vec<_> = property["options"]
                .as_array()
                .into_iter()
                .flatten()
                .filter_map(Value::as_str)
                .collect();
            options.sort_unstable();
            let base = if options.is_empty() {
                "Any".to_owned()
            } else {
                format!(
                    "Literal[{}]",
                    options
                        .into_iter()
                        .map(serde_json::to_string)
                        .collect::<std::result::Result<Vec<_>, _>>()?
                        .join(", ")
                )
            };
            if property["include_none_option"] == true {
                format!("{base} | None")
            } else {
                base
            }
        }
        "string" | "str" | "color" => "str".to_owned(),
        "themerole" => "str | list[str] | None".to_owned(),
        "number" => "int | float | None".to_owned(),
        "integer" | "int" => "int".to_owned(),
        "float" => "float".to_owned(),
        "boolean" | "bool" => "bool".to_owned(),
        "dict" => "dict[str, Any]".to_owned(),
        "list" | "array" => "list[Any]".to_owned(),
        _ => "Any".to_owned(),
    })
}

fn html_template(source: &str) -> Result<Value> {
    let (mut template, body) = frontmatter(source)?;
    let document = Html::parse_fragment(body);
    let root = document.root_element();
    let significant: Vec<_> = root
        .children()
        .filter(|node| {
            !node.value().is_comment()
                && !node
                    .value()
                    .as_text()
                    .is_some_and(|text| text.trim().is_empty())
        })
        .collect();
    // A sole ordinary HTML root is the form itself; its anvil:name is ignored.
    let plain_root = if significant.len() == 1 {
        ElementRef::wrap(significant[0])
            .filter(|element| !element.value().name().starts_with("anvil-"))
            .map(|element| element.id())
    } else {
        None
    };
    let mut base = "HtmlComponent";
    let mut components = Vec::new();
    let mut layout = None;
    let mut form_events = Value::Null;
    let mut slots = serde_json::Map::new();
    for element in document
        .root_element()
        .descendants()
        .filter_map(ElementRef::wrap)
    {
        let id = element.id();
        let element = element.value();
        if element.name() == "anvil-form" {
            layout = element.attr("layout");
            base = element.attr("container").unwrap_or("HtmlComponent");
            form_events = html_events(element, "on:");
            // on:layout:* maps to layout.event_bindings, which the baseline
            // designer does not use to require form methods.
            form_events
                .as_object_mut()
                .unwrap()
                .retain(|event, _| !event.starts_with("layout:"));
        } else if element.name() == "anvil-slot" {
            // Only presence matters for the designer's generic slots mapping.
            let name = element.attr("name").unwrap_or("");
            slots.insert(name.to_owned(), json!({}));
        } else if element.name() == "anvil-component" {
            components.push(json!({"name": element.attr("name"), "type": element.attr("type"), "event_bindings": html_events(element, "on:")}));
        } else if Some(id) != plain_root
            && let Some(name) = element.attr("anvil:name").filter(|name| !name.is_empty())
        {
            components.push(json!({"name": name, "type": "HtmlComponent", "event_bindings": html_events(element, "anvil:on:")}));
        }
    }
    // HTML structure is authoritative over frontmatter, as in formTemplateParser.ts.
    template["container"] = json!({"type": base});
    template["layout"] = layout.map_or(
        Value::Null,
        |kind| json!({"type": kind, "form_event_bindings": form_events}),
    );
    template["slots"] = Value::Object(slots);
    template["components"] = json!(components);
    template["dom_nodes"] = dom_nodes(&document, "anvil:dom-node");
    Ok(template)
}

fn html_events(element: &scraper::node::Element, prefix: &str) -> Value {
    Value::Object(
        element
            .attrs()
            .filter_map(|(key, value)| {
                key.strip_prefix(prefix).map(|event| {
                    (
                        event.to_owned(),
                        json!(value.strip_prefix("self.").unwrap_or(value)),
                    )
                })
            })
            .collect(),
    )
}

fn dom_nodes(document: &Html, attribute: &str) -> Value {
    let mut nodes = BTreeMap::new();
    for element in document
        .root_element()
        .descendants()
        .filter_map(ElementRef::wrap)
    {
        if let Some(name) = element
            .value()
            .attr(attribute)
            .filter(|name| !name.is_empty())
        {
            nodes.entry(name).or_insert(element.value().name());
        }
    }
    json!(
        nodes
            .into_iter()
            .map(|(name, tag)| json!({"name": name, "tagName": tag}))
            .collect::<Vec<_>>()
    )
}

fn frontmatter(source: &str) -> Result<(Value, &str)> {
    if let Some(first) = source
        .split_inclusive('\n')
        .next()
        .filter(|line| line.trim_end() == "---")
    {
        let mut offset = first.len();
        for line in source[offset..].split_inclusive('\n') {
            if line.trim_end() == "---" {
                let value: Value = serde_yaml::from_str(&source[first.len()..offset])?;
                ensure!(
                    value.is_null() || value.is_object(),
                    "HTML form frontmatter must be a YAML object"
                );
                return Ok((
                    if value.is_null() { json!({}) } else { value },
                    &source[offset + line.len()..],
                ));
            }
            offset += line.len();
        }
    }
    Ok((json!({}), source))
}
