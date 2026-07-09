---
name: private-domain-ai-workflow
description: Design private-domain AI content supply workflows for lifecycle messaging, community content, direct messages, and conversion support. Use when the user asks about AI-generated copy/images for private-domain operations, content review, deduplication, channel adaptation, or human approval.
---

# Private Domain AI Workflow

Build a content supply workflow that supports user lifecycle goals while keeping facts, tone, and frequency controlled.

## Workflow

1. Define lifecycle stage, user state, message goal, and channel.
2. Build content inputs:
   - verified facts.
   - user segment.
   - scenario.
   - call to action.
   - forbidden claims.
3. Run generation with structured output for each channel.
4. Validate factual claims against a source list.
5. Deduplicate against recent content using deterministic similarity checks.
6. Adapt format for channel constraints.
7. Add human review for brand, compliance, and strategy-sensitive content.
8. Track reply rate, click-through, conversion contribution, complaint rate, and content reuse rate.

## Boundary

Use AI for divergent tasks such as copy variants and tone adjustment. Use code for deterministic tasks such as schedule calculation, deduplication, field filling, template insertion, and validation.

Read `references/content-pipeline.md` for the reusable pipeline.
