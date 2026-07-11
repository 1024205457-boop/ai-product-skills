---
name: ai-data-update-workflow
description: Run or design safe AI-assisted data update workflows for recurring reports, spreadsheets, dashboards, and anomaly checks, with source validation, scoped writes, read-back checks, and anomaly explanations. Use when the user asks to update data, automate weekly metrics, validate spreadsheets, compare week-over-week values, or design a data operations copilot.
---

# AI Data Update Workflow

Use AI as an operator with guardrails. The lesson: data updates look simple, but the dangerous failures are stale sources, wrong periods, shifted columns, denominator mistakes, silent anomalies, and unverified writes.

## Hard-Won Rules

1. Never update before confirming the period and source. Many bad updates come from using yesterday's file, last week's date, or an old export.
2. Locate cells by headers and dates, not row numbers. Rows move. Hardcoded positions quietly corrupt dashboards.
3. Read back after writing. A successful script run is not proof the right values landed in the right place.
4. Make denominators explicit. Conversion rate, completion rate, and coverage rate are meaningless without a named denominator.
5. Flag anomalies instead of smoothing them away. Large jumps, zeros, missing rows, and denominator drops need a note.
6. Preserve manual edits. Only write the intended range or table. Do not rewrite unrelated formulas, notes, or formatting.

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

## Beginner Implementation Paths

Choose the simplest path that matches the real source:

1. **CSV/XLSX export path:** safest for beginners. Export raw data, run a local script to aggregate it, then paste or write the result.
2. **API/Cookie path:** use only when the internal system has stable request endpoints and the operator can provide a short-lived cookie/token securely. Never commit cookies.
3. **Playwright path:** use when there is no API and data must be downloaded from a web UI. Use it to log in, click export, and save a file; do not let it blindly edit dashboards without read-back checks.

For beginner automation, first replace manual pivot tables with a script that reads raw detail rows and outputs pivot-like summary tables. Only automate writing back after the generated pivot output is trusted.

If the main question is whether to use API/Cookie or Playwright, use the separate `api-vs-playwright-automation` skill.

## Pitfall Checks

- Is the date range exactly the requested one?
- Are all required dimensions present?
- Are row counts and non-null counts plausible?
- Did any metric become zero because the source was empty?
- Did formulas survive after writing?
- Did the read-back match the intended output?
- Is every abnormal movement explained or explicitly marked unknown?

Use:

- `scripts/check_csv_quality.py` for basic CSV quality checks.
- `references/safety-rules.md` for guardrails.
- `references/beginner-automation-examples.md` for a mock-data example that replaces a pivot table and reads text-detail records.
- `references/raw-detail-to-pivot-script.md` when the user needs to turn raw user-state tables and touch-history tables into an automatically generated pivot table.
- `scripts/build_detail_pivot.py` as a starter script for generating Excel pivot-style summary sheets from raw detail CSV files.
