# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Record validation differences on temporary copies of local Anvil apps."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path

from engine_source import snapshot as engine_snapshot
from parity import ROOT, fingerprint, host_python, stub_fingerprint


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apps", nargs="+", type=Path)
    parser.add_argument(
        "--backend",
        type=Path,
        default=ROOT / "anvil/native/target/release/anvil-ty-native",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    backend = args.backend.resolve(strict=True)
    os.environ["ANVIL_TY_TEST_EXECUTABLE"] = str(backend)
    sys.path.insert(0, str(ROOT / "anvil/tests"))
    import test_validate as harness

    native_sources = [
        *sorted((ROOT / "anvil/native/src").glob("*.rs")),
        ROOT / "anvil/native/Cargo.toml",
        ROOT / "anvil/native/Cargo.lock",
        ROOT / "anvil/tests/test_validate.py",
        ROOT / "anvil/parity.py",
        ROOT / "anvil/engine_source.py",
        Path(__file__),
    ]
    report = {
        "boundary": "real anvil validate --json on temporary app copies; no performance measurements",
        "native_binary_sha256": fingerprint(backend),
        "ruff_source": engine_snapshot(ROOT),
        "host_python": host_python(),
        "cli_bundle_sha256": fingerprint(harness.CLI),
        "pyright_bundle_sha256": fingerprint(
            harness.PYRIGHT / "packages/pyright/dist/pyright.js"
        ),
        "api_stubs_sha256": stub_fingerprint(),
        "source_sha256": {
            str(path.relative_to(ROOT)): fingerprint(path) for path in native_sources
        },
        "apps": [],
    }
    for source in args.apps:
        source = source.resolve(strict=True)
        if not (source / "anvil.yaml").is_file():
            parser.error(f"not an Anvil app: {source}")
        print(f"Comparing {source.name}", flush=True)
        with tempfile.TemporaryDirectory() as directory:
            app = Path(directory) / "app"
            shutil.copytree(
                source,
                app,
                ignore=shutil.ignore_patterns(
                    ".git", "node_modules", ".venv", "__pycache__"
                ),
            )
            inputs = {
                str(path.relative_to(app)): fingerprint(path)
                for path in sorted(app.rglob("*"))
                if path.is_file()
            }
            case = {"source": str(source), "input_sha256": inputs, "outputs": []}
            validator = harness.ValidateIntegration()
            validator.app = app
            for name, executable in (
                ("pyright", harness.PYRIGHT / "packages/pyright/index.js"),
                ("native", None),
            ):
                result, events = validator.validate(backend=executable)
                events = json.loads(json.dumps(events).replace(str(app), "<app>"))
                for event in events:
                    event.pop("timestamp", None)
                data = events[-1].get("data", {})
                diagnostics = data.get("issues", []) + data.get("warnings", [])
                for file in data.get("files", []):
                    diagnostics += file.get("issues", []) + file.get("warnings", [])
                case["outputs"].append(
                    {
                        "backend": name,
                        "exit_code": result.returncode,
                        "diagnostic_counts": dict(
                            Counter(issue.get("rule", "cli") for issue in diagnostics)
                        ),
                        "events": events,
                        "stderr": result.stderr.replace(str(app), "<app>"),
                    }
                )
            case["source_unchanged"] = all(
                fingerprint(source / name) == digest for name, digest in inputs.items()
            )
            if not case["source_unchanged"]:
                raise RuntimeError(f"source app changed during comparison: {source}")
            report["apps"].append(case)
    if (
        engine_snapshot(ROOT) != report["ruff_source"]
        or fingerprint(backend) != report["native_binary_sha256"]
        or any(
            fingerprint(ROOT / path) != digest
            for path, digest in report["source_sha256"].items()
        )
    ):
        raise RuntimeError(
            "checker or adapter sources changed during corpus comparison"
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
