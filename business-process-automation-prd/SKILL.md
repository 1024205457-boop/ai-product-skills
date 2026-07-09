---
name: business-process-automation-prd
description: Convert manual business operations into AI workflow automation PRDs. Use when the user asks to productize repetitive operations, define human-AI boundaries, automate forms/tasks/data flows, or write requirements for an internal AI tool.
---

# Business Process Automation PRD

Turn manual operations into a workflow system with clear ownership, data inputs, exceptions, and measurable efficiency gains.

## Workflow

1. Map the current process:
   - trigger.
   - actors.
   - inputs.
   - decisions.
   - outputs.
   - failure points.
2. Separate AI, code, and human responsibilities:
   - AI handles semantic, creative, or judgment-assist tasks.
   - code handles deterministic calculations, formatting, scheduling, validation, and API calls.
   - humans handle approvals, strategy, edge cases, and risk judgment.
3. Design target workflow with states, permissions, audit logs, and rollback.
4. Define PRD sections:
   - background and problem.
   - user roles.
   - scope and non-scope.
   - core workflow.
   - data schema.
   - exception handling.
   - metrics.
   - launch plan.
5. Add acceptance criteria and risk checklist.

Read `references/prd-template.md` for a reusable template.
