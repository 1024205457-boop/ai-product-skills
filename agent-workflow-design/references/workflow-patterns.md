# Agent Workflow Patterns

## Single Agent + Tools

Use when one role can complete the full journey and tools provide external facts or actions.

Best for:

- Shopping guides
- Learning advisors
- Customer service assistants
- Internal operation copilots

Risk:

- The model may blend intent recognition, planning, and execution.
- Add event rules and tool contracts to improve controllability.

## Event/TODO-Driven Agent

Use when the Agent must act across time.

Design:

| Element | Definition |
| --- | --- |
| Trigger | User message, system event, scheduled TODO, status change |
| State | Current phase, user profile, previous actions, pending tasks |
| Action | Message, tool call, memory update, escalation |
| Guardrail | Frequency cap, source-backed facts, no hallucination |

## Tool Contract Template

```text
Tool name:
Purpose:
When to call:
Required inputs:
Source of truth:
Success condition:
Failure handling:
User-facing output rule:
Logging fields:
```

## Redline Template

Escalate to a human when:

- User complains, threatens, or asks for refund/legal/medical/financial judgment.
- The answer requires unavailable price, policy, inventory, or learning data.
- Tool results conflict.
- The model is unsure about a high-impact recommendation.
