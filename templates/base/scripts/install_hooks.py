"""Point git at the versioned .githooks directory. Cross-platform; run via `uv run poe hooks`.

Replaces the usual `pre-commit install` dance — the pre-commit framework is not
used here, the hook is a plain sh script that git's bundled shell runs on every
platform.
"""

from __future__ import annotations

import stat
import subprocess
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    toplevel = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
        cwd=project_root,
    ).stdout.strip()
    if Path(toplevel).resolve() != project_root:
        print(
            "Not installed: this project is nested inside another git repository\n"
            f"  project root: {project_root}\n"
            f"  git toplevel: {toplevel}\n"
            "core.hooksPath is repo-wide, so hooks only make sense once the template\n"
            "is the root of its own repository.",
            file=sys.stderr,
        )
        return 1
    subprocess.run(["git", "config", "core.hooksPath", ".githooks"], check=True, cwd=project_root)
    hook = project_root / ".githooks" / "pre-commit"
    hook.chmod(hook.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print("Installed: core.hooksPath -> .githooks (pre-commit runs `uv run poe check`).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
