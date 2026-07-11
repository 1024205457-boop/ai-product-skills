# API/Cookie Path

Use this path when the system has a stable endpoint and the task can be represented as request parameters.

## Typical Manual Workflow

```text
1. Open internal report page.
2. Select date range: 2026-07-01 to 2026-07-07.
3. Select channel: all.
4. Click search.
5. Download CSV or copy table.
6. Make a weekly summary.
```

## API/Cookie Automation Shape

```text
1. Operator provides date range.
2. Operator provides cookie/token at runtime.
3. Script requests report endpoint.
4. Script saves raw response.
5. Script validates fields and row count.
6. Script aggregates metrics.
7. Script outputs summary CSV and anomaly notes.
```

## Credential Handling

Good:

```bash
export REPORT_COOKIE="paste-short-lived-cookie-here"
python fetch_report.py --start 2026-07-01 --end 2026-07-07
```

Bad:

```python
COOKIE = "real_cookie_committed_to_git"
```

Never commit cookies, tokens, user IDs from production, or raw private exports.

## Minimal Python Skeleton

```python
import argparse
import csv
import os
import requests

parser = argparse.ArgumentParser()
parser.add_argument("--start", required=True)
parser.add_argument("--end", required=True)
parser.add_argument("--output", default="raw_report.csv")
args = parser.parse_args()

cookie = os.environ.get("REPORT_COOKIE")
if not cookie:
    raise SystemExit("Missing REPORT_COOKIE environment variable")

url = "https://example.com/api/report"
params = {"start": args.start, "end": args.end}
headers = {"Cookie": cookie}

resp = requests.get(url, params=params, headers=headers, timeout=30)
resp.raise_for_status()
data = resp.json()

rows = data.get("rows", [])
if not rows:
    raise SystemExit("No rows returned; confirm date range and permissions")

required = {"date", "channel", "views", "orders"}
missing = required - set(rows[0].keys())
if missing:
    raise SystemExit(f"Missing fields: {sorted(missing)}")

with open(args.output, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=sorted(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved {len(rows)} rows to {args.output}")
```

## Validation Checklist

- Request URL and parameters logged.
- Date range in response matches requested date range.
- Row count is nonzero.
- Required fields exist.
- Duplicate primary keys checked.
- Empty metrics are flagged.
- Raw response is saved before transformation.

## When Not to Use This Path

- Endpoint changes every session.
- Parameters are encrypted or signed in unknown ways.
- Cookie expires too quickly for repeat runs.
- Terms or permissions do not allow scripted access.
- The task depends on visual UI state that the API does not expose.

