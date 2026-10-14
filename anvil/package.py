#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Package the native checker, API stubs and @anvil-works/anvil-ty npm wrapper."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import platform
import shutil
import subprocess
import tarfile
from pathlib import Path

from engine_source import snapshot as engine_snapshot

ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / "anvil/native"
API_STUBS = ROOT / "anvil/api-stubs"


def sha256(path: Path) -> str:
    with path.open("rb") as content:
        return hashlib.file_digest(content, "sha256").hexdigest()


def package(binary: Path, output: Path) -> dict:
    archive = output.with_name(output.name + ".tar.gz")
    checksum = archive.with_name(archive.name + ".sha256")
    version = subprocess.check_output([str(binary), "--version"], text=True).strip()
    if not version.startswith("anvil-ty native"):
        raise ValueError(f"expected the native checker, got {version!r}")
    engine = engine_snapshot(ROOT)
    npm = json.loads((ROOT / "anvil/npm/package.json").read_text())
    os_name = {"Darwin": "darwin", "Linux": "linux", "Windows": "win32"}[
        platform.system()
    ]
    cpu = {"arm64": "arm64", "aarch64": "arm64", "x86_64": "x64", "amd64": "x64"}[
        platform.machine().lower()
    ]
    name = f"@anvil-works/anvil-ty-{os_name}-{cpu}"
    if name not in npm["optionalDependencies"]:
        raise ValueError(f"unsupported npm platform: {os_name}-{cpu}")
    platform_npm = {
        "name": name,
        "version": npm["version"],
        "description": npm["description"],
        "license": npm["license"],
        "repository": {**npm["repository"], "directory": "anvil/native"},
        "publishConfig": npm["publishConfig"],
        "os": [os_name],
        "cpu": [cpu],
        "files": ["bin", "share", "licenses", "manifest.json", "README.md"],
    }
    if os_name == "linux":
        platform_npm["libc"] = ["glibc"]
    npm_packages = [(output, platform_npm), (ROOT / "anvil/npm", npm)]
    npm_archives = [
        output.parent
        / f"{metadata['name'].lstrip('@').replace('/', '-')}-{metadata['version']}.tgz"
        for _, metadata in npm_packages
    ]
    for path in (output, archive, checksum, *npm_archives):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite {path}")

    (output / "bin").mkdir(parents=True)
    executable = output / (
        "bin/anvil-ty-native.exe" if os_name == "win32" else "bin/anvil-ty-native"
    )
    shutil.copyfile(binary, executable)
    executable.chmod(0o755)
    shutil.copytree(
        API_STUBS,
        output / "share/anvil-typeshed",
    )
    licenses = {
        "ruff-MIT.txt": ROOT / "LICENSE",
        "typeshed.txt": ROOT / "crates/ty_vendored/vendor/typeshed/LICENSE",
        "anvil-pyright-MIT.txt": ROOT / "anvil/licenses/anvil-pyright-MIT.txt",
    }
    (output / "licenses").mkdir()
    for license_name, source in licenses.items():
        shutil.copyfile(source, output / "licenses" / license_name)
    (output / "package.json").write_text(json.dumps(platform_npm, indent=2) + "\n")
    (output / "README.md").write_text(
        f"# {platform_npm['name']}\n\n"
        "This bundle contains a native checker and the static Anvil API stubs.\n"
        "Keep bin/ and share/ together; the entire folder can be moved.\n"
        "This is the native package selected by @anvil-works/anvil-ty.\n"
        "anvil-cli uses that wrapper to select the executable for your platform.\n"
        "For a standalone bundle with the new CLI:\n\n"
        "~~~sh\n"
        f'ANVIL_TY="/absolute/path/to/this/bundle/{executable.relative_to(output).as_posix()}" '
        "anvil validate /path/to/app\n"
        "~~~\n\n"
        "No anvil-pyright or anvil-ruff checkout, Rust toolchain, or Python launcher\n"
        "is required. The existing Node-based anvil-cli remains required. Cached\n"
        "Anvil dependencies and optional Python libraries must already be available\n"
        "in the user's app/environment; this bundle does not fetch or install them.\n\n"
        "The executable is built for the platform in manifest.json. Linux builds\n"
        "require glibc 2.34 or newer; Alpine/musl is unsupported. This checker\n"
        "supplies validation rather than LSP support. Native ty\n"
        "diagnostics and the documented Pyright-specific differences still apply.\n\n"
        "Anvil API stubs are generated from anvil-works/anvil. ty/Ruff and the\n"
        "vendored standard-library typeshed originate from Astral's upstream\n"
        "repositories. Relevant source licenses are in licenses/. The manifest\n"
        "records the prebuilt binary hash, bundled file hashes and the source\n"
        "snapshot at packaging time, including uncommitted native changes.\n",
        encoding="utf-8",
    )
    source_paths = [
        *sorted((NATIVE / "src").glob("*.rs")),
        NATIVE / "Cargo.toml",
        NATIVE / "Cargo.lock",
        NATIVE / "rust-toolchain.toml",
        Path(__file__).resolve(),
        Path(__file__).with_name("engine_source.py").resolve(),
        ROOT / "anvil/npm/package.json",
        ROOT / "anvil/npm/index.cjs",
        ROOT / "anvil/npm/README.md",
        ROOT / "anvil/npm/LICENSE",
        ROOT / "anvil/sync-anvil-stubs.mjs",
    ]
    manifest = {
        "format_version": 3,
        "checker_version": version,
        "build_host": {"system": platform.system(), "machine": platform.machine()},
        "source_snapshot_at_packaging": {
            **engine,
            "anvil_api_stubs": json.loads((API_STUBS / "SOURCE.json").read_text()),
            "native_files": {
                path.relative_to(ROOT).as_posix(): sha256(path) for path in source_paths
            },
        },
        "files": {
            path.relative_to(output).as_posix(): sha256(path)
            for path in sorted(output.rglob("*"))
            if path.is_file()
        },
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    # Stable tar/gzip headers make identical inputs produce identical archives.
    with archive.open("xb") as raw, gzip.GzipFile(
        fileobj=raw, mode="wb", filename="", mtime=0
    ) as compressed, tarfile.open(fileobj=compressed, mode="w") as tar:
        for path in [output, *sorted(output.rglob("*"))]:
            info = tar.gettarinfo(
                str(path), str(Path(output.name) / path.relative_to(output))
            )
            info.uid = info.gid = info.mtime = 0
            info.uname = info.gname = ""
            info.mode = 0o755 if path.is_dir() or path == executable else 0o644
            if path.is_file():
                with path.open("rb") as content:
                    tar.addfile(info, content)
            else:
                tar.addfile(info)
    digest = sha256(archive)
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    packed = []
    for directory, metadata in npm_packages:
        result = json.loads(
            subprocess.check_output(
                [
                    shutil.which("npm") or "npm",
                    "pack",
                    "--ignore-scripts",
                    "--json",
                    "--pack-destination",
                    str(output.parent),
                    str(directory),
                ],
                text=True,
            )
        )[0]
        npm_archive = output.parent / result["filename"]
        packed.append(
            {
                "name": metadata["name"],
                "archive": str(npm_archive),
                "sha256": sha256(npm_archive),
            }
        )
    return {
        "bundle": str(output),
        "archive": str(archive),
        "sha256": digest,
        "npm_packages": packed,
    }


def main() -> None:
    version = json.loads((ROOT / "anvil/npm/package.json").read_text())["version"]
    system = "macos" if platform.system() == "Darwin" else platform.system().lower()
    name = f"anvil-ty-{version}-{system}-{platform.machine()}"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--binary",
        type=Path,
        default=NATIVE
        / (
            "target/release/anvil-ty-native.exe"
            if platform.system() == "Windows"
            else "target/release/anvil-ty-native"
        ),
    )
    parser.add_argument("--output", type=Path, default=ROOT / "anvil/dist" / name)
    args = parser.parse_args()
    print(json.dumps(package(args.binary.resolve(), args.output.resolve()), indent=2))


if __name__ == "__main__":
    main()
