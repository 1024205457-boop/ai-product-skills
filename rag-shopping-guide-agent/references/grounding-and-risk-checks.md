# Grounding and Risk Checks

## Retrieval Fields

| Field | Why It Matters | Never Guess |
| --- | --- | --- |
| Product identity | Prevents mixing variants | Brand, exact model, SKU, version |
| Full facts | Enables screening | Full ingredient list, specs, curriculum, service terms |
| Transaction facts | High hallucination risk | Price, coupon, inventory, purchase link |
| Suitability facts | Drives personalization | Skin type, age, use case, device, learning level |
| Policy facts | Legal and trust risk | Refund, warranty, renewal, safety warnings |
| Source metadata | Enables confidence | Source, update time, completeness |

## Decision Output

Use a compact structure:

| Item | Match Reason | Risk / Caveat | Best For | Avoid If | Source Completeness |
| --- | --- | --- | --- | --- | --- |

Then add:

- Why the top choice fits.
- What trade-off the user is accepting.
- What must be verified before purchase.

## Evaluation Items

- Need parsing accuracy.
- Product match accuracy.
- Risk recall.
- Fact grounding.
- Missing-information handling.
- Comparison usefulness.
- Unsupported claim rate.

