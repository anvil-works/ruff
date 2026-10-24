//! Select curated typing snapshots from app requirements, without installing code.
use pep440_rs::{Operator, Version, VersionSpecifiers};
use serde::Deserialize;
use std::collections::{BTreeMap, BTreeSet};
use wasm_bindgen::prelude::*;

#[derive(Deserialize)]
struct Package {
    id: String,
    version: Version,
    url: String,
    #[serde(default)]
    dependencies: Vec<String>,
}

#[wasm_bindgen(js_name = serverPackages)]
pub fn server_packages(requirements: &str, packages: &str) -> Result<String, JsValue> {
    let lines: Vec<_> = requirements
        .lines()
        .map(|line| {
            let line = line.trim();
            if line.starts_with('#') {
                ""
            } else if let Some((before, _)) = line.split_once('#')
                && before.chars().next_back().is_some_and(char::is_whitespace)
            {
                before.trim_end()
            } else {
                line
            }
        })
        .filter(|line| !line.is_empty())
        .collect();
    // Includes, constraints and continuation lines can change a named package's
    // meaning. Wait for resolved metadata instead of choosing from partial input.
    if lines.iter().any(|line| {
        let option = line
            .split(|c: char| c.is_whitespace() || c == '=')
            .next()
            .unwrap_or_default();
        // Registry mirrors do not constrain the installed package versions.
        let unresolved_option =
            line.starts_with('-') && !matches!(option, "--index-url" | "--extra-index-url" | "-i");
        unresolved_option || line.ends_with('\\')
    }) {
        return Ok("[]".to_owned());
    }
    let packages: Vec<Package> =
        serde_json::from_str(packages).map_err(|error| JsValue::from_str(&error.to_string()))?;
    let requirements: Vec<_> = lines
        .into_iter()
        .filter_map(|line| {
            let name_end = line
                .find(|c: char| !c.is_ascii_alphanumeric() && !matches!(c, '-' | '_' | '.'))
                .unwrap_or(line.len());
            let name = line[..name_end].to_ascii_lowercase();
            if !packages.iter().any(|package| package.id == name) {
                return None;
            }
            let mut specifier = line[name_end..].trim();
            if let Some(extras) = specifier.strip_prefix('[') {
                specifier = extras.split_once(']').map_or("?", |(_, rest)| rest.trim());
            }
            if let Some(parenthesised) = specifier
                .strip_prefix('(')
                .and_then(|value| value.strip_suffix(')'))
            {
                specifier = parenthesised.trim();
            }
            // Accept named requirements and PEP 440 specifiers only. Markers,
            // URLs and pip directives need resolved installation metadata; keep
            // known names with invalid specifiers so dependencies cannot bypass them.
            let versions = specifier.parse::<VersionSpecifiers>().ok();
            Some((name, versions))
        })
        .collect();
    // Select one immutable artifact per library, preferring an admitted version
    // before SemVer approximation. Exact pins establish the runtime version;
    // broad ranges do not justify using declarations older than their minimum.
    let mut candidates: BTreeMap<&str, (bool, &Package)> = BTreeMap::new();
    for package in &packages {
        let Some(admitted) = match_requirement(package, &requirements) else {
            continue;
        };
        if candidates
            .get(package.id.as_str())
            .is_none_or(|(previous_admitted, previous)| {
                (admitted, &package.version) > (*previous_admitted, &previous.version)
            })
        {
            candidates.insert(&package.id, (admitted, package));
        }
    }
    let mut selected = BTreeSet::new();
    for (_, package) in candidates.values() {
        if !requirements.iter().any(|(name, _)| name == &package.id) {
            continue;
        }
        let mut pending = vec![*package];
        let mut dependencies = BTreeSet::new();
        let mut complete = true;
        while let Some(package) = pending.pop() {
            if !dependencies.insert(&package.url) {
                continue;
            }
            for id in &package.dependencies {
                if let Some((_, dependency)) = candidates.get(id.as_str()) {
                    pending.push(dependency);
                } else {
                    complete = false;
                }
            }
        }
        if complete {
            selected.extend(dependencies);
        }
    }
    serde_json::to_string(&selected).map_err(|error| JsValue::from_str(&error.to_string()))
}

/// `Some(true)` admits the snapshot directly; `Some(false)` is an approximation.
fn match_requirement(
    package: &Package,
    requirements: &[(String, Option<VersionSpecifiers>)],
) -> Option<bool> {
    let constraints: Vec<_> = requirements
        .iter()
        .filter(|(name, _)| name == &package.id)
        .map(|(_, versions)| versions.as_ref())
        .collect::<Option<_>>()?;
    if constraints
        .iter()
        .all(|versions| versions.contains(&package.version))
    {
        return Some(true);
    }
    let runtime = constraints
        .iter()
        .flat_map(|versions| versions.iter())
        .find(|specifier| *specifier.operator() == Operator::Equal)?
        .version();
    if !constraints
        .iter()
        .all(|versions| versions.contains(runtime))
        || [runtime, &package.version].iter().any(|version| {
            !version.is_stable() || version.is_post() || version.is_local() || version.epoch() != 0
        })
    {
        return None;
    }
    let [major, minor, ..] = runtime.release() else {
        return None;
    };
    let [stub_major, stub_minor, ..] = package.version.release() else {
        return None;
    };
    (*major == *stub_major && stub_minor <= minor && (*major != 0 || minor == stub_minor))
        .then_some(false)
}
