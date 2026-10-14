# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Run native/Pyright CLI acceptance cases and preserve their inputs and outputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

from engine_source import snapshot as engine_snapshot

ROOT = Path(__file__).resolve().parents[1]


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stub_fingerprint():
    root = ROOT.parent / "anvil-pyright/packages/pyright-internal/src/anvil-typeshed"
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest.update(str(path.relative_to(root)).encode() + b"\0")
            digest.update(path.read_bytes())
    return digest.hexdigest()


def host_python():
    executable = shutil.which("python3")
    if executable is None:
        return None
    # The report harness probes the same host used by the comparison checker.
    # Native validation itself never executes this interpreter.
    return json.loads(
        subprocess.check_output(
            [
                executable,
                "-c",
                "import json, sys; print(json.dumps({'executable': sys.executable, 'version': sys.version, 'prefix': sys.prefix, 'search_paths': sys.path}))",
            ],
            text=True,
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
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
    import test_parity
    import test_validate

    loader = unittest.TestLoader()
    cases = [
        test_parity.ValidateParity(name)
        for name in loader.getTestCaseNames(test_parity.ValidateParity)
    ]
    bundle = test_validate.PYRIGHT / "packages/pyright/dist/pyright.js"
    source_files = [ROOT / "anvil/native/Cargo.toml", ROOT / "anvil/native/Cargo.lock"]
    source_files += sorted((ROOT / "anvil/native/src").glob("*.rs"))
    source_files += [
        ROOT / "anvil/tests/test_parity.py",
        ROOT / "anvil/tests/test_validate.py",
        Path(__file__),
        ROOT / "anvil/engine_source.py",
    ]
    report = {
        "boundary": "real anvil validate --json; no performance measurements",
        "native_binary_sha256": fingerprint(backend),
        "cli_bundle_sha256": fingerprint(test_validate.CLI),
        "pyright_bundle_sha256": fingerprint(bundle),
        "api_stubs_sha256": stub_fingerprint(),
        "ruff_source": engine_snapshot(ROOT),
        "host_python": host_python(),
        "pyright_version": subprocess.check_output(
            [str(test_validate.PYRIGHT / "packages/pyright/index.js"), "--version"],
            text=True,
        ).strip(),
        "source_sha256": {
            str(path.relative_to(ROOT)): fingerprint(path) for path in source_files
        },
    }
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(cases))
    if (
        engine_snapshot(ROOT) != report["ruff_source"]
        or fingerprint(backend) != report["native_binary_sha256"]
        or any(
            fingerprint(ROOT / path) != digest
            for path, digest in report["source_sha256"].items()
        )
    ):
        raise RuntimeError("checker or adapter sources changed during acceptance tests")
    report.update(
        {
            "passed": result.wasSuccessful() and not result.skipped,
            "tests_run": result.testsRun,
            "equivalent_on_recorded_cases": result.wasSuccessful()
            and not result.skipped
            and not any(
                item["comparison"] == "known-difference"
                for case in cases
                for item in getattr(case, "evidence", [])
            ),
            "cases": [
                {"name": case.id(), "evidence": getattr(case, "evidence", [])}
                for case in cases
            ],
        }
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
