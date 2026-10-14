#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Collect one consistent set of native npm packages for local publication."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tarfile
from pathlib import Path

WRAPPER = "@anvil-works/anvil-ty"


def collect(inputs: Path, output: Path) -> dict:
    archives = {}
    snapshots = []
    for path in sorted(inputs.rglob("*.tgz")):
        with tarfile.open(path) as tar:
            metadata = json.load(tar.extractfile("package/package.json"))
            name = metadata["name"]
            if name in archives:
                # Each build also packs the wrapper. npm's tar headers can differ
                # between hosts; the published wrapper's actual files must agree.
                if name != WRAPPER:
                    raise ValueError(f"duplicate platform package: {name}")
                files = {
                    item.name: tar.extractfile(item).read()
                    for item in tar.getmembers()
                    if item.isfile()
                }
                with tarfile.open(archives[name][0]) as previous:
                    previous_files = {
                        item.name: previous.extractfile(item).read()
                        for item in previous.getmembers()
                        if item.isfile()
                    }
                if files != previous_files:
                    raise ValueError("wrapper files differ between builds")
                continue
            archives[name] = (path, metadata)
            if name != WRAPPER:
                manifest = json.load(tar.extractfile("package/manifest.json"))
                snapshot = manifest["source_snapshot_at_packaging"]
                if snapshot["patch"]:
                    raise ValueError(f"uncommitted source in {name}")
                snapshots.append(snapshot)
                for filename, digest in manifest["files"].items():
                    with tar.extractfile("package/" + filename) as content:
                        if hashlib.file_digest(content, "sha256").hexdigest() != digest:
                            raise ValueError(f"bundle hash mismatch: {name}/{filename}")
    if WRAPPER not in archives:
        raise ValueError("missing wrapper package")
    wrapper = archives[WRAPPER][1]
    expected_wrapper = json.loads(
        (Path(__file__).resolve().parent / "npm/package.json").read_text()
    )
    if wrapper != expected_wrapper:
        raise ValueError("wrapper metadata does not match the selected release source")
    expected = {WRAPPER, *wrapper["optionalDependencies"]}
    if set(archives) != expected:
        raise ValueError(f"missing or unexpected packages: {expected ^ set(archives)}")
    version = wrapper["version"]
    if any(metadata["version"] != version for _, metadata in archives.values()) or any(
        value != version for value in wrapper["optionalDependencies"].values()
    ):
        raise ValueError("package versions differ")
    if not snapshots or any(snapshot != snapshots[0] for snapshot in snapshots):
        raise ValueError("platforms were built from different source snapshots")

    # Check the complete input set before creating any publication output.
    output.mkdir(parents=True, exist_ok=False)
    result = {
        "version": version,
        "source_revision": snapshots[0]["revision"],
        "packages": [],
    }
    for name, (path, _) in sorted(archives.items()):
        filename = name.lstrip("@").replace("/", "-") + f"-{version}.tgz"
        destination = output / filename
        shutil.copyfile(path, destination)
        with destination.open("rb") as content:
            digest = hashlib.file_digest(content, "sha256").hexdigest()
        result["packages"].append({"name": name, "file": filename, "sha256": digest})
    (output / "RELEASE.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    (output / "SHA256SUMS").write_text(
        "".join(f"{item['sha256']}  {item['file']}\n" for item in result["packages"]),
        encoding="utf-8",
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(collect(args.inputs, args.output), indent=2))
