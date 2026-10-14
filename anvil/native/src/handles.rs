//! Validate decorator targets using the same metadata as native designer generation.
use std::collections::{BTreeMap, BTreeSet, HashMap};
use std::path::{Path, PathBuf};

use anyhow::Result;
use ruff_db::files::{File, system_path_to_file};
use ruff_db::parsed::parsed_module;
use ruff_db::system::SystemPath;
use ruff_python_ast::visitor::{Visitor, walk_stmt};
use ruff_python_ast::{Expr, Stmt};
use ruff_text_size::Ranged;
use serde_json::Value;
use ty_project::ProjectDatabase;
use ty_python_semantic::types::TypeDefinition;
use ty_python_semantic::{Db, HasType, SemanticModel};

struct Form {
    name: String,
    events: Option<BTreeSet<String>>,
    components: BTreeMap<String, String>,
}

#[derive(Default)]
pub struct Registry {
    forms: HashMap<PathBuf, Form>,
    modules: HashMap<String, PathBuf>,
}

impl Registry {
    pub fn collect(
        &mut self,
        source: PathBuf,
        root: &Path,
        package: &str,
        name: &str,
        template: &Value,
        components: BTreeMap<String, String>,
    ) {
        let relative = source.strip_prefix(root).unwrap();
        self.modules.insert(
            crate::imports::module_name(package, relative),
            source.clone(),
        );
        let mut events = builtin_events(
            template["container"]["type"]
                .as_str()
                .unwrap_or("ColumnPanel"),
        )
        .map(|events| {
            events
                .into_iter()
                .map(str::to_owned)
                .collect::<BTreeSet<_>>()
        });
        if let Some(events) = &mut events {
            events.insert("refreshing_data_bindings".to_owned());
            if let Some(custom) = template["events"].as_array() {
                events.extend(
                    custom
                        .iter()
                        .filter_map(|event| event["name"].as_str())
                        .map(str::to_owned),
                );
            }
        }
        self.forms.insert(
            source,
            Form {
                name: name.to_owned(),
                events,
                components,
            },
        );
    }

    pub fn check(
        &self,
        db: &ProjectDatabase,
        path: &SystemPath,
        origin: &Path,
        api: &SystemPath,
    ) -> Result<Vec<Value>> {
        let Some(form) = self.forms.get(origin) else {
            return Ok(Vec::new());
        };
        let file = system_path_to_file(db, path)?;
        let model = SemanticModel::new(db, db.program_file(file));
        let parsed = parsed_module(db, model.python_file()).load(db);
        let mut visitor = Handles {
            model,
            api: system_path_to_file(db, api)?,
            origin,
            form,
            registry: self,
            issues: Vec::new(),
        };
        visitor.visit_body(&parsed.syntax().body);
        Ok(visitor.issues)
    }

    fn events(&self, form: &Form, component: &str) -> Option<BTreeSet<String>> {
        if component.is_empty() {
            return form.events.clone();
        }
        let kind = &form.components[component];
        if let Some(events) = builtin_events(kind) {
            return Some(events.into_iter().map(str::to_owned).collect());
        }
        self.forms.get(self.modules.get(kind)?)?.events.clone()
    }
}

struct Handles<'db, 'r> {
    model: SemanticModel<'db>,
    api: File,
    origin: &'r Path,
    form: &'r Form,
    registry: &'r Registry,
    issues: Vec<Value>,
}

impl<'ast> Visitor<'ast> for Handles<'_, '_> {
    fn visit_stmt(&mut self, stmt: &'ast Stmt) {
        if let Stmt::FunctionDef(function) = stmt {
            for decorator in &function.decorator_list {
                let Expr::Call(call) = &decorator.expression else {
                    continue;
                };
                let valid = call
                    .func
                    .inferred_type(&self.model)
                    .and_then(|ty| {
                        ty.definition(self.model.db(), &self.model.program_environment())
                    })
                    .is_some_and(|definition| match definition {
                        TypeDefinition::Function(definition) => {
                            definition.file(self.model.db()) == self.api
                                && definition.name(self.model.db()).as_deref() == Some("handle")
                        }
                        _ => false,
                    });
                if !valid {
                    continue;
                }
                let Some(Expr::StringLiteral(component)) = call.arguments.args.first() else {
                    continue;
                };
                let name = component.value.to_str();
                if !name.is_empty() && !self.form.components.contains_key(name) {
                    self.issues.push(crate::checks::issue(
                        self.model.db(),
                        self.model.file(),
                        self.origin,
                        decorator.range(),
                        "reportAnvilUnknownComponent",
                        "warning",
                        format!("{} has no component named '{name}'", self.form.name),
                    ));
                    continue;
                }
                let Some(Expr::StringLiteral(event)) = call.arguments.args.get(1) else {
                    continue;
                };
                let event = event.value.to_str();
                if let Some(events) = self.registry.events(self.form, name) {
                    // Component.$verifyEventName accepts arbitrary x- custom events.
                    if !event.starts_with("x-") && !events.contains(event) {
                        let target = if name.is_empty() {
                            &self.form.name
                        } else {
                            &self.form.components[name]
                        };
                        self.issues.push(crate::checks::issue(
                            self.model.db(),
                            self.model.file(),
                            self.origin,
                            decorator.range(),
                            "reportAnvilInvalidEvent",
                            "warning",
                            format!(
                                "{target} has no event '{event}'. Valid events: {}",
                                events.into_iter().collect::<Vec<_>>().join(", ")
                            ),
                        ));
                    }
                }
            }
        }
        walk_stmt(self, stmt);
    }
}

// Ported from anvil-pyright/src/anvil/componentEvents.ts, corrected against
// anvil/runtime/client/js/components and PyDefUtils/event-groups.ts. Custom form
// types are resolved separately from their metadata.
fn builtin_events(kind: &str) -> Option<Vec<&'static str>> {
    let kind = kind.strip_prefix("anvil.").unwrap_or(kind);
    if kind.contains(':') || kind.contains('.') {
        return None;
    }
    let specific: &[&str] = match kind {
        "Button" | "Link" => &["click"],
        "TextBox" => &["change", "pressed_enter", "lost_focus", "focus"],
        "TextArea" => &["change", "lost_focus", "focus"],
        "CheckBox" | "DropDown" | "DatePicker" | "FileLoader" => &["change"],
        "RadioButton" => &["change", "clicked"],
        "Timer" => &["tick"],
        "Canvas" => &[
            "reset",
            "mouse_down",
            "mouse_up",
            "mouse_move",
            "mouse_enter",
            "mouse_leave",
        ],
        "Image" => &[
            "mouse_down",
            "mouse_up",
            "mouse_move",
            "mouse_enter",
            "mouse_leave",
        ],
        "Plot" => &["click", "double_click", "hover", "unhover", "select"],
        "GoogleMap" => &["bounds_changed", "click", "zoom_changed"],
        "YouTubeVideo" => &["state_change"],
        "DataGrid" => &["page_changed"],
        _ => &[],
    };
    Some(specific.iter().copied().chain(["show", "hide"]).collect())
}
