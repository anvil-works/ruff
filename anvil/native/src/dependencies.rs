//! Resolve declared apps from the local cache, following anvil-pyright's two passes.
use std::path::{Path, PathBuf};

use anyhow::{Result, ensure};
use serde_json::Value;

pub(crate) struct Dependency {
    pub(crate) root: PathBuf,
    pub(crate) package: String,
    pub(crate) ids: Vec<String>,
}

pub(crate) fn resolve(app: &Path, config: &Value) -> Result<Vec<Dependency>> {
    let Some(declared) = config["dependencies"]
        .as_array()
        .filter(|items| !items.is_empty())
    else {
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
    let mut used = vec![false; cached.len()];
    let mut matched = Vec::new();
    let mut legacy = Vec::new();
    for dependency in declared {
        let hint = dependency["resolution_hints"]["package_name"].as_str();
        let index = hint.and_then(|hint| {
            // The baseline's lookup maps retain the last duplicate package name.
            cached
                .iter()
                .rposition(|item| item.package == hint)
                .filter(|index| !used[*index])
                .or_else(|| {
                    cached
                        .iter()
                        .position(|item| item.root.file_name().is_some_and(|name| name == hint))
                        .filter(|index| !used[*index])
                })
        });
        if let Some(index) = index {
            used[index] = true;
            matched.push((index, dependency));
        } else {
            legacy.push(dependency);
        }
    }
    for dependency in legacy {
        if let Some(index) = used.iter().position(|used| !used) {
            used[index] = true;
            matched.push((index, dependency));
        }
    }
    let mut cached: Vec<_> = cached.into_iter().map(Some).collect();
    matched
        .into_iter()
        .map(|(index, declared)| {
            let mut dependency = cached[index]
                .take()
                .expect("each cache entry is consumed once");
            dependency.ids = ["dep_id", "app_id"]
                .into_iter()
                .filter_map(|key| declared[key].as_str().map(str::to_owned))
                .collect();
            ensure!(
                crate::identifier(&dependency.package),
                "dependency package_name must be a Python identifier"
            );
            Ok(dependency)
        })
        .collect()
}
