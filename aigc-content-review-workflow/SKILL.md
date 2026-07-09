---
name: aigc-content-review-workflow
description: Design AIGC content generation, evaluation, badcase diagnosis, and iteration workflows. Use when the user asks about AI image/text generation quality, benchmark evaluation, review rubrics, content safety, or model-output improvement.
---

# AIGC Content Review Workflow

Treat AIGC as a production pipeline: generate, review, diagnose, iterate, and measure adoption.

## Workflow

1. Define the generation task: text, image, video, multimodal, editing, or transformation.
2. Define user value: creation, editing, understanding, personalization, or efficiency.
3. Build the review rubric:
   - functional value.
   - controllability.
   - consistency with instruction.
   - fluency or visual quality.
   - stability.
   - safety and compliance.
4. Run benchmark comparison when possible.
5. Tag badcases by scenario, failure type, severity, and suspected cause.
6. Convert badcases into product requirements, prompt changes, model feedback, or UI improvements.
7. Track metrics: generation success rate, adoption rate, edit rate, export rate, complaint rate, and review score.

Read `references/review-rubric.md` for a reusable rubric.
