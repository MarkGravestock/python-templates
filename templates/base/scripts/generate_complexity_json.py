"""Dump radon cyclomatic-complexity JSON for src/ to the given file.

Usage: python scripts/generate_complexity_json.py build/complexity.json
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    out_path = Path(sys.argv[1])
    result = subprocess.run(
        [sys.executable, "-m", "radon", "cc", "src", "-j"],
        capture_output=True,
        text=True,
        check=True,
    )
    json.loads(result.stdout)  # fail loudly here rather than in the checker
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(result.stdout, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
