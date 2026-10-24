//! Project structure need not be rebuilt for an ordinary Python body edit.
use crate::{Source, forms, models};
use serde::Deserialize;
use serde_json::{Value, json};
use wasm_bindgen::prelude::*;

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct Update {
    before: String,
    after: String,
    schema: Value,
    form_class: Option<String>,
}

fn model_declarations(source: &str) -> models::Registry {
    let source = Source {
        path: "source.py".into(),
        relative: "source.py".into(),
        text: source.to_owned(),
    };
    let mut models = models::Registry::default();
    models.collect(&[source], &[], "SourceUpdate");
    models
}

/// None requests full preparation because exported metadata might have changed.
/// Both projections use the same transformations as full app preparation.
#[wasm_bindgen(js_name = sourceUpdate)]
pub fn source_update(input: &str) -> Result<Option<String>, JsValue> {
    let update: Update =
        serde_json::from_str(input).map_err(|error| JsValue::from_str(&error.to_string()))?;
    if model_declarations(&update.before) != model_declarations(&update.after)
        || update.form_class.as_deref().is_some_and(|name| {
            forms::defined_members(&update.before, name)
                != forms::defined_members(&update.after, name)
        })
    {
        return Ok(None);
    }
    Ok(Some(
        json!({
            "before": models::analysis_source(&update.before, &update.schema),
            "after": models::analysis_source(&update.after, &update.schema),
        })
        .to_string(),
    ))
}
