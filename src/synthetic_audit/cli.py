"""Command-line interface for the deterministic audit report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .validator import validate_records


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate synthetic evidence and emit a stable JSON report")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path, help="compare the generated report with this expected JSON file")
    args = parser.parse_args()

    raw = json.loads(args.input.read_text(encoding="utf-8"))
    report = validate_records(raw)
    rendered = json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n"
    if args.check:
        expected = args.check.read_text(encoding="utf-8")
        if rendered != expected:
            raise SystemExit("report does not match expected JSON")
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
