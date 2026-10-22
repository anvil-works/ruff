//! Anvil declarations shared by the native checker and browser preparation.
use serde_json::Value;
use std::path::PathBuf;

pub mod dependencies;
pub mod dom;
pub mod forms;
pub mod imports;
pub mod models;
pub mod services;
pub mod skulpt;
pub mod tables;
pub struct Source {
    pub path: PathBuf,
    pub relative: PathBuf,
    pub text: String,
}

pub fn identifier(value: &str) -> bool {
    let mut chars = value.chars();
    chars
        .next()
        .is_some_and(|c| c == '_' || c.is_ascii_alphabetic())
        && chars.all(|c| c == '_' || c.is_ascii_alphanumeric())
}

pub fn populated(value: &Value) -> bool {
    match value {
        Value::Null => false,
        Value::Array(items) => !items.is_empty(),
        Value::Object(items) => !items.is_empty(),
        Value::Bool(value) => *value,
        _ => true,
    }
}

#[cfg(feature = "browser")]
mod browser;

#[cfg(feature = "browser")]
mod symbols;

#[cfg(feature = "browser")]
mod item_metadata;

#[cfg(feature = "browser")]
mod positions;

#[cfg(feature = "browser")]
mod js_components;

#[cfg(feature = "browser")]
mod api_calls;

#[cfg(feature = "browser")]
mod rename_names;

#[cfg(feature = "browser")]
mod rpc_types;

#[cfg(feature = "browser")]
mod item_assignments;

mod literal_options;

#[cfg(feature = "browser")]
mod source_imports;

#[cfg(feature = "browser")]
mod source_updates;

#[cfg(feature = "browser")]
mod server_packages;

#[cfg(feature = "browser")]
mod configuration;
