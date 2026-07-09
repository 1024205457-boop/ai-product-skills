---
name: ai-data-update-workflow
description: Run or design safe AI-assisted data update workflows for recurring reports, spreadsheets, dashboards, and anomaly checks. Use when the user asks to update data, automate weekly metrics, validate spreadsheets, compare week-over-week values, or design a data operations copilot.
---

# AI Data Update Workflow

Use AI as an operator with guardrails. It can execute, check, and report, but it must not invent data or silently accept anomalies.

## Workflow

1. Confirm the target period, source files, destination file, and required completeness.
2. Fetch or load data into an inspectable intermediate format.
3. Validate before writing:
   - date range complete.
   - required fields present.
   - row count nonzero.
   - no stale parameters.
   - formulas and denominators explicit.
4. Write with minimal scope and locate targets by headers/dates, not hardcoded row numbers.
5. Read back written values.
6. Compare against previous period and flag large changes.
7. Report normal metrics, anomalies, pending confirmations, and completed steps.

Use `scripts/check_csv_quality.py` for basic CSV quality checks. Read `references/safety-rules.md` for guardrails.
