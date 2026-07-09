# Private-Domain Content Pipeline

## Pipeline

```text
source facts -> generation -> factual validation -> deduplication -> channel formatting -> human review -> deployment -> metric review
```

## Prompt Contract

```text
Role:
User segment:
Lifecycle stage:
Goal:
Verified facts:
Forbidden claims:
Tone:
Channel:
Output schema:
```

## Review Checklist

- Does the message match the lifecycle stage?
- Are all factual claims supported by the fact list?
- Does it avoid price, policy, medical, legal, or performance claims unless sourced?
- Is the call to action clear?
- Is the tone appropriate for the relationship?
- Is it too similar to recent content?
- Does it respect frequency and consent rules?

## Metrics

- Generation pass rate.
- Review pass rate.
- Duplicate rejection rate.
- Reply rate.
- Click-through rate.
- Conversion contribution.
- Complaint or unsubscribe rate.
