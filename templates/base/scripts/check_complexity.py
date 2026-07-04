"""Fail if any block in a radon JSON report has cyclomatic-complexity grade D, E, or F.

Grade C is the ceiling. Split any failing block into named helpers.

Usage: python scripts/check_complexity.py build/complexity.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

FAILING_GRADES = frozenset({"D", "E", "F"})


def main() -> int:
    report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    failures = [
        f"{path}:{block['lineno']} {block['name']} — grade {block['rank']}"
        f" (complexity {block['complexity']})"
        for path, blocks in report.items()
        if isinstance(blocks, list)  # radon reports per-file errors as dicts
        for block in blocks
        if block.get("rank") in FAILING_GRADES
    ]
    if failures:
        print("Complexity gate failed — split these blocks into named helpers:")
        for line in failures:
            print(f"  {line}")
        return 1
    print("Complexity gate passed: no D/E/F grade blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
