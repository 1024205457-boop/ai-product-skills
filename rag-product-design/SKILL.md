---
name: rag-product-design
description: Design RAG, AI search, and answer-with-citation product experiences. Use when the user asks about AI search, shopping guide search, knowledge-base Q&A, retrieval strategy, citation quality, query taxonomy, or search evaluation.
---

# RAG Product Design

Design AI search as a user decision flow: understand intent, retrieve evidence, rank results, answer with sources, and support follow-up.

## Workflow

1. Classify the user query: navigational, informational, comparative, constraint-based, troubleshooting, transaction-oriented, or ambiguous.
2. Define searchable objects: products, documents, policies, FAQs, user records, logs, cases, or multimodal assets.
3. Design retrieval:
   - lexical search for exact terms.
   - vector search for semantic matches.
   - filters for structured constraints.
   - reranking for final precision.
4. Design answer generation:
   - cite retrieved evidence.
   - separate facts, recommendations, and assumptions.
   - ask a follow-up only when required for task completion.
5. Define fallback:
   - no result.
   - conflicting sources.
   - low confidence.
   - policy-sensitive question.
6. Define metrics:
   - offline retrieval precision/recall.
   - answer accuracy.
   - citation coverage.
   - click-through rate.
   - reformulation and follow-up rate.
   - task completion or conversion rate.

Read `references/query-taxonomy.md` and `references/evaluation.md` for detailed templates.
