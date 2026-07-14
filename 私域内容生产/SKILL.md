---
name: private-domain-content-production
description: Design or review a private-domain AI content production workflow for lifecycle messages, copy variants, images, channel adaptation, review, deduplication, frequency control, and conversion support. Use when the user asks about private-domain push, AI copy generation, image generation, marketing content operations, or turning content production into a reusable workflow.
---

# Private Domain Content Production

Use this when AI is used to produce messages or images for private-domain operations. The lesson: content generation alone is not the product. The real workflow is goal definition, source facts, batch generation, review, deduplication, channel adaptation, frequency control, and performance feedback.

## Hard-Won Rules

1. Do not make "filling forms" the product value. The user value is timely, relevant, non-annoying communication that helps a lifecycle goal.
2. Copy and image generation are one content supply chain. Treat text, image, title, CTA, and channel format as one package.
3. Use AI for variation, not unchecked publishing. Brand, fact, policy, and frequency-sensitive content needs review gates.
4. Separate creative from deterministic operations. Let AI draft variants. Let code handle schedules, field insertion, dedupe, export, and validation.
5. Never let generated images carry critical text unless verified. For reliable text, generate background/visuals and overlay text with code or design tooling.
6. Do not publish private assets. Generated images, real campaign data, company templates, and user screenshots should stay out of public repos.

## Workflow

1. Define lifecycle stage, audience segment, channel, user value, and conversion goal.
2. Prepare grounded inputs:
   - approved facts.
   - product or service claims.
   - user segment.
   - CTA.
   - forbidden claims.
   - frequency limit.
   - topic cycle.
   - seasonal context.
   - recent touch history.
   - dedupe keys.
3. Generate copy and visual concepts in batches.
4. Review:
   - factual accuracy.
   - tone and brand fit.
   - image-text consistency.
   - duplicate or repetitive phrasing.
   - risk of over-pushing.
5. Adapt to channel:
   - short DM.
   - community post.
   - poster/card.
   - follow-up message.
6. Export with a human-readable review sheet and track usage/performance.

## Implementation Split

For a given approved copy, explicitly split the workflow into three parts:

1. **Code-inserted facts:** user name, class name, deadline, coupon amount, activity link, teacher name, opt-out text. These should come from CRM/export tables and be inserted by code.
2. **Rotating templates:** opening line, CTA wording, reminder angle, emoji/no-emoji style, send-time batch. These can be selected from a controlled template pool.
3. **AI free generation:** rewrite tone, produce 3-5 variants, adapt to channel length, summarize a long source note into short copy. AI must not invent prices, deadlines, promises, or user-specific facts.

When writing a plan, include a field map and a generation boundary table. Do not only say "AI generates private-domain copy".

## Pitfall Checks

- Is the content useful to the recipient, or only convenient for the operator?
- Are multiple pushes repeating the same intent?
- Are generated images stored or committed publicly?
- Does any visual contain broken text, wrong logo, or misleading product state?
- Are claims traceable to approved facts?
- Is there a frequency or opt-out rule?

Read:

- `references/content-review-gates.md` for review checkpoints.
- `references/copy-splitting-and-generation-boundaries.md` for a beginner-friendly example of how to split one source copy into code fields, rotating templates, and AI-generated variants.
- `references/batch-generation-variables.md` for a batch-generation example that combines provided copy facts, user state, touch history, topic cycles, seasonal variables, dedupe, and frequency control.
