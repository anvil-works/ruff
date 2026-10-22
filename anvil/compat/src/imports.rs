use std::path::Path;

/// Convert a relative source path to a Python module name, accepting either OS separator.
pub fn module_name(package: &str, relative: &Path) -> String {
    let module = relative
        .with_extension("")
        .to_string_lossy()
        .replace(['/', '\\'], ".");
    let module = module.strip_suffix(".__init__").unwrap_or(&module);
    if module == "__init__" {
        package.to_owned()
    } else {
        format!("{package}.{module}")
    }
}
