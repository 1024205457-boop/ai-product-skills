# Data Update Safety Rules

Use these rules when updating recurring data files. The common failure is not "AI cannot calculate"; it is updating the wrong period, wrong denominator, wrong cells, or silently accepting an anomaly.

## Must Do

- Confirm date range, source file/export time, destination, and owner before writing.
- Keep raw input files separate from output files.
- Validate every required field, dimension, row count, and duplicate key.
- Use explicit formulas, numerators, and denominators.
- Locate target cells by table, header, and date key.
- Keep writes scoped to intended rows/cells.
- Read back destination values after writing.
- Flag large period-over-period changes.
- Stop after repeated identical failures.

## Must Not Do

- Do not invent missing values.
- Do not write incomplete periods without confirmation.
- Do not assume spreadsheet structure is unchanged.
- Do not suppress anomalies because they seem plausible.
- Do not mix business judgment with mechanical validation.
- Do not invent explanations for metric movement.
- Do not overwrite unrelated formulas, notes, formatting, or manual edits.

## Anomaly Notes

Use short, explicit notes:

- "Metric increased because numerator rose while denominator was stable."
- "Metric dropped because denominator expanded faster than numerator."
- "Zero value appears source-driven; confirm export completeness."
- "Cannot explain movement from available data; mark for owner confirmation."

## Report Template

```text
Data Update Report (<period>)

Completed:
- Source loaded:
- Validation:
- Output written:
- Read-back check:

Normal metrics:
- metric: current (previous, change)

Anomalies:
- metric: current (previous, change, reason needs confirmation)

Pending:
- items requiring human judgment
```
