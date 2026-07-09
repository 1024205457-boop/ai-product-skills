---
name: agent-workflow-design
description: Design controllable AI Agent workflows for product scenarios. Use when the user asks to design Agent phases, tool-calling rules, event/TODO triggers, memory boundaries, human handoff, or single-Agent versus multi-Agent architecture.
---

# Agent Workflow Design

Design the Agent around task completion, not open-ended conversation.

## Workflow

1. Define the user, task, success moment, and business outcome.
2. Choose the architecture:
   - Single Agent plus tools for narrow workflows.
   - Workflow Agent for phased journeys.
   - Multi-Agent only when responsibilities truly require separate agents.
3. Split the journey into phases with entry conditions, exit conditions, and trigger events.
4. Define which steps are handled by model reasoning, deterministic code, tools, memory, RAG, and human review.
5. Write tool-calling contracts:
   - When to call the tool.
   - Required inputs.
   - Source of truth.
   - Failure fallback.
   - Whether user-facing messages require a send-message tool.
6. Add future-task rules for reminders, follow-ups, and scheduled actions.
7. Add redline escalation rules for safety, complaints, transactions, or policy-sensitive answers.
8. Produce an implementation-facing workflow table and a product-facing explanation.

## Output

Return:

- Architecture choice and reason.
- Phase table.
- Tool list and calling rules.
- Event/TODO design.
- Memory and RAG boundaries.
- Fallback and escalation rules.
- Metrics and evaluation hooks.

Read `references/workflow-patterns.md` for reusable patterns.
