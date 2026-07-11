# Playwright Path

Use this path when the reliable workflow is browser-based: login, choose filters, click export, download a file, or take screenshots.

## Typical Manual Workflow

```text
1. Open report backend.
2. Log in through SSO or QR code.
3. Select date range.
4. Click query.
5. Click export.
6. Wait for CSV download.
7. Check downloaded file and build summary.
```

## Playwright Automation Shape

```text
1. Open browser.
2. Use existing login state or allow manual login.
3. Navigate to report page.
4. Fill date range and filters.
5. Click export.
6. Save downloaded CSV.
7. Run deterministic validation/aggregation script.
```

## Minimal Node Skeleton

```js
import { chromium } from "playwright";

const browser = await chromium.launch({ headless: false });
const context = await browser.newContext({ acceptDownloads: true });
const page = await context.newPage();

await page.goto("https://example.com/report");

// If login is manual/SSO, pause and let the operator finish it.
if (await page.getByText("Login").isVisible().catch(() => false)) {
  console.log("Please log in manually, then press Enter in terminal.");
  await new Promise(resolve => process.stdin.once("data", resolve));
}

await page.getByLabel("Start date").fill("2026-07-01");
await page.getByLabel("End date").fill("2026-07-07");
await page.getByRole("button", { name: "Query" }).click();

const downloadPromise = page.waitForEvent("download");
await page.getByRole("button", { name: "Export" }).click();
const download = await downloadPromise;
await download.saveAs("raw_report.csv");

await page.screenshot({ path: "report-exported.png", fullPage: true });
await browser.close();
```

## Selector Rules

Prefer:

- `getByRole`
- `getByLabel`
- stable test IDs
- visible text that product owners control

Avoid:

- long CSS chains.
- auto-generated class names.
- nth-child selectors unless there is no alternative.

## Validation Checklist

- Screenshot saved after filters are applied.
- Download file exists.
- File modified time matches current run.
- CSV headers match expected fields.
- Date range inside file matches selected date range.
- Row count is plausible.

## When Not to Use This Path

- A stable API endpoint already exists.
- The run needs high-frequency batch execution.
- UI selectors change daily.
- The script would click destructive buttons.
- There is no read-back or downloaded artifact to verify.

## Safe Write-Back Rule

For beginners, Playwright should usually stop at export/download. If it must write back:

```text
1. Write only one scoped table/range.
2. Take screenshot before and after.
3. Read the resulting value from the page.
4. Compare with source summary.
5. Stop on first mismatch.
```

