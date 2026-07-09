---
name: agent-evaluation-framework
description: Design evaluation systems for AI Agents, including golden datasets, scoring rubrics, tool-call checks, redline vetoes, and online-offline metric mapping. Use when the user asks how to evaluate an Agent, define accuracy, create test cases, or build acceptance criteria.
---

# Agent Evaluation Framework

Evaluate whether the Agent completes the right task safely, not just whether the text sounds good.

## Workflow

1. Define the task boundary and user journey.
2. Split evaluation into five layers:
   - intent and phase judgment.
   - factual grounding.
   - tool and event execution.
   - response quality.
   - safety and compliance.
3. Build a golden dataset with real or synthetic user inputs, expected state, expected tools, expected sources, and unacceptable outputs.
4. Define scoring:
   - binary pass/fail for redlines.
   - 1-5 rating for response quality.
   - exact match or tolerance for structured fields.
5. Connect offline metrics to online metrics such as reply rate, task completion, click-through, conversion, complaint rate, and escalation rate.
6. Produce an acceptance checklist before launch.

Use `scripts/generate_eval_template.py` to create a CSV template. Read `references/rubric.md` for scoring details.
