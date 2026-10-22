use std::env;
use std::fs;
use std::path::PathBuf;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let root = PathBuf::from(env::var("CARGO_MANIFEST_DIR")?).join("../api-stubs");
    let mut paths = walkdir::WalkDir::new(&root)
        .into_iter()
        .collect::<Result<Vec<_>, _>>()?;
    paths.sort_by_key(|entry| entry.path().to_path_buf());
    let mut source = String::from("const API_STUBS: &[(&str, &str)] = &[\n");
    for entry in paths {
        if entry.file_type().is_file() && entry.path().extension().is_some_and(|ext| ext == "pyi") {
            let relative = entry
                .path()
                .strip_prefix(&root)?
                .to_string_lossy()
                .replace('\\', "/");
            // Only the discoverable package root belongs in the eager API set.
            // The browser fetches the Plotly catalogue from its separate asset.
            if relative.starts_with("client/plotly/") && relative != "client/plotly/__init__.pyi" {
                continue;
            }
            source.push_str(&format!(
                "({relative:?}, include_str!({:?})),\n",
                entry.path().canonicalize()?
            ));
        }
    }
    source.push_str("];\n");
    fs::write(
        PathBuf::from(env::var("OUT_DIR")?).join("api_stubs.rs"),
        source,
    )?;
    println!("cargo:rerun-if-changed={}", root.display());
    Ok(())
}
