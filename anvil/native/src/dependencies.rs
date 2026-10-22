//! Resolve declared apps from the local cache, following anvil-pyright's two passes.
use std::path::Path;

use anyhow::Result;
use serde_json::Value;

pub(crate) use anvil_ty_compat::dependencies::Dependency;

pub(crate) fn resolve(app: &Path, config: &Value) -> Result<Vec<Dependency>> {
    if config["dependencies"]
        .as_array()
        .filter(|items| !items.is_empty())
        .is_none()
    {
        return Ok(Vec::new());
    };
    let Ok(entries) = std::fs::read_dir(app.join(".anvil/deps")) else {
        return Ok(Vec::new());
    };
    let mut roots: Vec<_> = entries
        .filter_map(Result::ok)
        .map(|entry| entry.path())
        .collect();
    roots.sort();
    let cached: Vec<_> = roots
        .into_iter()
        .filter_map(|root| {
            let config = crate::yaml(&root.join("anvil.yaml")).ok()?;
            let package = config["package_name"].as_str()?.to_owned();
            Some(Dependency {
                root,
                package,
                ids: Vec::new(),
            })
        })
        .collect();
    anvil_ty_compat::dependencies::select(config, cached)
}
