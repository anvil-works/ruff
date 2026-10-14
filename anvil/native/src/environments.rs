//! Supplement ty's environment discovery with CPython's Unix user-site layout.
use ruff_db::system::{System, SystemPathBuf};
use ty_site_packages::PythonEnvironment;

pub fn user_site(system: &dyn System) -> Option<SystemPathBuf> {
    if !cfg!(unix)
        || system
            .env_var("PYTHONNOUSERSITE")
            .is_ok_and(|value| !value.is_empty())
    {
        return None;
    }
    let environment = PythonEnvironment::discover(None, system).ok()??;
    // Ordinary virtual environments disable the user site. Environments that
    // opt into system/user packages need separate coverage before enabling it.
    if environment.is_virtual() {
        return None;
    }
    let version = environment
        .site_packages_paths(system)
        .ok()?
        .python_version_from_layout()?
        .version;
    let framework = if cfg!(target_os = "macos") {
        environment
            .sys_prefix()
            .components()
            .find_map(|component| component.as_str().strip_suffix(".framework"))
    } else {
        None
    };
    // CPython site.py uses the framework scheme on macOS and the Unix scheme
    // otherwise. The host interpreter version, rather than the typing target,
    // determines its library directories. PYTHONUSERBASE overrides only the base.
    let base = if let Ok(base) = system.env_var("PYTHONUSERBASE")
        && !base.is_empty()
    {
        SystemPathBuf::from(base)
    } else {
        let home = SystemPathBuf::from(system.env_var("HOME").ok()?);
        if let Some(framework) = framework {
            home.join("Library")
                .join(framework)
                .join(version.to_string())
        } else {
            home.join(".local")
        }
    };
    let path = if framework.is_some() {
        base.join("lib/python/site-packages")
    } else {
        base.join(format!("lib/python{version}/site-packages"))
    };
    system.is_directory(&path).then_some(path)
}
