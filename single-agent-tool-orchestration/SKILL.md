---
name: single-agent-tool-orchestration
description: Design or review a single-Agent plus tools workflow where model reasoning must be constrained by stages, business events, scheduled follow-ups, source-of-truth data, and redline handoff rules. Use when the user asks about Agent architecture, tool-calling rules, event/TODO design, memory boundaries, or why a workflow is not multi-Agent.
---

# Single Agent Tool Orchestration

Use this when an Agent must complete a business workflow, not just chat. The core lesson: do not let the model freely decide tools from scratch each turn. Give it a light orchestration layer made of stages, events, tool contracts, state memory, and redline fallbacks.

## Hard-Won Rules

1. Name the architecture honestly. If there is one model coordinating tools and code, call it "single Agent + toolized code + event/TODO drive", not multi-Agent.
2. Separate reasoning from execution. Let the model understand intent, stage, and wording. Let deterministic tools handle identity, status, factual data, message delivery, future tasks, and handoff.
3. Every future action needs a real scheduled task. A note in the model response is not a reminder. If something must happen later, create a TODO/task now.
4. Every user-visible message needs a send action. Drafting text is not sending. If the user should see it, a message tool must be called and checked.
5. Facts must come from their source of truth. Membership, order status, learning data, prices, policies, and quotas should come from tools, databases, or approved knowledge sources.
6. Redlines beat conversion or completion. Complaints, privacy issues, unsafe claims, policy uncertainty, or repeated tool failure should route to human assistance.

## Workflow

1. Define the user journey and success moment.
2. Split the journey into stages with entry conditions, exit conditions, trigger events, and forbidden actions.
3. List business events that wake the Agent, such as user message, account binding, behavior event, scheduled follow-up, purchase, cancellation, or service closeout.
4. For each stage, write tool contracts:
   - trigger condition.
   - required inputs.
   - source of truth.
   - success condition.
   - retry and fallback.
   - whether it creates user-visible output.
5. Define memory boundaries:
   - store stable state and decision signals.
   - do not store data that should be queried live.
   - append important state changes with timestamps.
6. Add an audit checklist before launch:
   - required tool was called.
   - data source was used.
   - message was actually sent.
   - future task was actually scheduled.
   - frequency and redline checks passed.

## Pitfall Checks

- Did the model answer a user without sending through the official channel?
- Did it promise a later follow-up without creating a task?
- Did it mention user-specific facts without querying the relevant tool?
- Did it keep selling after refusal, complaint, or opt-out?
- Did it retry forever instead of handing off after repeated tool failure?
- Did it route a user by what they claimed instead of verified account/status data?

Read `references/tool-contracts.md` when writing implementation-facing tables.

