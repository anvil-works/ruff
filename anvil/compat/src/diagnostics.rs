//! Anvil runtime rules shared by IDE analysis and native validation.
use ruff_python_ast::visitor::{Visitor, walk_expr, walk_stmt};
use ruff_python_ast::{Expr, Stmt};
use ruff_text_size::{Ranged, TextRange};
use serde::Deserialize;
use std::collections::{HashMap, HashSet};
#[cfg(feature = "browser")]
use wasm_bindgen::JsValue;

#[derive(Default, Deserialize)]
#[serde(default, rename_all = "camelCase")]
pub struct Context {
    pub client: bool,
    pub form_class: Option<String>,
    pub duplicate_callables: HashSet<String>,
    pub duplicate_tasks: HashSet<String>,
    pub show_handlers: HashMap<String, String>,
}

pub struct Diagnostic {
    pub range: TextRange,
    pub rule: &'static str,
    pub message: String,
}

/// Callers resolve API references through Ty in their own analysis environment.
pub fn check<'ast>(
    body: &'ast [Stmt],
    context: &Context,
    mut resolve: impl FnMut(&Expr) -> Option<String>,
) -> Vec<Diagnostic> {
    let show_handlers = effective_show_handlers(body, context, &mut resolve);
    let mut checks = Checks {
        show_handlers,
        context,
        resolve,
        diagnostics: Vec::new(),
        module_scope: true,
        form_scope: false,
        show_body: None,
    };
    checks.visit_body(body);
    checks.diagnostics
}

struct Checks<'a, F> {
    context: &'a Context,
    show_handlers: HashSet<String>,
    resolve: F,
    diagnostics: Vec<Diagnostic>,
    module_scope: bool,
    form_scope: bool,
    show_body: Option<TextRange>,
}

fn decorator_target(expression: &Expr) -> &Expr {
    match expression {
        Expr::Call(call) => &call.func,
        expression => expression,
    }
}

/// Dynamic registration names cannot establish a known collision.
pub fn registration_name<'a>(decorator: &'a Expr, default: &'a str) -> Option<&'a str> {
    let Expr::Call(call) = decorator else {
        return Some(default);
    };
    let argument = call
        .arguments
        .keywords
        .iter()
        .find(|keyword| {
            keyword
                .arg
                .as_ref()
                .is_some_and(|name| name == "name" || name == "fn_or_name")
        })
        .map(|keyword| &keyword.value)
        .or_else(|| call.arguments.args.first());
    match argument {
        None | Some(Expr::NoneLiteral(_)) => Some(default),
        Some(Expr::StringLiteral(value)) => Some(value.value.to_str()),
        _ => None,
    }
}

/// Preserve component identities: a decorated handler replaces that component's
/// YAML binding, without replacing show handlers on other components.
pub fn show_handlers(template: &serde_json::Value) -> HashMap<String, String> {
    fn visit(value: &serde_json::Value, component: &str, handlers: &mut HashMap<String, String>) {
        let component = value["name"].as_str().unwrap_or(component);
        if let Some(handler) = value["event_bindings"]["show"].as_str() {
            handlers.insert(component.to_owned(), handler.to_owned());
        }
        if let Some(handler) = value["form_event_bindings"]["show"].as_str() {
            handlers.insert(String::new(), handler.to_owned());
        }
        if let Some(children) = value["components"].as_array() {
            for child in children {
                visit(child, "", handlers);
            }
        }
        for (key, name) in [("container", component), ("layout", "layout")] {
            if value[key].is_object() {
                visit(&value[key], name, handlers);
            }
        }
        if let Some(slots) = value["components_by_slot"].as_object() {
            for children in slots.values().filter_map(serde_json::Value::as_array) {
                for child in children {
                    visit(child, "", handlers);
                }
            }
        }
    }
    let mut handlers = HashMap::new();
    visit(template, "", &mut handlers);
    handlers
}

fn effective_show_handlers(
    body: &[Stmt],
    context: &Context,
    resolve: &mut impl FnMut(&Expr) -> Option<String>,
) -> HashSet<String> {
    let mut yaml = context.show_handlers.clone();
    let mut handlers = HashSet::new();
    for statement in body {
        let Stmt::ClassDef(class) = statement else {
            continue;
        };
        if context.form_class.as_deref() != Some(class.name.as_str()) {
            continue;
        }
        for statement in &class.body {
            let Stmt::FunctionDef(method) = statement else {
                continue;
            };
            for decorator in &method.decorator_list {
                let Expr::Call(call) = &decorator.expression else {
                    continue;
                };
                let [Expr::StringLiteral(component), Expr::StringLiteral(event)] =
                    call.arguments.args.as_ref()
                else {
                    continue;
                };
                if event.value.to_str() == "show"
                    && resolve(&call.func).as_deref() == Some("handle")
                {
                    yaml.remove(component.value.to_str());
                    handlers.insert(method.name.to_string());
                }
            }
        }
    }
    handlers.extend(yaml.into_values());
    handlers
}

impl<'ast, F: FnMut(&Expr) -> Option<String>> Visitor<'ast> for Checks<'_, F> {
    fn visit_stmt(&mut self, statement: &'ast Stmt) {
        if let Stmt::FunctionDef(function) = statement
            && !self.context.client
            && self.module_scope
        {
            for decorator in &function.decorator_list {
                let Some(name) = registration_name(&decorator.expression, function.name.as_str())
                else {
                    continue;
                };
                let api = (self.resolve)(decorator_target(&decorator.expression));
                let (rule, kind) = match api.as_deref() {
                    Some("callable") if self.context.duplicate_callables.contains(name) => {
                        ("reportAnvilDuplicateCallable", "callable functions")
                    }
                    Some("background_task") if self.context.duplicate_tasks.contains(name) => {
                        ("reportAnvilDuplicateBackgroundTask", "background tasks")
                    }
                    _ => continue,
                };
                self.diagnostics.push(Diagnostic { range: decorator.expression.range(), rule,
                    message: format!("It looks like you have multiple {kind} named '{name}'. This is probably not what you want.") });
            }
        }
        if let Stmt::ClassDef(class) = statement
            && (!self.context.client || self.context.form_class.is_some())
        {
            for decorator in &class.decorator_list {
                if (self.resolve)(decorator_target(&decorator.expression)).as_deref()
                    == Some("portable_class")
                {
                    let location = if self.context.client {
                        "Forms"
                    } else {
                        "Server Modules"
                    };
                    self.diagnostics.push(Diagnostic {
                        range: decorator.expression.range(),
                        rule: "reportAnvilPortableClassPlacement",
                        message: format!("You should define Portable Classes in Modules (not {location}), so they can be imported from both server and client code."),
                    });
                }
            }
        }
        let module_scope = self.module_scope;
        let form_scope = self.form_scope;
        let show_body = self.show_body;
        match statement {
            Stmt::ClassDef(class) => {
                self.form_scope = self.module_scope
                    && self.context.form_class.as_deref() == Some(class.name.as_str());
                self.show_body = None;
            }
            Stmt::FunctionDef(function) => {
                let show = self.context.client
                    && self.form_scope
                    && self.show_handlers.contains(function.name.as_str());
                self.show_body = if show {
                    function
                        .body
                        .first()
                        .zip(function.body.last())
                        .map(|(first, last)| TextRange::new(first.start(), last.end()))
                } else {
                    None
                };
                self.form_scope = false;
            }
            _ => {}
        }
        if matches!(statement, Stmt::FunctionDef(_) | Stmt::ClassDef(_)) {
            self.module_scope = false;
        }
        walk_stmt(self, statement);
        self.module_scope = module_scope;
        self.form_scope = form_scope;
        self.show_body = show_body;
    }

    fn visit_expr(&mut self, expression: &'ast Expr) {
        if let Expr::Call(call) = expression
            && self
                .show_body
                .is_some_and(|body| body.contains(call.start()))
            && (self.resolve)(&call.func).as_deref() == Some("open_form")
        {
            self.diagnostics.push(Diagnostic { range: call.range(), rule: "reportAnvilOpenFormInShow",
                message: "Calling open_form() from a show event handler may cause unexpected navigation while the form is still being shown.".to_owned() });
        }
        let show_body = self.show_body;
        if matches!(expression, Expr::Lambda(_)) {
            self.show_body = None;
        }
        walk_expr(self, expression);
        self.show_body = show_body;
    }
}

#[cfg(feature = "browser")]
#[wasm_bindgen::prelude::wasm_bindgen(js_name = anvilDiagnostics)]
pub fn browser_diagnostics(
    source: &str,
    context: &str,
    resolve: &js_sys::Function,
) -> Result<String, wasm_bindgen::JsValue> {
    let context =
        serde_json::from_str(context).map_err(|error| JsValue::from_str(&error.to_string()))?;
    let parsed =
        ruff_python_parser::parse_unchecked_source(source, ruff_python_ast::PySourceType::Python);
    let positions = crate::positions::Positions::new(source);
    let mut failure = None;
    let diagnostics = check(&parsed.syntax().body, &context, |expression| {
        let offset = match expression {
            Expr::Attribute(attribute) => attribute.attr.start(),
            expression => expression.start(),
        };
        let (line, character) = positions.coordinates(offset);
        match resolve.call2(
            &JsValue::NULL,
            &JsValue::from_f64(line as f64),
            &JsValue::from_f64(character as f64),
        ) {
            Ok(value) => value.as_string(),
            Err(error) => {
                failure = Some(error);
                None
            }
        }
    });
    if let Some(error) = failure {
        return Err(error);
    }
    Ok(serde_json::json!(diagnostics.into_iter().map(|diagnostic| {
        serde_json::json!({ "range": { "start": positions.at(diagnostic.range.start()), "end": positions.at(diagnostic.range.end()) },
            "code": diagnostic.rule, "message": diagnostic.message })
    }).collect::<Vec<_>>()).to_string())
}
