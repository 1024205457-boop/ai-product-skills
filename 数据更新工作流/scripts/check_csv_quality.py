#!/usr/bin/env python3
import csv
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_csv_quality.py <file.csv> [required_field,...]")
        return 2

    path = Path(sys.argv[1])
    required = sys.argv[2].split(",") if len(sys.argv) > 2 and sys.argv[2] else []

    if not path.exists():
        print(f"[FAIL] Missing file: {path}")
        return 1

    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)

    missing_fields = [field for field in required if field not in headers]
    empty_required = []
    for field in required:
        if field in headers:
            empty_count = sum(1 for row in rows if not str(row.get(field, "")).strip())
            if empty_count:
                empty_required.append((field, empty_count))

    print(f"file: {path}")
    print(f"rows: {len(rows)}")
    print(f"columns: {len(headers)}")

    if missing_fields:
        print(f"[FAIL] missing required fields: {', '.join(missing_fields)}")
        return 1

    if empty_required:
        for field, count in empty_required:
            print(f"[WARN] required field has empty values: {field} ({count})")
    else:
        print("[OK] required fields present and non-empty")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
