//! Inferred type declarations and literal-name RPC overloads.
use ruff_python_ast::{AnyParameterRef, Expr, PySourceType, Stmt};
use ruff_python_parser::parse_unchecked_source;
use ruff_text_size::Ranged;
use serde::Deserialize;
use serde_json::json;
use wasm_bindgen::prelude::*;

use crate::positions::Positions;

/// Describe a callable's parameter shape without evaluating defaults or moving
/// server-local annotations into the client namespace. The worker infers each
/// annotated probe's portable type through the same path as RPC return types.
#[wasm_bindgen(js_name = rpcSignature)]
pub fn rpc_signature(source: &str, name: &str, rpc_name: &str) -> String {
    let parsed = parse_unchecked_source(source, PySourceType::Python);
    let mut functions = parsed
        .syntax()
        .body
        .iter()
        .filter_map(|statement| match statement {
            Stmt::FunctionDef(function) if function.name.as_str() == name => Some(function),
            _ => None,
        });
    let Some(function) = functions.next() else {
        return "null".into();
    };
    // Overload sets cannot be reduced to one implementation signature. Keep the
    // ordinary RPC fallback until their complete contract can be exported.
    if functions.next().is_some() {
        return "null".into();
    }
    let mut prefix = "_AnvilRpc".to_owned();
    while source.contains(&prefix) {
        prefix.push('_');
    }
    let mut probes = Vec::new();
    let mut probe_source = String::new();
    let result_probe = function.returns.as_deref().map(|annotation| {
        let name = format!("{prefix}Result");
        probe_source.push_str(&format!(
            "\ndef {name}() -> ({}): ...\n",
            &source[annotation.range()]
        ));
        name
    });
    let mut parameter = |parameter: AnyParameterRef<'_>, stars: &str| {
        let annotation = if let Some(annotation) = parameter.annotation() {
            let probe = format!("{prefix}Arg{}", probes.len());
            probe_source.push_str(&format!(
                "\ndef {probe}() -> ({}): ...\n",
                &source[annotation.range()]
            ));
            probes.push(probe.clone());
            probe
        } else {
            format!("{prefix}Any")
        };
        format!(
            "{stars}{}: {annotation}{}",
            parameter.name(),
            if parameter.default().is_some() {
                " = ..."
            } else {
                ""
            }
        )
    };
    let params = &function.parameters;
    let mut name_parameter = "fn_name".to_owned();
    while params
        .iter()
        .any(|param| param.name().as_str() == name_parameter)
    {
        name_parameter.push('_');
    }
    let mut signature = vec![
        format!("{prefix}self"),
        format!(
            "{name_parameter}: {prefix}Literal[{}]",
            serde_json::to_string(rpc_name).unwrap()
        ),
    ];
    signature.extend(
        params
            .posonlyargs
            .iter()
            .map(|param| parameter(AnyParameterRef::NonVariadic(param), "")),
    );
    signature.push("/".into());
    signature.extend(
        params
            .args
            .iter()
            .map(|param| parameter(AnyParameterRef::NonVariadic(param), "")),
    );
    if let Some(param) = &params.vararg {
        signature.push(parameter(AnyParameterRef::Variadic(param), "*"));
    } else if !params.kwonlyargs.is_empty() {
        signature.push("*".into());
    }
    signature.extend(
        params
            .kwonlyargs
            .iter()
            .map(|param| parameter(AnyParameterRef::NonVariadic(param), "")),
    );
    if let Some(param) = &params.kwarg {
        signature.push(parameter(AnyParameterRef::Variadic(param), "**"));
    }
    let doc = function.body.first().and_then(|statement| match statement {
        Stmt::Expr(expr) => match expr.value.as_ref() {
            Expr::StringLiteral(literal) => Some(literal.value.to_str()),
            _ => None,
        },
        _ => None,
    });
    let declaration = format!(
        "from typing import Any as {prefix}Any, Protocol as {prefix}Protocol, Literal as {prefix}Literal\nclass {prefix}Call({prefix}Protocol):\n    def __call__({}) -> _Result:\n        {}\n        ...\n_call: {prefix}Call\n",
        signature.join(", "),
        serde_json::to_string(doc.unwrap_or("")).unwrap()
    );
    json!({ "declaration": declaration, "probes": probes, "probeSource": probe_source, "resultProbe": result_probe }).to_string()
}

/// Keep the annotation and imports from a fresh ty-annotated function, excluding
/// its body and probe target. Callers isolate each result's import namespace.
#[wasm_bindgen(js_name = returnTypeDeclaration)]
pub fn return_type_declaration(source: &str) -> String {
    let parsed = parse_unchecked_source(source, PySourceType::Python);
    let mut imports = String::new();
    let mut annotation = None;
    let mut imported_names = std::collections::BTreeMap::new();
    for statement in &parsed.syntax().body {
        match statement {
            Stmt::Import(_) => {
                imports.push_str(&source[statement.range()]);
                imports.push('\n');
            }
            Stmt::ImportFrom(import) => {
                for alias in &import.names {
                    let name = alias
                        .asname
                        .as_ref()
                        .map_or(alias.name.as_str(), |name| name.as_str());
                    imported_names
                        .insert(name, import.module.as_ref().map(|module| module.as_str()));
                }
                let aliases: Vec<_> = import
                    .names
                    .iter()
                    .filter(|alias| {
                        alias
                            .asname
                            .as_ref()
                            .is_none_or(|name| name != "_anvil_target")
                    })
                    .map(|alias| &source[alias.range()])
                    .collect();
                if !aliases.is_empty() {
                    imports.push_str(&format!(
                        "from {}{} import {}\n",
                        ".".repeat(import.level as usize),
                        import.module.as_ref().map_or("", |name| name.as_str()),
                        aliases.join(", ")
                    ));
                }
            }
            Stmt::FunctionDef(function) if function.name.as_str() == "_anvil_result" => {
                annotation = function.returns.as_deref();
            }
            _ => {}
        }
    }
    let dictionary = matches!(annotation, Some(Expr::Subscript(subscript)) if matches!(subscript.value.as_ref(), Expr::Name(name) if name.id == "dict"));
    let annotation_module = match annotation {
        Some(Expr::Name(name)) => imported_names.get(name.id.as_str()).copied().flatten(),
        _ => None,
    }
    .map(str::to_owned);
    let source = match annotation {
        Some(annotation) => format!(
            "{imports}\n_Result: _AnvilTypeAlias = {}\n",
            &source[annotation.range()]
        ),
        None => "from typing import Any, TypeAlias\n_Result: TypeAlias = Any\n".into(),
    };
    // The same module name can refer to different client and server sources.
    // Supply import positions so the worker can compare their ty definitions.
    let parsed = parse_unchecked_source(&source, PySourceType::Stub);
    let positions = Positions::new(&source);
    let imports: Vec<_> = parsed
        .syntax()
        .body
        .iter()
        .flat_map(|statement| match statement {
            Stmt::Import(import) => import.names.as_slice(),
            Stmt::ImportFrom(import) => import.names.as_slice(),
            _ => &[],
        })
        .map(|alias| positions.at(alias.name.end() - ruff_text_size::TextSize::new(1)))
        .collect();
    json!({ "source": source, "imports": imports, "dictionary": dictionary, "annotationModule": annotation_module }).to_string()
}

#[derive(Deserialize)]
struct Registration {
    name: String,
    kind: String,
    module: String,
}

/// Specialise literal RPC names while retaining the documented broad fallback
/// for dynamic names and the usual positional/keyword argument contract.
#[wasm_bindgen(js_name = rpcServerStub)]
pub fn rpc_server_stub(source: &str, registrations: &str) -> Result<String, JsError> {
    let registrations: Vec<Registration> = serde_json::from_str(registrations)?;
    let parsed = parse_unchecked_source(source, PySourceType::Stub);
    let mut replacements = Vec::new();
    let mut imports = String::new();
    for (index, registration) in registrations.iter().enumerate() {
        imports.push_str(&format!(
            "from {} import _Result as _AnvilRpcResult{index}\n",
            registration.module
        ));
    }
    for statement in &parsed.syntax().body {
        let Stmt::FunctionDef(function) = statement else {
            continue;
        };
        let (kind, parameter, task) = match function.name.as_str() {
            "call" | "call_s" => ("callable", "fn_name", false),
            "launch_background_task" => ("background_task", "task_name", true),
            _ => continue,
        };
        let mut overloads = String::new();
        for (index, registration) in registrations.iter().enumerate() {
            if registration.kind != kind {
                continue;
            }
            let result = format!("_AnvilRpcResult{index}");
            let result = if task {
                format!("BackgroundTaskState[{result}]")
            } else {
                result
            };
            overloads.push_str(&format!(
                "@overload\ndef {}({parameter}: Literal[{}], /, *args: Any, **kwargs: Any) -> {result}: ...\n",
                function.name, serde_json::to_string(&registration.name)?
            ));
        }
        if !overloads.is_empty() {
            overloads.push_str("@overload\n");
            overloads.push_str(&source[statement.range()]);
            replacements.push((statement.range(), overloads));
        }
    }
    let mut result = source.to_owned();
    for (range, replacement) in replacements.into_iter().rev() {
        result.replace_range(std::ops::Range::<usize>::from(range), &replacement);
    }
    Ok(format!("{imports}{result}"))
}
