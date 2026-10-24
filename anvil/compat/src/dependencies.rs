use std::path::PathBuf;

pub struct Dependency {
    pub root: PathBuf,
    pub package: String,
    pub ids: Vec<String>,
}

/// Select declared apps from sorted cache entries using the baseline two-pass policy.
pub fn select(
    config: &serde_json::Value,
    cached: Vec<Dependency>,
) -> anyhow::Result<Vec<Dependency>> {
    let Some(declared) = config["dependencies"]
        .as_array()
        .filter(|items| !items.is_empty())
    else {
        return Ok(Vec::new());
    };
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
            anyhow::ensure!(
                crate::identifier(&dependency.package),
                "dependency package_name must be a Python identifier"
            );
            Ok(dependency)
        })
        .collect()
}
