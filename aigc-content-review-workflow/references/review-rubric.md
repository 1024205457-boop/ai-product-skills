# AIGC Review Rubric

## Five-Point Scale

| Score | Meaning |
| --- | --- |
| 5 | Excellent, directly usable, no obvious issue |
| 4 | Good, minor issue but usable |
| 3 | Acceptable, needs user correction |
| 2 | Poor, key requirement partially failed |
| 1 | Failed, unusable or unsafe |

## Dimensions

- Functional value: solves the intended generation or editing task.
- Instruction following: follows user prompt, constraints, and references.
- Controllability: user can predict and adjust output.
- Consistency: style, identity, layout, or object remains stable.
- Fluency/beauty: output looks or reads naturally.
- Speed and feedback: waiting time and progress feedback are acceptable.
- Safety: avoids harmful, misleading, or policy-sensitive content.

## Badcase Schema

```text
case_id:
scenario:
input:
expected_output:
actual_output:
score:
failure_type:
severity:
suspected_cause:
recommended_fix:
```
