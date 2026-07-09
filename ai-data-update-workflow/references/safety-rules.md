# Data Update Safety Rules

## Must Do

- Confirm date range before writing.
- Keep raw input files separate from output files.
- Validate every required field.
- Use explicit formulas and denominators.
- Flag large period-over-period changes.
- Stop after repeated identical failures.

## Must Not Do

- Do not invent missing values.
- Do not write incomplete periods without confirmation.
- Do not assume spreadsheet structure is unchanged.
- Do not suppress anomalies because they seem plausible.
- Do not mix business judgment with mechanical validation.

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
