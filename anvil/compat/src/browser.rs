//! Prepare declarations from in-memory app data using the native checker's renderer.
use std::collections::{BTreeMap, HashSet};
use std::path::{Path, PathBuf};

use anyhow::{Context, Result};
use serde_json::{Value, json};
use wasm_bindgen::prelude::*;

use crate::forms::{RenderedForm, TemplateContext, class_name, parse_template, render};
use crate::{Source, dependencies, js_components, models, tables};

include!(concat!(env!("OUT_DIR"), "/api_stubs.rs"));

/// IDE-resolved cache roots and logical dependency IDs mapped to those roots.
/// The IDE server has already selected direct and transitive dependencies.
#[derive(serde::Deserialize)]
struct ResolvedDependencies {
    roots: Vec<String>,
    ids: BTreeMap<String, String>,
}

fn python_sources(files: &BTreeMap<String, String>, root: &str) -> Vec<Source> {
    files
        .iter()
        .filter_map(|(path, text)| {
            let relative = path.strip_prefix(&format!("{root}/"))?;
            (relative.ends_with(".py") || relative.ends_with(".pyi")).then(|| Source {
                path: path.into(),
                relative: relative.into(),
                text: text.clone(),
            })
        })
        .collect()
}

#[derive(Default)]
struct CachedModels {
    code: String,
    package: String,
    models: models::Registry,
}

#[derive(Clone)]
struct CachedForm {
    template: String,
    data: Value,
    code: String,
    rendered: RenderedForm,
    class_name: String,
}

#[derive(PartialEq, Eq)]
struct FormContext {
    apps: Vec<(String, Value)>,
    dependency_roots: BTreeMap<String, BTreeMap<String, String>>,
    paths: Vec<String>,
    models: BTreeMap<String, models::Registry>,
    inferred_items: BTreeMap<String, String>,
}

/// One worker owns this preparation cache alongside its ty workspace. Cache only
/// pure Anvil declarations; ty remains responsible for incremental Python types.
#[wasm_bindgen]
#[derive(Default)]
pub struct Preparation {
    models: BTreeMap<PathBuf, CachedModels>,
    forms: BTreeMap<String, CachedForm>,
    form_context: Option<FormContext>,
}

#[wasm_bindgen]
impl Preparation {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        Self::default()
    }

    pub fn prepare(
        &mut self,
        root: &str,
        files_json: &str,
        is_server: bool,
        inferred_items: &str,
    ) -> Result<String, JsValue> {
        self.prepare_files(root, files_json, is_server, inferred_items)
            .map_err(|error| JsValue::from_str(&format!("{error:#}")))
    }
}

impl Preparation {
    fn model_registry(
        &mut self,
        files: &BTreeMap<String, String>,
        root: &str,
        package: &str,
    ) -> models::Registry {
        self.models
            .retain(|path, _| path.to_str().is_some_and(|path| files.contains_key(path)));
        let client = python_sources(files, &format!("{root}/client_code"));
        let server = python_sources(files, &format!("{root}/server_code"));
        let server_modules: HashSet<_> = server
            .iter()
            .map(|source| crate::imports::module_name(package, &source.relative))
            .collect();
        let mut models = models::Registry::default();
        for (source, is_server) in client
            .iter()
            .map(|source| (source, false))
            .chain(server.iter().map(|source| (source, true)))
        {
            let entry = self.models.entry(source.path.clone()).or_default();
            if entry.code != source.text || entry.package != package {
                let mut discovered = models::Registry::default();
                discovered.collect(std::slice::from_ref(source), &[], package);
                *entry = CachedModels {
                    code: source.text.clone(),
                    package: package.to_owned(),
                    models: discovered,
                };
            }
            if !is_server {
                models.client.extend(entry.models.client.clone());
            }
            if is_server
                || !server_modules.contains(&crate::imports::module_name(package, &source.relative))
            {
                models.server.extend(entry.models.server.clone());
            }
        }
        models
    }

    fn prepare_files(
        &mut self,
        root: &str,
        files_json: &str,
        is_server: bool,
        inferred_items: &str,
    ) -> Result<String> {
        let files: BTreeMap<String, String> = serde_json::from_str(files_json)?;
        let inferred_items: BTreeMap<String, String> = serde_json::from_str(inferred_items)?;
        self.forms.retain(|path, _| files.contains_key(path));
        let Some(config) = files.get(&format!("{root}/anvil.yaml")) else {
            return Ok(json!({ "files": {}, "roots": [root], "contextRoot": root }).to_string());
        };
        let mut apps = vec![(root.to_owned(), serde_yaml::from_str::<Value>(config)?)];
        let mut cached = Vec::new();
        let mut cached_configs = BTreeMap::new();
        for (path, text) in &files {
            if let Some(relative) = path.strip_prefix(&format!("{root}/.anvil/deps/"))
                && let Some(id) = relative.strip_suffix("/anvil.yaml")
                && !id.contains('/')
                && let Ok(config) = serde_yaml::from_str::<Value>(text)
                && let Some(package) = config["package_name"].as_str()
            {
                let app = format!("{root}/.anvil/deps/{id}");
                cached.push(dependencies::Dependency {
                    root: app.clone().into(),
                    package: package.to_owned(),
                    ids: Vec::new(),
                });
                cached_configs.insert(app, config);
            }
        }
        let resolved = files
            .get(&format!("{root}/.anvil/dependencies.json"))
            .map(|text| serde_json::from_str::<ResolvedDependencies>(text))
            .transpose()?;
        let dependencies = if let Some(resolved) = &resolved {
            let mut cached: BTreeMap<_, _> = cached
                .into_iter()
                .map(|dependency| (dependency.root.to_string_lossy().into_owned(), dependency))
                .collect();
            resolved
                .roots
                .iter()
                .map(|root| {
                    let mut dependency = cached
                        .remove(root)
                        .with_context(|| format!("selected dependency is unavailable: {root}"))?;
                    dependency.ids = resolved
                        .ids
                        .iter()
                        .filter(|(_, target)| *target == root)
                        .map(|(id, _)| id.clone())
                        .collect();
                    Ok(dependency)
                })
                .collect::<Result<Vec<_>>>()?
        } else {
            dependencies::select(&apps[0].1, cached)?
        };
        for dependency in &dependencies {
            let app = dependency.root.to_string_lossy().into_owned();
            let config = cached_configs
                .remove(&app)
                .context("selected dependency config is missing")?;
            apps.push((app, config));
        }
        // Keep logical dependency names with their owning app. Designer Form
        // specifications use these IDs, which need not match cache directories.
        let mut dependency_roots = BTreeMap::new();
        for (app, config) in &apps {
            if resolved.is_some() {
                let ids: BTreeMap<_, _> = dependencies
                    .iter()
                    .flat_map(|dependency| {
                        dependency
                            .ids
                            .iter()
                            .map(|id| (id.clone(), dependency.root.to_string_lossy().into_owned()))
                    })
                    .collect();
                dependency_roots.insert(app.clone(), ids);
                continue;
            }
            let mut cached: Vec<_> = apps
                .iter()
                .skip(1)
                .filter(|(path, _)| path != app)
                .map(|(path, config)| dependencies::Dependency {
                    root: path.into(),
                    package: config["package_name"]
                        .as_str()
                        .unwrap_or("main_app_package")
                        .to_owned(),
                    ids: Vec::new(),
                })
                .collect();
            cached.sort_by(|left, right| left.root.cmp(&right.root));
            let mut ids = BTreeMap::new();
            for dependency in dependencies::select(config, cached)? {
                for id in dependency.ids {
                    ids.insert(id, dependency.root.to_string_lossy().into_owned());
                }
            }
            dependency_roots.insert(app.clone(), ids);
        }
        let environment = if is_server { "server" } else { "client" };
        let api_root = format!("{root}/.anvil/types/{environment}");
        let api = API_STUBS
            .iter()
            .find(|(path, _)| *path == "client/anvil/__init__.pyi")
            .map(|(_, text)| *text)
            .context("bundled client Anvil API is missing")?;
        let analysis_root = format!("{root}/.anvil/analysis/{environment}");
        let context_root = format!(
            "{analysis_root}/{}",
            apps[0].1["package_name"]
                .as_str()
                .unwrap_or("main_app_package")
        );
        let mut sources = BTreeMap::new();
        // Unselected cache entries must not contribute importable files or references.
        let mut excluded_sources: Vec<_> = files
            .keys()
            .filter(|path| {
                path.starts_with(&format!("{root}/.anvil/deps/"))
                    && (path.ends_with(".py") || path.ends_with(".pyi"))
            })
            .cloned()
            .collect();
        let mut source_environments = BTreeMap::new();
        let mut projected = BTreeMap::new();
        let mut diagnostics = Vec::new();
        let mut form_classes = BTreeMap::new();
        let mut handler_types = BTreeMap::new();
        let mut forms = Vec::new();
        let main_models = if crate::populated(&apps[0].1["db_schema"]) {
            self.model_registry(
                &files,
                root,
                apps[0].1["package_name"]
                    .as_str()
                    .unwrap_or("main_app_package"),
            )
        } else {
            self.models.clear();
            models::Registry::default()
        };
        let mut form_models = BTreeMap::from([(root.to_owned(), main_models.clone())]);
        for (app, config) in apps.iter().skip(1) {
            form_models.insert(
                app.clone(),
                self.model_registry(
                    &files,
                    app,
                    config["package_name"]
                        .as_str()
                        .unwrap_or("main_app_package"),
                ),
            );
        }
        let packages: BTreeMap<_, _> = apps
            .iter()
            .map(|(app, config)| {
                (
                    config["package_name"]
                        .as_str()
                        .unwrap_or("main_app_package")
                        .to_owned(),
                    format!("{app}/client_code"),
                )
            })
            .collect();
        let js_metadata: Value = files
            .get(&format!("{root}/.anvil/js-components.json"))
            .map(|text| serde_json::from_str(text))
            .transpose()?
            .unwrap_or_default();
        let js = js_components::declarations(&js_metadata, &packages);
        let js_modules: HashSet<_> = js
            .exports
            .keys()
            .map(|module| {
                let (package, relative) = module
                    .split_once('/')
                    .unwrap_or((module.as_str(), "__init__"));
                format!("{}/{}.py", packages[package], relative)
            })
            .collect();
        // Source bodies affect only their own Form. Changes to available modules,
        // app configuration, dependency IDs or row-model identities can affect any
        // Form's imports.
        let context = FormContext {
            apps: apps.clone(),
            dependency_roots: dependency_roots.clone(),
            paths: files
                .keys()
                .filter(|path| path.ends_with(".py") || path.ends_with(".pyi"))
                .cloned()
                .chain(js_modules.iter().cloned())
                .collect::<std::collections::BTreeSet<_>>()
                .into_iter()
                .collect(),
            models: form_models.clone(),
            inferred_items: inferred_items.clone(),
        };
        if self.form_context.as_ref() != Some(&context) {
            self.forms.clear();
            self.form_context = Some(context);
        }
        for (path, text) in API_STUBS {
            if let Some(path) = path.strip_prefix(&format!("{environment}/")) {
                let text = match path {
                    "anvil/tables/__init__.pyi" => {
                        tables::stub(&apps[0].1["db_schema"], text, &main_models, environment)?
                    }
                    "anvil/users/__init__.pyi" => {
                        crate::services::users(&apps[0].1, text, &main_models, environment)?
                    }
                    "anvil/google/drive.pyi" => crate::services::drive(&apps[0].1, text)?,
                    _ => None,
                }
                .unwrap_or_else(|| (*text).to_owned());
                projected.insert(format!("{api_root}/{path}"), text);
            }
        }
        let mut component_api = None;
        for (app, config) in &apps {
            let package = config["package_name"]
                .as_str()
                .unwrap_or("main_app_package");
            let client = format!("{app}/client_code");
            let models = &form_models[app];
            let mut generated = BTreeMap::<String, String>::new();
            for (path, text) in &files {
                if !path.starts_with(&format!("{client}/")) {
                    continue;
                }
                let template_path = Path::new(path);
                let Some(format @ ("yaml" | "html")) =
                    template_path.extension().and_then(|ext| ext.to_str())
                else {
                    continue;
                };
                if format == "html"
                    && files.contains_key(
                        &template_path
                            .with_extension("yaml")
                            .to_string_lossy()
                            .into_owned(),
                    )
                {
                    continue;
                }
                let directory = template_path
                    .parent()
                    .context("template needs a directory")?;
                let source = if template_path.file_name().is_some_and(|name| {
                    name == "form_template.yaml" || name == "form_template.html"
                }) {
                    directory.join("__init__.py")
                } else {
                    template_path.with_extension("py")
                };
                let Some(code) = files.get(source.to_str().context("invalid source path")?) else {
                    continue;
                };
                let stem = if source.file_name().is_some_and(|name| name == "__init__.py") {
                    directory.file_name()
                } else {
                    source.file_stem()
                };
                let name = stem
                    .and_then(|name| name.to_str())
                    .context("Form needs a name")?;
                let exists = |path: &Path| {
                    path.to_str()
                        .is_some_and(|path| files.contains_key(path) || js_modules.contains(path))
                };
                let rendered = (|| -> Result<_> {
                    if let Some(cached) = self
                        .forms
                        .get(path)
                        .filter(|cached| cached.template == *text && cached.code == *code)
                    {
                        return Ok(cached.clone());
                    }
                    let template = parse_template(text, format == "html")?;
                    let rendered = render(
                        &template,
                        TemplateContext {
                            root: Path::new(&client),
                            package,
                            name,
                            api: component_api
                                .get_or_insert_with(|| crate::forms::ComponentApi::parse(api)),
                            code,
                            models,
                            dependencies: &dependencies,
                            exists: &exists,
                            inferred_item_type: inferred_items
                                .get(source.to_str().context("invalid source path")?)
                                .map(String::as_str),
                        },
                    )?;
                    let cached = CachedForm {
                        template: text.clone(),
                        data: template.clone(),
                        code: code.clone(),
                        rendered,
                        class_name: class_name(&template, name).to_owned(),
                    };
                    self.forms.insert(path.clone(), cached.clone());
                    Ok(cached)
                })();
                let stub = match rendered {
                    Ok(cached) => {
                        let relative = source.strip_prefix(&client)?.to_string_lossy();
                        let local_name = relative
                            .strip_suffix("/__init__.py")
                            .or_else(|| relative.strip_suffix(".py"))
                            .unwrap_or(&relative)
                            .replace('/', ".");
                        forms.push(json!({ "root": app, "name": local_name, "path": source, "data": cached.data }));
                        handler_types.insert(
                            source.to_string_lossy().into_owned(),
                            cached.rendered.handler_types,
                        );
                        form_classes
                            .insert(source.to_string_lossy().into_owned(), cached.class_name);
                        cached.rendered.stub
                    }
                    Err(error) => {
                        diagnostics.push(json!({
                            "file": source,
                            "code": "invalid-form-template",
                            "message": format!("Cannot prepare {path}: {error:#}"),
                        }));
                        // Match native preparation: keep checking Python and permit a
                        // later metadata update to replace this fallback declaration.
                        format!("from typing import Any\n{name}Template = Any\n")
                    }
                };
                let stub_path = directory
                    .join("_anvil_designer.pyi")
                    .to_string_lossy()
                    .into_owned();
                generated
                    .entry(stub_path)
                    .or_default()
                    .push_str(&format!("{stub}\n"));
            }
            // Give every Python definition one canonical package identity. Queries and
            // edits are mapped back to the untouched original paths by the worker.
            let package_root = format!("{analysis_root}/{package}");
            let candidates = [
                ("client_code", python_sources(&files, &client)),
                (
                    "server_code",
                    python_sources(&files, &format!("{app}/server_code")),
                ),
            ];
            let server_modules: HashSet<_> = candidates[1]
                .1
                .iter()
                .map(|source| crate::imports::module_name(package, &source.relative))
                .collect();
            for (kind, candidates) in candidates {
                for source in candidates {
                    excluded_sources.push(source.path.to_string_lossy().into_owned());
                    source_environments.insert(source.path.clone(), kind == "server_code");
                    // The runtime chooses server modules before client modules,
                    // including a server .py that shadows a client package.
                    let shadowed = is_server
                        && kind == "client_code"
                        && server_modules
                            .contains(&crate::imports::module_name(package, &source.relative));
                    if (kind == "client_code" || is_server) && !shadowed {
                        let canonical = format!("{package_root}/{}", source.relative.display());
                        sources.insert(
                            canonical.clone(),
                            source.path.to_string_lossy().into_owned(),
                        );
                        projected.insert(
                            canonical,
                            models::analysis_source(&source.text, &apps[0].1["db_schema"]),
                        );
                    }
                }
            }
            for (path, text) in generated {
                let path = path.strip_prefix(&client).map_or_else(
                    || path.clone(),
                    |relative| format!("{package_root}{relative}"),
                );
                projected.insert(path, text);
            }
        }
        for (relative, text) in &js.stubs {
            projected.insert(format!("{api_root}/{relative}"), text.clone());
        }
        for (module, exports) in &js.exports {
            let path = format!("{analysis_root}/{module}");
            let path = if projected.contains_key(&format!("{path}.py")) {
                format!("{path}.py")
            } else if js.packages.contains(module)
                || projected.contains_key(&format!("{path}/__init__.py"))
            {
                format!("{path}/__init__.py")
            } else {
                format!("{path}.py")
            };
            // JS exports belong to client modules; a server module keeps precedence.
            if is_server
                && sources.get(&path).is_some_and(|original| {
                    source_environments.get(Path::new(original)) == Some(&true)
                })
            {
                continue;
            }
            let text = projected.entry(path).or_default();
            text.push('\n');
            for export in exports {
                text.push_str(export);
                text.push('\n');
            }
        }
        let mut row_types = Vec::new();
        if let Some(schema) = apps[0].1["db_schema"].as_object() {
            for (name, table) in schema {
                let python = table["python_name"].as_str().unwrap_or(name);
                let keys: Vec<_> = table["columns"]
                    .as_array()
                    .into_iter()
                    .flatten()
                    .filter_map(|column| column["name"].as_str())
                    .collect();
                row_types.push(json!({ "path": format!("{api_root}/anvil/tables/__init__.pyi"), "name": format!("_Row_{python}"), "keys": keys }));
                if let Some(model) = main_models.get(name, environment) {
                    let package = apps[0].1["package_name"]
                        .as_str()
                        .unwrap_or("main_app_package");
                    let package_root = format!("{analysis_root}/{package}/");
                    for (canonical, original) in &sources {
                        if let Some(relative) = canonical.strip_prefix(&package_root)
                            && crate::imports::module_name(package, Path::new(relative))
                                == model.module
                        {
                            row_types.push(
                                json!({ "path": original, "name": model.name, "keys": keys }),
                            );
                        }
                    }
                }
            }
        }
        Ok(json!({ "files": projected, "sources": sources, "excludedSources": excluded_sources, "sourceEnvironments": source_environments, "roots": [analysis_root, api_root], "diagnostics": diagnostics,
        "dependencyRoots": dependency_roots, "tableRows": row_types, "formClasses": form_classes, "handlerTypes": handler_types,
        "apps": apps.iter().map(|(path, config)| (path, config)).collect::<BTreeMap<_, _>>(), "forms": forms, "contextRoot": context_root }).to_string())
    }
}
