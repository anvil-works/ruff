# /// script
# requires-python = ">=3.11"
# dependencies = ["psutil==7.2.2"]
# ///
"""Profile a generated release example and the existing CLI without production edits."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "anvil"))
from benchmark import synthetic  # ruff: ignore[module-import-not-at-top-of-file] -- import the existing fixture generator


def native_source():
    source = (ROOT / "anvil/native/src/main.rs").read_text()

    def replace(before, after):
        nonlocal source
        assert source.count(before) == 1, before
        source = source.replace(before, after)

    def before(anchor, label):
        replace(anchor, f"profile_mark({label});\n{anchor}")

    replace(
        "fn main() {",
        """fn profile_mark(label: &str) {
    static START: std::sync::OnceLock<Instant> = std::sync::OnceLock::new();
    eprintln!("[ANVIL_NATIVE_PROFILE] {}", json!({"name": label, "milliseconds": START.get_or_init(Instant::now).elapsed().as_secs_f64() * 1000.0}));
}
fn main() {
    profile_mark("main");""",
    )
    before("    if args.version {", '"arguments"')
    before("    let pyright = std::env::var_os", '"config"')
    before("    let client = sources", '"api_read"')
    before("    let forms = designers", '"source_read"')
    before(
        "    let mut output = Vec::new();\n    for (environment, selected)",
        '"form_generation"',
    )
    before("        let root = SystemPathBuf::from", '&format!("{environment}.start")')
    before("        if !fs.is_file(code.join", '&format!("{environment}.source_mount")')
    before(
        "        for entry in WalkDir::new(stubs.join",
        '&format!("{environment}.form_mount")',
    )
    before("        let mut roots = vec!", '&format!("{environment}.api_mount")')
    before(
        "        let mut db = ProjectDatabase::fallible",
        '&format!("{environment}.options")',
    )
    before("        let paths = selected", '&format!("{environment}.db_init")')
    replace(
        "        for item in db.check() {",
        """        profile_mark(&format!("{environment}.db_ready"));
        let diagnostics = db.check();
        profile_mark(&format!("{environment}.check"));
        for item in diagnostics {""",
    )
    replace(
        "            output.push(diagnostic(&db, item, &origins)?);\n        }",
        """            output.push(diagnostic(&db, item, &origins)?);
        }
        profile_mark(&format!("{environment}.diagnostics"));
        drop(db);
        profile_mark(&format!("{environment}.drop"));""",
    )
    before("    std::process::exit(i32::from(errors > 0));", '"output"')
    return source


def invoke(command, env, prefix):
    started = time.perf_counter()
    result = subprocess.run(
        command, env=env, text=True, capture_output=True, check=True
    )
    milliseconds = (time.perf_counter() - started) * 1000
    payload = (
        json.loads(result.stdout)
        if prefix == "ANVIL_NATIVE_PROFILE"
        else [json.loads(line) for line in result.stdout.splitlines()][-1]
    )
    profiles = [
        json.loads(line.split("] ", 1)[1])
        for line in result.stderr.splitlines()
        if line.startswith(f"[{prefix}] ")
    ]
    return {"wall_ms": milliseconds, "profile": profiles, "output": payload}


def normalize(value, app):
    if isinstance(value, dict):
        return {
            key: normalize(item, app)
            for key, item in value.items()
            if key not in ("timestamp", "timeInSec", "version")
        }
    if isinstance(value, list):
        return [normalize(item, app) for item in value]
    if isinstance(value, str):
        return value.replace(str(app), "<app>")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    native = ROOT / "anvil/native"
    example = native / "examples/anvil_profile.rs"
    assert not example.exists(), "Do not overwrite an existing example"
    made_directory = not example.parent.exists()
    example.parent.mkdir(exist_ok=True)
    try:
        example.write_text(native_source())
        subprocess.run(
            ["cargo", "build", "--release", "--locked", "--example", "anvil_profile"],
            cwd=native,
            check=True,
        )
    finally:
        example.unlink()
        if made_directory:
            example.parent.rmdir()
    executable = native / "target/release/examples/anvil_profile"
    baseline = native / "target/release/anvil-ty-native"
    cli = ROOT.parent / "anvil-cli/dist/cli.js"
    env = {**os.environ, "ANVIL_PYRIGHT_ROOT": str(ROOT.parent / "anvil-pyright")}
    report = {
        "method": "Five fresh-process runs after warm-up per fixture/mode. Stopwatch boundaries in a generated Rust release example and read-only transformation of the existing CLI bundle. Profiling overhead is included; plain controls are also recorded. Cached CLI is a throwaway per-invocation app-root memoization experiment. Outputs must match plain controls. No production sources changed.",
        "sha256": {
            str(file): hashlib.sha256(file.read_bytes()).hexdigest()
            for file in [
                cli,
                baseline,
                native / "src/main.rs",
                native / "Cargo.toml",
                native / "Cargo.lock",
            ]
        },
        "cases": [],
    }
    with tempfile.TemporaryDirectory(prefix="anvil-profile-") as temporary:
        for size in (10, 100):
            app = Path(temporary) / str(size)
            synthetic(app, size)
            direct = ["--outputjson", "--project", str(app)]
            cli_command = ["node", str(cli), "--json", "validate", str(app)]
            modes = {
                "native_plain": ([str(baseline), *direct], env, "ANVIL_NATIVE_PROFILE"),
                "native_profile": (
                    [str(executable), *direct],
                    env,
                    "ANVIL_NATIVE_PROFILE",
                ),
                "cli_plain": (
                    cli_command,
                    {**env, "ANVIL_PYRIGHT": str(baseline)},
                    "ANVIL_CLI_PROFILE",
                ),
                "cli_profile": (
                    cli_command,
                    {
                        **env,
                        "ANVIL_PYRIGHT": str(executable),
                        "ANVIL_PROFILE_CLI": str(cli),
                        "NODE_OPTIONS": f"--require {ROOT / 'anvil/profiling/cli_probe.cjs'}",
                    },
                    "ANVIL_CLI_PROFILE",
                ),
            }
            modes["cli_cached"] = (
                cli_command,
                {**modes["cli_profile"][1], "ANVIL_PROFILE_ROOT_CACHE": "1"},
                "ANVIL_CLI_PROFILE",
            )
            modes["cli_lazy_ui"] = (
                cli_command,
                {**modes["cli_profile"][1], "ANVIL_PROFILE_LAZY_UI": "1"},
                "ANVIL_CLI_PROFILE",
            )
            modes["cli_lazy_ui_cached"] = (
                cli_command,
                {**modes["cli_lazy_ui"][1], "ANVIL_PROFILE_ROOT_CACHE": "1"},
                "ANVIL_CLI_PROFILE",
            )
            samples = {mode: [] for mode in modes}
            expected = {}
            for mode, (command, variables, prefix) in modes.items():
                sample = invoke(command, variables, prefix)
                category = "native" if mode.startswith("native") else "cli"
                output = normalize(sample["output"], app)
                if category in expected:
                    assert output == expected[category], (size, mode, output)
                expected[category] = output
            for run in range(args.runs):
                order = list(modes)
                order = order[run % len(order) :] + order[: run % len(order)]
                for mode in order:
                    command, variables, prefix = modes[mode]
                    sample = invoke(command, variables, prefix)
                    category = "native" if mode.startswith("native") else "cli"
                    assert normalize(sample.pop("output"), app) == expected[category], (
                        size,
                        mode,
                    )
                    samples[mode].append(sample)
            case = {
                "python_files": size * 2,
                "modes": {
                    mode: {
                        "median_wall_ms": statistics.median(
                            sample["wall_ms"] for sample in data
                        ),
                        "samples": data,
                    }
                    for mode, data in samples.items()
                },
                "equivalent_outputs": True,
            }
            report["cases"].append(case)
            print(
                size * 2,
                {
                    mode: round(data["median_wall_ms"], 2)
                    for mode, data in case["modes"].items()
                },
                flush=True,
            )
    args.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
