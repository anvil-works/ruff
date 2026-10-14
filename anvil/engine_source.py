"""Record the Ruff checkout used by local validation experiments."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


def snapshot(root: Path) -> dict[str, str]:
    def git(*arguments: str) -> str:
        return subprocess.check_output(["git", "-C", str(root), *arguments], text=True)

    # Diff against HEAD includes staged and unstaged changes. Reject untracked
    # source rather than presenting an incomplete patch as reproducible evidence.
    if git("ls-files", "--others", "--exclude-standard").strip():
        raise RuntimeError(
            "Ruff has untracked files; track engine sources before recording evidence"
        )
    patch = git(
        "diff", "HEAD", "--binary", "--no-ext-diff", "--no-textconv", "--no-color"
    )
    return {
        "revision": git("rev-parse", "HEAD").strip(),
        "patch": patch,
        "patch_sha256": hashlib.sha256(patch.encode()).hexdigest(),
    }
