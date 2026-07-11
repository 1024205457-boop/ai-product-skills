---
name: api-vs-playwright-automation
description: Design or review beginner-friendly automation scripts that choose between API/Cookie requests and Playwright browser automation for data export, dashboard updates, report refreshes, or internal tool operations. Use when the user asks whether to use API, cookie, browser automation, Playwright, web scraping, dashboard automation, replacing manual exports, or writing scripts for internal systems.
---

# API vs Playwright Automation

Use this when a workflow can be automated either by calling an endpoint or by driving a browser. The core lesson: API scripts and Playwright scripts solve different problems. Do not choose by what feels easier in the first 10 minutes; choose by stability, permission, observability, and failure risk.

## Decision Rule

Prefer **API/Cookie scripts** when:

- the page has a stable request endpoint.
- inputs are clear: date range, page number, filters, IDs.
- output is structured JSON/CSV.
- the task is mostly export, aggregation, or read-only update.
- credentials can be supplied safely at runtime.

Prefer **Playwright** when:

- there is no stable API or endpoint is hard to reproduce.
- login depends on SSO, QR code, browser profile, or human confirmation.
- the only reliable path is UI clicks: open report, choose date, click export.
- you need screenshots, visual checks, or UI regression evidence.

Avoid both until clarified when:

- the task may violate site terms.
- the workflow needs destructive writes.
- credentials/cookies would need to be stored in code.
- the source period, owner, or destination is unclear.

## Beginner Workflow

1. Describe the manual workflow exactly: pages visited, filters selected, buttons clicked, copied fields, final destination.
2. Decide whether the source is **structured endpoint** or **UI-only workflow**.
3. Build a read-only prototype first:
   - API path: fetch data and save raw JSON/CSV.
   - Playwright path: log in, export/download, save raw file.
4. Validate raw output: date range, row count, required fields, duplicates, empty values.
5. Transform data in a deterministic script.
6. Only then automate write-back, with read-back verification.

## Output Contract

When designing an automation, produce:

- decision: API/Cookie, Playwright, or hybrid.
- reason for the decision.
- manual workflow being replaced.
- inputs and outputs.
- credential handling plan.
- failure cases and fallback.
- script skeleton or pseudocode.
- validation and read-back checks.

## Common Hybrid Pattern

Use Playwright only to obtain the export file, then use deterministic scripts for processing:

```text
Playwright login/export -> raw CSV -> validation script -> summary CSV -> manual review or scoped write-back
```

This is often safer than letting Playwright directly edit dashboards.

## References

- Read `references/api-cookie-path.md` when the source has a visible API request, export endpoint, or cookie-based session.
- Read `references/playwright-path.md` when the workflow depends on browser UI, downloads, SSO, screenshots, or selectors.
- Read `references/path-decision-table.md` when comparing both approaches for a product/design document.

