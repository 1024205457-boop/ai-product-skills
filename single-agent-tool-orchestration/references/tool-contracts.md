# Tool Contract Template

Use this table when turning an Agent idea into an executable workflow.

| Field | What to Specify | Common Failure |
| --- | --- | --- |
| Tool name | Human-readable action, not only API name | Interviewers do not understand internal tool names |
| Trigger | Exact condition for calling | Model calls it whenever it feels useful |
| Required input | Where each parameter comes from | Model guesses missing IDs, dates, or user state |
| Source of truth | Database, API, knowledge file, or user profile | Model treats user statements as verified facts |
| Success condition | What proves the action happened | Text was drafted but not sent or persisted |
| Failure fallback | Retry count, alternate route, human handoff | Infinite retry or silent failure |
| State write | What memory/profile field changes | Future turns lose the decision state |
| Metric | How to evaluate it | Only text quality is evaluated |

## Minimum Tool Groups

- Identity/status: bind account, query status, verify eligibility.
- Factual data: query behavior, order, learning, inventory, coupon, or price data.
- User-visible action: send message, create link, issue coupon, change address, submit ticket.
- Future action: create task, cancel task, reschedule task.
- State: read memory, write memory, archive final state.
- Risk: request human assistance, transfer ownership, stop proactive messaging.

## Output Checklist

- Use product-language names first, API names second.
- Explain why code/tools own deterministic actions.
- Keep the Agent responsible for interpretation and response synthesis.
- Keep source-of-truth facts outside model memory unless deliberately cached.

