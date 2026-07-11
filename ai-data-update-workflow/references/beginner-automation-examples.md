# Beginner Automation Examples

This reference is for beginners who currently update reports by opening exports, making pivot tables, and copying numbers into a weekly dashboard.

## Example 1: Replace a Pivot Table With a Script

### Mock Raw Data

Save this as `mock_events.csv`:

```csv
date,user_id,channel,event,amount
2026-07-01,U001,wechat,view,0
2026-07-01,U001,wechat,book,0
2026-07-01,U002,community,view,0
2026-07-02,U003,wechat,view,0
2026-07-02,U003,wechat,pay,199
2026-07-02,U004,ad,view,0
2026-07-02,U004,ad,book,0
```

Manual pivot goal:

- Rows: `channel`
- Columns/metrics: views, bookings, payments, revenue
- Derived metrics: booking rate = bookings / views, pay rate = payments / views

### Minimal Python Script

Save as `weekly_summary.py`:

```python
import csv
from collections import defaultdict

input_file = "mock_events.csv"
output_file = "weekly_summary.csv"

summary = defaultdict(lambda: {
    "views": 0,
    "bookings": 0,
    "payments": 0,
    "revenue": 0.0,
})

with open(input_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    required = {"date", "user_id", "channel", "event", "amount"}
    missing = required - set(reader.fieldnames or [])
    if missing:
        raise SystemExit(f"Missing columns: {sorted(missing)}")

    for row in reader:
        channel = row["channel"]
        event = row["event"]
        amount = float(row["amount"] or 0)

        if event == "view":
            summary[channel]["views"] += 1
        elif event == "book":
            summary[channel]["bookings"] += 1
        elif event == "pay":
            summary[channel]["payments"] += 1
            summary[channel]["revenue"] += amount

with open(output_file, "w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "channel",
        "views",
        "bookings",
        "payments",
        "revenue",
        "booking_rate",
        "pay_rate",
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for channel, m in sorted(summary.items()):
        views = m["views"]
        writer.writerow({
            "channel": channel,
            "views": views,
            "bookings": m["bookings"],
            "payments": m["payments"],
            "revenue": round(m["revenue"], 2),
            "booking_rate": round(m["bookings"] / views, 4) if views else "",
            "pay_rate": round(m["payments"] / views, 4) if views else "",
        })

print(f"Wrote {output_file}")
```

Run:

```bash
python weekly_summary.py
```

What this replaces:

- No manual pivot table.
- No hand-counting.
- Denominators are explicit.
- The output can be compared week over week.

## Example 2: Read Detailed Diary Logs

Some products do not only have event rows. They also have diary-like operation logs, such as "teacher called parent", "student missed class", or "user complained".

### Mock Diary Data

Save as `mock_diary.csv`:

```csv
date,user_id,operator,note
2026-07-01,U001,teacher_a,家长说孩子最近图形题听不懂，约了周三直播课
2026-07-01,U002,teacher_b,用户觉得提醒太频繁，要求减少推送
2026-07-02,U003,teacher_a,孩子完成试听，家长问是否有暑期班优惠
2026-07-02,U004,teacher_c,电话未接通，准备明天再跟进
```

### Simple Rule Extraction

```python
import csv

rules = {
    "learning_issue": ["听不懂", "薄弱", "错题", "不会"],
    "push_risk": ["太频繁", "打扰", "退订", "别发"],
    "price_interest": ["优惠", "价格", "多少钱", "活动"],
    "follow_up": ["未接通", "明天", "再跟进"],
}

with open("mock_diary.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        note = row["note"]
        tags = [
            tag for tag, keywords in rules.items()
            if any(keyword in note for keyword in keywords)
        ]
        print(row["date"], row["user_id"], tags, note)
```

Where AI can help:

- Summarize long notes.
- Classify ambiguous notes.
- Extract action items.

Where code should stay in charge:

- Reading rows.
- Matching user IDs.
- Writing tags.
- Counting tag frequency.
- Keeping original notes unchanged.

## Example 3: Cookie vs Playwright

### Cookie/API Path

Use this when:

- The page calls a stable API endpoint.
- You can inspect request parameters.
- The operator can paste a temporary cookie or token at runtime.

Beginner shape:

```text
1. Operator exports cookie into local environment variable.
2. Script requests `/api/report?start=2026-07-01&end=2026-07-07`.
3. Script saves raw JSON/CSV.
4. Script validates fields and row count.
5. Script writes summary CSV.
```

Rules:

- Do not commit cookies.
- Do not paste cookies into prompts.
- Prefer read-only export endpoints.
- Log the request period and export time.

### Playwright Path

Use this when:

- There is no documented API.
- The only stable operation is "open page -> choose date -> click export".
- Login requires browser session or SSO.

Beginner shape:

```text
1. Open browser with Playwright.
2. Use existing logged-in browser profile or manual login.
3. Navigate to report page.
4. Select date range.
5. Click export.
6. Save downloaded CSV.
7. Run the same validation and summary script.
```

Rules:

- Playwright should fetch/export first, not directly edit dashboards.
- Always keep downloaded raw files.
- Add screenshot or HTML snapshot if selectors are unstable.
- After any write-back, read the destination and compare values.

## Example 4: Safe Write-Back Checklist

Before writing into a dashboard:

- Target period confirmed.
- Raw export saved.
- Summary generated.
- Required metrics non-empty.
- Denominators named.
- Previous period comparison checked.
- Destination located by header/date, not row number.

After writing:

- Read back all written values.
- Compare read-back with summary CSV.
- Add anomaly notes.
- Report exactly what changed.

