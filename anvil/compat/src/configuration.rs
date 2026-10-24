//! Decode the app's TOML; upstream Ty remains responsible for option validation.
use serde_json::{Value, json};
use wasm_bindgen::prelude::*;

#[wasm_bindgen(js_name = tyConfiguration)]
pub fn ty_configuration(source: &str, pyproject: bool) -> Result<String, JsValue> {
    let value: Value =
        toml::from_str(source).map_err(|error| JsValue::from_str(&error.to_string()))?;
    let options = if pyproject {
        value.get("tool").and_then(|tool| tool.get("ty"))
    } else {
        Some(&value)
    };
    serde_json::to_string(options.unwrap_or(&json!({})))
        .map_err(|error| JsValue::from_str(&error.to_string()))
}
