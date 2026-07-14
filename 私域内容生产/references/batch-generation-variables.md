# Batch Generation Variables

Use this reference when the goal is: "Given approved copy information, generate private-domain messages in batches while respecting topic cycles, seasonal context, dedupe, and frequency control."

Do not hardcode real private data in the skill. Use generic tables like:

- user state table.
- touch history table.
- campaign facts table.
- topic cycle table.
- seasonal context table.
- template pool.

## 1. Input Tables

### Campaign Facts

These are approved facts. AI can rewrite them, but cannot invent new facts.

```csv
campaign_id,product_name,core_offer,deadline,cta,link,forbidden_claims
C001,数学思维直播课,本周可预约一节体验课,2026-07-15,点击预约,https://example.com/book,"一定提分;仅剩3席;名师保过"
```

### User State

```csv
user_id,parent_name,student_grade,segment,intent_level,risk_flag,weakness_tag,last_summary
U001,小雨妈妈,一年级,trial_parent,high,0,图形找规律,"最近看过数学思维课，家长关注图形题"
U002,乐乐爸爸,二年级,quiet_user,medium,1,计算粗心,"近期触达较多，家长回复变少"
U003,安安妈妈,一年级,active_parent,high,0,应用题理解,"家长主动问过暑期课安排"
```

### Touch History

```csv
user_id,touch_date,channel,topic_key,message_hash,result
U001,2026-07-08,wechat,math_live,hash_001,clicked
U002,2026-07-09,wechat,math_live,hash_002,no_reply
U002,2026-07-10,wechat,renewal,hash_003,complaint
U003,2026-07-05,community,summer_plan,hash_004,replied
```

### Topic Cycle

Use topic cycles to avoid pushing the same angle every day.

```csv
week,topic_key,angle,priority
2026-W28,math_live,薄弱点补强,1
2026-W28,summer_plan,暑期规划,2
2026-W29,math_live,课前提醒,1
2026-W29,practice,课后练习,2
```

### Seasonal Context

Use seasonal variables for timing and relevance, not fake urgency.

```csv
date_range,season_key,usable_angle,avoid_angle
2026-07-01/2026-07-15,summer_start,暑期刚开始，适合建立学习节奏,不要制造落后焦虑
2026-08-20/2026-08-31,back_to_school,开学前查漏补缺,不要承诺开学排名提升
```

## 2. Variable Ownership

| Variable | Source | Owner | Example |
| --- | --- | --- | --- |
| parent name | user state | code insert | 小雨妈妈 |
| grade | user state | code insert | 一年级 |
| weakness tag | user state | code insert | 图形找规律 |
| offer/deadline/link | campaign facts | code insert | 2026-07-15 |
| topic angle | topic cycle | deterministic selection | 薄弱点补强 |
| seasonal angle | seasonal context | deterministic selection | 暑期刚开始 |
| opening/CTA wording | template pool | rotation | 可以先帮孩子占一个体验名额 |
| final tone | AI | controlled rewrite | 温和、短、不焦虑 |

## 3. Batch Generation Logic

```text
for each user:
  1. read user state.
  2. read campaign facts.
  3. choose topic angle from current week.
  4. choose seasonal angle from current date.
  5. check recent touch history:
     - skip if same topic sent in last N days.
     - skip or downgrade if user has complaint/risk flag.
     - avoid same message_hash.
  6. render fixed fields by code.
  7. choose one template from rotation pool.
  8. ask AI to rewrite within strict boundaries.
  9. run review gates.
  10. export review sheet, not direct-send by default.
```

## 4. Dedupe and Frequency Rules

Examples:

```json
{
  "max_user_touches_per_7_days": 2,
  "same_topic_cooldown_days": 5,
  "risk_user_max_touches_per_7_days": 1,
  "skip_if_recent_result": ["complaint", "opt_out"],
  "dedupe_keys": ["user_id", "topic_key", "campaign_id"]
}
```

Dedupe should be handled by code, not by the model.

## 5. AI Prompt Boundary

```text
你是私域文案改写助手。你只能基于以下字段生成，不得新增价格、名额、截止时间、学习诊断、承诺效果。

用户字段：
- 称呼：{{parent_name}}
- 年级：{{student_grade}}
- 薄弱点：{{weakness_tag}}
- 用户分层：{{segment}}

活动字段：
- 产品：{{product_name}}
- 权益：{{core_offer}}
- 截止时间：{{deadline}}
- 链接：{{link}}

运营变量：
- 本周主题：{{topic_angle}}
- 时令角度：{{seasonal_angle}}
- 语气：温和、具体、不制造焦虑

请生成 3 条微信私聊文案，每条 80 字以内。
必须包含：称呼、产品/主题、推荐理由、CTA、链接。
不能出现：{{forbidden_claims}}。
```

## 6. Review Sheet Output

Batch generation should export a review sheet:

| user_id | topic_key | seasonal_angle | generated_text | dedupe_status | frequency_status | risk_note | reviewer_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U001 | math_live | summer_start | ... | pass | pass | none | approve |
| U002 | math_live | summer_start | skipped | same topic recently | risk user | complaint within 7 days | reject |

## 7. What AI Should Not Control

AI should not decide:

- who is eligible to receive a push.
- whether frequency rules can be bypassed.
- whether a complaint user can still be pushed.
- whether an unapproved offer can be mentioned.
- the final send action.

AI can help:

- rewrite approved information.
- create controlled variants.
- adapt copy to channel length.
- summarize why a user was skipped, based on rule outputs.

