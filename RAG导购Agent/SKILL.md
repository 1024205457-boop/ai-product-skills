---
name: rag-shopping-guide-agent
description: Design or review an AI shopping-guide Agent that turns vague user needs into grounded product recommendations, comparisons, risk checks, and decision support without fabricating prices, links, inventory, ingredients, policies, or claims. Use for ecommerce guide, AI search, product recommendation, RAG QA, ingredient or spec screening, and JD-style AI search scenarios.
---

# RAG Shopping Guide Agent

Use this when the user wants an AI guide that helps people decide what to buy. The lesson: shopping guidance is not "recommend popular products". It must translate fuzzy needs into decision criteria, retrieve grounded product facts, explain trade-offs, and refuse to fill missing facts with model guesses.

## Hard-Won Rules

1. Need understanding is broader than keyword matching. Capture use case, user type, constraints, risk factors, and decision anxiety.
2. Retrieve before judging. Product names, ingredients, specs, prices, stock, coupons, policies, and links must come from approved sources.
3. Say "information insufficient" when the source is incomplete. Do not infer a full ingredient list, latest price, discount, or availability.
4. Give decision evidence, not only product names. Explain match reason, risk, alternatives, and who should avoid the item.
5. Separate recommendation from transaction facts. A model can explain why an item fits; it should not invent purchase links or promotions.
6. Evaluate recall of risks, not just answer fluency. A beautiful recommendation that misses a safety constraint is a bad answer.

## Workflow

1. Parse the user request into:
   - desired outcome.
   - user profile or scenario.
   - constraints and taboos.
   - stated or implied risk factors.
   - missing but necessary clarifications.
2. Build retrieval queries for product facts and domain facts.
3. Retrieve from knowledge base, API, search, or database.
4. Screen each candidate against:
   - must-have criteria.
   - exclusion criteria.
   - risk ingredients/specs/policies.
   - source freshness and completeness.
5. Produce a structured comparison:
   - recommendation.
   - evidence from retrieved facts.
   - risks and unsuitable groups.
   - when to choose an alternative.
   - what information is missing.
6. Add a final grounding check before output.

## Pitfall Checks

- Did the Agent recommend without a complete source record?
- Did it quote a price, stock state, coupon, or link without a source?
- Did it treat "popular" as "suitable"?
- Did it ignore user-specific constraints such as allergy, pregnancy, sensitivity, age, device, or budget?
- Did it give a single answer when comparison is needed?
- Did it bury risk warnings after persuasive copy?

Read `references/grounding-and-risk-checks.md` when defining retrieval fields, risk categories, and evaluation items.

