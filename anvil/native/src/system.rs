//! Read-only access to Python environments alongside generated in-memory app files.
use std::any::Any;

use ruff_db::system::walk_directory::WalkDirectoryBuilder;
use ruff_db::system::{
    DirectoryEntry, InMemorySystem, MemoryFileSystem, Metadata, OsSystem, Result, System,
    SystemPath, SystemPathBuf, SystemVirtualPath, WhichError, WhichResult, WritableSystem,
};
use ruff_notebook::{Notebook, NotebookError};

#[derive(Clone, Debug)]
pub struct ValidationSystem {
    memory: InMemorySystem,
    disk: OsSystem,
    root: SystemPathBuf,
}

impl ValidationSystem {
    pub fn new(root: SystemPathBuf) -> Self {
        Self {
            // MemoryFileSystem requires a slash-rooted cwd even on Windows.
            // Expose the native project root through System::current_directory.
            memory: InMemorySystem::default(),
            disk: OsSystem::new(&root),
            root,
        }
    }

    pub fn memory_file_system(&self) -> &MemoryFileSystem {
        self.memory.fs()
    }

    fn system_for(&self, path: &SystemPath) -> &dyn System {
        if path.starts_with(&self.root) {
            &self.memory
        } else {
            &self.disk
        }
    }
}

impl System for ValidationSystem {
    fn path_metadata(&self, path: &SystemPath) -> Result<Metadata> {
        self.system_for(path).path_metadata(path)
    }

    fn canonicalize_path(&self, path: &SystemPath) -> Result<SystemPathBuf> {
        self.system_for(path).canonicalize_path(path)
    }

    fn is_same_file(&self, first: &SystemPath, second: &SystemPath) -> Result<bool> {
        if first.starts_with(&self.root) != second.starts_with(&self.root) {
            Ok(false)
        } else {
            self.system_for(first).is_same_file(first, second)
        }
    }

    fn which(&self, name: &str) -> WhichResult {
        let path = self.disk.which(name)?;
        // Homebrew's libexec/bin symlinks make ty infer libexec as sys.prefix.
        // Resolve that facade; retain ordinary venv bin paths and their identity.
        if path
            .parent()
            .and_then(SystemPath::parent)
            .and_then(SystemPath::file_name)
            == Some("libexec")
        {
            self.disk
                .canonicalize_path(&path)
                .map_err(|_| WhichError::CannotCanonicalize)
        } else {
            Ok(path)
        }
    }

    fn env_var(&self, name: &str) -> std::result::Result<String, std::env::VarError> {
        self.disk.env_var(name)
    }

    fn read_to_string(&self, path: &SystemPath) -> Result<String> {
        self.system_for(path).read_to_string(path)
    }

    fn read_to_notebook(&self, path: &SystemPath) -> std::result::Result<Notebook, NotebookError> {
        self.system_for(path).read_to_notebook(path)
    }

    fn read_virtual_path_to_string(&self, path: &SystemVirtualPath) -> Result<String> {
        self.memory.read_virtual_path_to_string(path)
    }

    fn read_virtual_path_to_notebook(
        &self,
        path: &SystemVirtualPath,
    ) -> std::result::Result<Notebook, NotebookError> {
        self.memory.read_virtual_path_to_notebook(path)
    }

    fn current_directory(&self) -> &SystemPath {
        &self.root
    }

    fn user_config_directory(&self) -> Option<SystemPathBuf> {
        None
    }

    fn cache_dir(&self) -> Option<SystemPathBuf> {
        None
    }

    fn read_directory<'a>(
        &'a self,
        path: &SystemPath,
    ) -> Result<Box<dyn Iterator<Item = Result<DirectoryEntry>> + 'a>> {
        self.system_for(path).read_directory(path)
    }

    fn walk_directory(&self, path: &SystemPath) -> WalkDirectoryBuilder {
        self.system_for(path).walk_directory(path)
    }

    fn as_writable(&self) -> Option<&dyn WritableSystem> {
        None
    }

    fn as_any(&self) -> &dyn Any {
        self
    }

    fn as_any_mut(&mut self) -> &mut dyn Any {
        self
    }

    fn dyn_clone(&self) -> Box<dyn System> {
        Box::new(self.clone())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn native_project_root_reads_memory_and_disk() -> anyhow::Result<()> {
        let path = std::path::absolute("/anvil/system-test")?;
        let root = SystemPathBuf::from(crate::utf8(&path)?);
        let system = ValidationSystem::new(root.clone());
        let fs = system.memory_file_system();
        let file = root.join("module.py");
        fs.create_directory_all(&root)?;
        fs.write_file(&file, "value = 42\n")?;

        assert_eq!(system.current_directory(), root.as_path());
        assert!(system.current_directory().is_absolute());
        assert_eq!(system.read_to_string(&file)?, "value = 42\n");
        assert_eq!(system.canonicalize_path(&file)?, file);
        let entries = system
            .read_directory(&root)?
            .collect::<std::io::Result<Vec<_>>>()?;
        assert_eq!(entries.len(), 1);

        let manifest = SystemPath::new(concat!(env!("CARGO_MANIFEST_DIR"), "/Cargo.toml"));
        assert!(system.read_to_string(manifest)?.contains("anvil-ty-native"));
        assert!(system.canonicalize_path(manifest)?.is_absolute());
        assert!(system.as_writable().is_none());
        Ok(())
    }
}
