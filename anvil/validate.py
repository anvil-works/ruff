# /// script
# requires-python = ">=3.13"
# dependencies = ["ty==0.0.85"]
# ///
"""Development adapter for anvil-cli's existing semantic validator contract."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def position(source, point):
    # ty's GitLab output uses one-based Unicode scalar columns; Pyright uses UTF-16.
    line = point["line"] - 1
    text = source.split("\n")[line].removeprefix("\ufeff")
    character = len(text[: point["column"] - 1].encode("utf-16-le")) // 2
    return {"line": line, "character": character}


def validate(app, files):
    pyright_root = Path(
        os.environ.get("ANVIL_PYRIGHT_ROOT", ROOT.parent / "anvil-pyright")
    ).resolve()
    ty = ROOT / ".venv/bin/ty"
    diagnostics = []
    with tempfile.TemporaryDirectory(prefix="anvil-ty-") as temporary:
        prepared = subprocess.run(
            [
                "node",
                str(ROOT / "anvil/prepare.cjs"),
                str(pyright_root),
                str(app),
                temporary,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        manifest = json.loads(prepared.stdout)
        for environment in ("client", "server"):
            selected = manifest["selected"][environment]
            if files:
                selected = [
                    file
                    for file in selected
                    if Path(manifest["origins"][file]) in files
                ]
            if not selected:
                continue
            workspace = Path(temporary) / environment
            roots = [str(workspace / "stubs"), str(workspace)]
            if environment == "server":
                roots.append(str(workspace / manifest["package"]))
            result = subprocess.run(
                [
                    str(ty),
                    "check",
                    "--project",
                    str(workspace),
                    "--python-version",
                    "3.10",
                    "--config",
                    "environment.root = " + json.dumps(roots),
                    "--output-format",
                    "gitlab",
                    "--color",
                    "never",
                    "--no-progress",
                    *selected,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if result.returncode not in (0, 1):
                raise RuntimeError(result.stderr or result.stdout)
            for diagnostic in json.loads(result.stdout):
                location = diagnostic["location"]
                staged = (
                    os.path.abspath(workspace / location["path"])
                    if location["path"]
                    else None
                )
                original = manifest["origins"].get(staged)
                item = {
                    "severity": {
                        "major": "error",
                        "critical": "error",
                        "minor": "warning",
                        "info": "information",
                    }[diagnostic["severity"]],
                    "message": diagnostic["description"],
                    "rule": diagnostic["check_name"],
                }
                if original:
                    item["file"] = original
                    source = Path(staged).read_text()
                    item["range"] = {
                        "start": position(source, location["positions"]["begin"]),
                        "end": position(source, location["positions"]["end"]),
                    }
                diagnostics.append(item)
        if manifest["dependencies"]:
            diagnostics.append(
                {
                    "severity": "warning",
                    "rule": "anvil-ty-proof-limit",
                    "message": "The ty proof does not yet resolve Anvil dependency caches.",
                }
            )
    return diagnostics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="store_true")
    parser.add_argument("--outputjson", action="store_true")
    parser.add_argument("--level", choices=["error", "warning"], default="warning")
    parser.add_argument("--project", type=Path)
    parser.add_argument("files", nargs="*", type=Path)
    args = parser.parse_args()
    if args.version:
        result = subprocess.run(
            [str(ROOT / ".venv/bin/ty"), "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        print("anvil-ty proof; " + result.stdout.strip())
        return 0
    if not args.outputjson or args.project is None:
        parser.error("the development adapter requires --outputjson and --project")
    started = time.perf_counter()
    try:
        diagnostics = validate(
            args.project.absolute(), {file.absolute() for file in args.files}
        )
    except (OSError, RuntimeError, subprocess.CalledProcessError, ValueError) as error:
        detail = (
            error.stderr
            if isinstance(error, subprocess.CalledProcessError)
            else str(error)
        )
        print(detail, file=sys.stderr)
        return 2
    if args.level == "error":
        diagnostics = [item for item in diagnostics if item["severity"] == "error"]
    print(
        json.dumps(
            {
                "version": "anvil-ty-proof",
                "generalDiagnostics": diagnostics,
                "summary": {
                    "errorCount": sum(
                        item["severity"] == "error" for item in diagnostics
                    ),
                    "warningCount": sum(
                        item["severity"] == "warning" for item in diagnostics
                    ),
                    "timeInSec": time.perf_counter() - started,
                },
            }
        )
    )
    return int(any(item["severity"] == "error" for item in diagnostics))


if __name__ == "__main__":
    sys.exit(main())
