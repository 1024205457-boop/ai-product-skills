---
name: ai-image-generation-workflow
description: Design batch AI image generation workflows with prompt hierarchy, reference images, scene pools, manual quality review, and production handoff. Use when the user asks about generating cards, posters, social images, marketing visuals, or AIGC image review.
---

# AI Image Generation Workflow

Design image generation as a controlled production workflow, not a one-shot prompt.

## Workflow

1. Define image type, size, channel, brand constraints, and final usage.
2. Choose generation mode:
   - text-to-image for loose ideation.
   - image-to-image for style/layout consistency.
   - generated background plus code overlay for reliable text.
3. Write prompt hierarchy:
   - highest priority: mandatory text or object.
   - high priority: layout and composition.
   - normal priority: scene and atmosphere.
   - negative constraints: what must not appear.
4. Use curated scene pools for diversity with control.
5. Generate in batches and record parameters.
6. Review manually for text accuracy, anatomy/object issues, brand fit, safety, and layout.
7. Store accepted outputs with version and usage notes.

Read `references/prompt-and-review.md` for prompt and review templates.
