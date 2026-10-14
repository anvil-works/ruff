# /// script
# requires-python = ">=3.13"
# dependencies = ["psutil==7.2.2"]
# ///
"""Compare fresh checker and real CLI processes, including all child RSS."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import statistics
import subprocess
import tempfile
import time
from contextlib import suppress
from datetime import datetime, timezone
from pathlib import Path

import psutil
from engine_source import snapshot as engine_snapshot

ROOT = Path(__file__).resolve().parents[1]


def measure(command, env):
    # File output avoids pipe-buffer stalls while sampling the process tree.
    with tempfile.TemporaryFile(mode="w+") as output, tempfile.TemporaryFile(
        mode="w+"
    ) as errors:
        started = time.perf_counter()
        process = subprocess.Popen(command, env=env, stdout=output, stderr=errors)
        peak = 0
        while process.poll() is None:
            try:
                parent = psutil.Process(process.pid)
                rss = 0
                for child in [parent, *parent.children(recursive=True)]:
                    with suppress(psutil.NoSuchProcess, psutil.AccessDenied):
                        rss += child.memory_info().rss
                peak = max(peak, rss)
            except psutil.NoSuchProcess:
                pass
            time.sleep(0.002)
        elapsed = time.perf_counter() - started
        output.seek(0)
        errors.seek(0)
        stdout, stderr = output.read(), errors.read()
    if process.returncode not in (0, 1):
        raise RuntimeError(f"{command}: exit {process.returncode}: {stderr or stdout}")
    payload = (
        json.loads(stdout)
        if "--outputjson" in command
        else [json.loads(line) for line in stdout.splitlines() if line.strip()][-1]
    )
    return {
        "seconds": elapsed,
        "peak_tree_rss_mib": peak / 1024**2,
        "exit_code": process.returncode,
        "output": payload,
    }


def synthetic(app, forms):
    app.mkdir()
    (app / "anvil.yaml").write_text(
        "name: Ty benchmark\npackage_name: TyBenchmark\nruntime_options:\n  version: 2\n  client_version: '3'\n  server_version: python3-full\n"
    )
    for index in range(forms):
        form = app / "client_code" / f"Form{index}"
        form.mkdir(parents=True)
        (form / "form_template.yaml").write_text(
            "container:\n  type: ColumnPanel\ncomponents:\n- name: label_1\n  type: Label\n"
        )
        (form / "__init__.py").write_text(
            f"from ._anvil_designer import Form{index}Template\nimport anvil.server\n\nclass Form{index}(Form{index}Template):\n    def __init__(self, **properties):\n        self.init_components(**properties)\n        self.label_1.text = 'Ready'\n\n    def load(self) -> str:\n        return anvil.server.call('title_{index}')\n"
        )
        server = app / "server_code"
        server.mkdir(exist_ok=True)
        (server / f"Service{index}.py").write_text(
            f"import anvil.server\n\n@anvil.server.callable\ndef title_{index}() -> str:\n    return 'Ready'\n"
        )


def revision(repository):
    return subprocess.check_output(
        ["git", "-C", str(repository), "rev-parse", "HEAD"], text=True
    ).strip()


def diagnostics_summary(payload):
    if "generalDiagnostics" in payload:
        return {
            "summary": payload["summary"],
            "diagnostics": payload["generalDiagnostics"],
        }
    data = payload.get("data", {})
    files = data.get("files", [data])
    return {
        "success": payload["success"],
        "file_count": data.get("count", 1),
        "invalid_files": [
            file for file in files if file.get("valid") is False or file.get("issues")
        ],
        "warnings": data.get("warnings", []),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pyright-root", type=Path, default=ROOT.parent / "anvil-pyright"
    )
    parser.add_argument("--cli-root", type=Path, default=ROOT.parent / "anvil-cli")
    parser.add_argument(
        "--app",
        type=Path,
        help="Optional existing app in addition to synthetic fixtures",
    )
    parser.add_argument("--sizes", nargs="+", type=int, default=[10, 100])
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--native", type=Path, help="Also benchmark the release Rust adapter"
    )
    args = parser.parse_args()
    if args.runs < 1 or any(size < 1 for size in args.sizes):
        parser.error("runs and sizes must be positive")
    pyright = args.pyright_root.absolute() / "packages/pyright/index.js"
    adapter = ROOT / "anvil/anvil-ty"
    cli = args.cli_root.absolute() / "dist/cli.js"
    executables = {"pyright": pyright, "ty": adapter}
    if args.native:
        executables["native"] = args.native.absolute()
    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "host": {
            "platform": platform.platform(),
            "machine": platform.machine(),
            "ram_mib": psutil.virtual_memory().total / 1024**2,
        },
        "versions": {
            "ty": subprocess.check_output(
                [str(adapter), "--version"], text=True
            ).strip(),
            "pyright": subprocess.check_output(
                ["node", str(pyright), "--version"], text=True
            ).strip(),
            "node": subprocess.check_output(["node", "--version"], text=True).strip(),
            "ty_revision": revision(ROOT),
            "pyright_revision": revision(args.pyright_root),
            "cli_revision": revision(args.cli_root),
        },
        "method": "Fresh processes; one warm-up per command; alternating backend order; 2ms sampled sum of RSS across parent and descendants. Warm filesystem caches; no incremental or cold-cache claim. Shared memory may be counted more than once; brief peaks may be missed.",
        "ruff_source": engine_snapshot(ROOT),
        "cases": [],
    }
    report["sha256"] = {
        str(file.relative_to(args.pyright_root)): hashlib.sha256(
            file.read_bytes()
        ).hexdigest()
        for file in [
            args.pyright_root / "packages/pyright/dist/pyright.js",
            *sorted(
                (
                    args.pyright_root
                    / "packages/pyright-internal/out/packages/pyright-internal/src/anvil"
                ).glob("*.js")
            ),
        ]
    }
    for file in [
        Path(__file__),
        ROOT / "anvil/engine_source.py",
        adapter,
        ROOT / "anvil/validate.py",
        ROOT / "anvil/prepare.cjs",
        cli,
    ]:
        report["sha256"][str(file)] = hashlib.sha256(file.read_bytes()).hexdigest()
    if args.native:
        report["versions"]["native"] = subprocess.check_output(
            [str(executables["native"]), "--version"], text=True
        ).strip()
        report["versions"]["rustc"] = subprocess.check_output(
            ["rustc", "+1.99.0", "--version"], text=True
        ).strip()
        report["sha256"]["native_executable"] = hashlib.sha256(
            executables["native"].read_bytes()
        ).hexdigest()
        native = ROOT / "anvil/native"
        for file in [
            native / "Cargo.lock",
            native / "Cargo.toml",
            *sorted((native / "src").glob("*.rs")),
        ]:
            report["sha256"][f"native/{file.relative_to(native)}"] = hashlib.sha256(
                file.read_bytes()
            ).hexdigest()
    stub_hash = hashlib.sha256()
    stub_root = args.pyright_root / "packages/pyright-internal/src/anvil-typeshed"
    for file in sorted(stub_root.rglob("*.pyi")):
        stub_hash.update(
            str(file.relative_to(stub_root)).encode() + b"\0" + file.read_bytes()
        )
    report["sha256"]["anvil_typeshed"] = stub_hash.hexdigest()
    with tempfile.TemporaryDirectory(prefix="anvil-ty-benchmark-") as temporary:
        fixtures = []
        for size in args.sizes:
            app = Path(temporary) / f"forms-{size}"
            synthetic(app, size)
            fixtures.append((f"synthetic-{size}-forms-{size}-services", app))
        if args.app:
            fixtures.append((args.app.name, args.app.absolute()))
        for name, app in fixtures:
            for mode in ("checker", "cli"):
                case = {
                    "fixture": name,
                    "mode": mode,
                    "python_files": sum(
                        1
                        for area in ("client_code", "server_code")
                        for _ in (app / area).rglob("*.py")
                    ),
                    "backends": {},
                    "input_sha256": {
                        str(path.relative_to(app)): hashlib.sha256(
                            path.read_bytes()
                        ).hexdigest()
                        for path in sorted(app.rglob("*"))
                        if path.is_file() and ".git" not in path.relative_to(app).parts
                    },
                }
                commands = {
                    backend: (
                        (["node"] if backend == "pyright" else [])
                        + [
                            str(executable),
                            "--outputjson",
                            "--level",
                            "warning",
                            "--project",
                            str(app),
                        ]
                        if mode == "checker"
                        else ["node", str(cli), "--json", "validate", str(app)]
                    )
                    for backend, executable in executables.items()
                }
                environments = {
                    backend: {
                        **os.environ,
                        "ANVIL_PYRIGHT": str(executables[backend]),
                        "ANVIL_PYRIGHT_ROOT": str(args.pyright_root.absolute()),
                    }
                    for backend in commands
                }
                # Verify the selected executable before benchmarking; the CLI falls back if probing fails.
                for backend, env in environments.items():
                    probe = subprocess.run(
                        [env["ANVIL_PYRIGHT"], "--version"],
                        env=env,
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    if backend != "pyright" and not probe.stdout.startswith("anvil-ty"):
                        raise RuntimeError("CLI would not select the ty adapter")
                    measure(commands[backend], env)
                    case["backends"][backend] = {"samples": []}
                for run in range(args.runs):
                    order = list(commands)
                    order = order[run % len(order) :] + order[: run % len(order)]
                    for backend in order:
                        sample = measure(commands[backend], environments[backend])
                        output = sample.pop("output")
                        sample["diagnostics"] = diagnostics_summary(output)
                        case["backends"][backend]["diagnostics"] = sample["diagnostics"]
                        case["backends"][backend]["samples"].append(sample)
                for data in case["backends"].values():
                    data["median_seconds"] = statistics.median(
                        s["seconds"] for s in data["samples"]
                    )
                    data["median_peak_tree_rss_mib"] = statistics.median(
                        s["peak_tree_rss_mib"] for s in data["samples"]
                    )
                before, after = case["backends"]["pyright"], case["backends"]["ty"]
                case["speedup"] = before["median_seconds"] / after["median_seconds"]
                case["rss_reduction_percent"] = 100 * (
                    1
                    - after["median_peak_tree_rss_mib"]
                    / before["median_peak_tree_rss_mib"]
                )
                if args.native:
                    native = case["backends"]["native"]
                    case["native_vs_adapter_speedup"] = (
                        after["median_seconds"] / native["median_seconds"]
                    )
                    case["native_vs_pyright_speedup"] = (
                        before["median_seconds"] / native["median_seconds"]
                    )
                report["cases"].append(case)
                print(
                    f"{name} {mode}: {before['median_seconds']:.3f}s / {before['median_peak_tree_rss_mib']:.1f}MiB -> {after['median_seconds']:.3f}s / {after['median_peak_tree_rss_mib']:.1f}MiB ({case['speedup']:.2f}x)",
                    flush=True,
                )
                if args.native:
                    print(
                        f"  native: {native['median_seconds']:.3f}s / {native['median_peak_tree_rss_mib']:.1f}MiB ({case['native_vs_adapter_speedup']:.2f}x over adapter, {case['native_vs_pyright_speedup']:.2f}x over pyright)",
                        flush=True,
                    )
    if engine_snapshot(ROOT) != report["ruff_source"]:
        raise RuntimeError("engine sources changed during benchmarking")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
