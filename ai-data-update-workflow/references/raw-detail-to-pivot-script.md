# Raw Detail Data to Pivot Script

This is the reference to read when the goal is: "I have raw user-state rows and touch-history rows, and I want a script to automatically produce the same output as a manual pivot table."

The examples below use sanitized mock data, but the shape mirrors common AI product operations data:

- **user state table:** long-lived user status, segment, intent, risk flag, tags, latest summary.
- **touch history table:** every user/operator/Agent action, message, click, follow-up, conversion, complaint, or handoff.

## 1. Start From the Manual Pivot Table

Before writing code, write down the pivot table exactly as a human would build it.

Example manual pivot:

```text
Rows:
- date
- scene

Columns / values:
- state_count: count of state_id
- active_users: distinct count of user_id
- high_intent_users: distinct count where intent_level = high
- risk_users: distinct count where risk_flag = 1
- followup_count: count of touch records where event_type = followup
- complaint_count: count of touch records where event_type = complaint

Filters:
- date between 2026-07-01 and 2026-07-07
- exclude test users
```

This becomes the script contract. Do not start from code first.

## 2. Raw User State Example

Save as `user_state.csv`:

```csv
state_id,user_id,created_at,scene,intent_level,risk_flag,tags,latest_summary
S001,U001,2026-07-01 09:12:00,trial_class,high,0,"试听,数学,待跟进","家长关注一年级数学思维，想先看直播课"
S002,U002,2026-07-01 10:20:00,private_push,medium,1,"推送频繁,退订风险","家长反馈最近提醒太频繁，需要降低触达"
S003,U003,2026-07-02 14:05:00,renewal,high,0,"续费,价格咨询","家长询问暑期班价格和优惠"
S004,U004,2026-07-02 16:30:00,trial_class,low,0,"未接通,二次跟进","电话未接通，明天再次跟进"
S005,U001,2026-07-03 19:40:00,trial_class,high,0,"完课,正反馈","孩子完成试听，家长反馈课程节奏可以"
```

Important fields:

| Field | Meaning | Pivot use |
| --- | --- | --- |
| `state_id` | unique state row | count records |
| `user_id` | user key | distinct users |
| `created_at` | state update time | date grouping |
| `scene` | business scenario | row dimension |
| `intent_level` | user intent | high intent count |
| `risk_flag` | risk signal | risk user count |
| `tags` | comma-separated tags | tag frequency sheet |
| `latest_summary` | text detail | source for human review, not a metric by itself |

## 3. Raw Touch History Example

Save as `touch_history.csv`:

```csv
touch_id,user_id,created_at,operator,channel,event_type,note
T001,U001,2026-07-01 09:20:00,teacher_a,wechat,followup,"发送试听课提醒，家长已读"
T002,U002,2026-07-01 10:28:00,teacher_b,wechat,complaint,"家长说提醒太频繁，要求减少推送"
T003,U003,2026-07-02 14:12:00,teacher_a,phone,followup,"解释暑期班价格，家长要求发优惠说明"
T004,U004,2026-07-02 16:35:00,teacher_c,phone,no_answer,"电话未接通，计划明天再打"
T005,U001,2026-07-03 20:00:00,teacher_a,wechat,conversion,"家长预约下一节直播课"
```

Important fields:

| Field | Meaning | Pivot use |
| --- | --- | --- |
| `touch_id` | unique touch row | count touch records |
| `user_id` | join key to user state | distinct touched users |
| `created_at` | action time | date grouping |
| `operator` | teacher/agent/operator | operator pivot |
| `channel` | wechat/phone/community | channel pivot |
| `event_type` | followup/complaint/conversion/no_answer | metric columns |
| `note` | detailed text | optional AI/manual tagging source |

## 4. Output Pivot Tables

The script should produce an Excel file like `detail_pivot.xlsx` with these sheets:

| Sheet | Purpose |
| --- | --- |
| `state_by_scene` | daily scenario summary from user-state rows |
| `touch_by_operator` | daily operator/channel/event summary from touch history |
| `tag_frequency` | tag counts from user-state tags |
| `quality_checks` | row count, missing fields, date range, duplicate keys |

This is easier for beginners than creating a native Excel pivot table object. It produces the same business output with less Excel automation risk.

## 5. Script Mapping

| Manual pivot action | Script action |
| --- | --- |
| Drag `date` to rows | parse `created_at`, create `date` column |
| Drag `scene` to rows | `groupby(["date", "scene"])` |
| Count state rows | `state_id.nunique()` |
| Distinct count users | `user_id.nunique()` |
| Filter high intent | count distinct users where `intent_level == "high"` |
| Filter risk users | count distinct users where `risk_flag == 1` |
| Drag event type to columns | `pivot_table(columns="event_type")` |
| Count tags | split `tags`, explode rows, group by tag |

## 6. Starter Script

Use `../scripts/build_detail_pivot.py` from this skill folder.

Run:

```bash
python scripts/build_detail_pivot.py \
  --state user_state.csv \
  --touch touch_history.csv \
  --output detail_pivot.xlsx \
  --start 2026-07-01 \
  --end 2026-07-07
```

The script should:

1. load user-state and touch-history CSV.
2. validate required columns.
3. parse dates.
4. filter target period.
5. build pivot-style summary sheets.
6. write Excel output.
7. write quality checks.

## 7. Where AI Fits

AI can help before the pivot script:

- read long `latest_summary` or `note` text.
- classify the text into tags: price_interest, push_risk, complaint, followup_needed.
- summarize reasons for anomalies.

Code should handle:

- counting.
- date filtering.
- distinct users.
- pivot table output.
- read-back and validation.

Do not let AI directly "estimate" metrics from text. Metrics must come from rows.

## 8. Beginner Checklist

Before running:

- raw user-state CSV exported.
- raw touch-history CSV exported.
- target date range confirmed.
- required columns confirmed.
- test users excluded or explicitly included.

After running:

- output Excel opens.
- row counts match raw files after date filtering.
- each sheet has non-empty rows.
- spot-check 3 users manually against raw detail rows.
- compare with previous manual pivot once before trusting automation.

