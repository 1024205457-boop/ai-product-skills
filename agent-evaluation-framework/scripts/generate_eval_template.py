#!/usr/bin/env python3
import csv
import sys
from pathlib import Path

FIELDS = [
    "case_id",
    "user_input",
    "user_context",
    "expected_intent",
    "expected_phase",
    "required_tools",
    "forbidden_tools",
    "required_sources",
    "expected_answer_points",
    "redline_tags",
    "pass_criteria",
    "actual_intent",
    "actual_phase",
    "actual_tools",
    "actual_answer",
    "pass_fail",
    "failure_reason",
]


def main() -> int:
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("agent_eval_template.csv")
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
    print(f"Created {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
