# Image Generation Prompt and Review

## Prompt Template

```text
[Highest priority]
Must include:
Must not change:

[Layout]
Canvas:
Main subject:
Text area:
Composition:

[Scene]
Background:
Lighting:
Mood:
Variation requirement:

[Reference]
Use reference image for:
Do not use reference image for:

[Negative constraints]
No:
```

## Human Review Checklist

- Text is correct and readable.
- Main object matches the prompt.
- Layout leaves room for downstream elements.
- No unsafe, distorted, or confusing content.
- Visual style fits the intended channel.
- Image is not too similar to previous accepted outputs.
- File is named and stored according to the handoff rule.

## Common Failure Types

- Text typo or missing text.
- Reference identity drift.
- Scene repetition.
- Overcrowded layout.
- Wrong object count.
- Unusable crop.
- Low visual readability.
