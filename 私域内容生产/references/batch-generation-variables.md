# 批量生成变量

当目标是“基于已批准文案信息，批量生成私域消息，同时遵守主题周期、季节背景、去重和频控”时，使用这个参考。

不要在技能里硬编码真实私域数据。使用通用表：

- 用户状态表。
- 触达历史表。
- 活动事实表。
- 主题周期表。
- 季节背景表。
- 模板池。

## 1. 输入表

### 活动事实

这些是已批准事实。AI 可以改写，但不能编造新事实。

```csv
campaign_id,product_name,core_offer,deadline,cta,link,forbidden_claims
C001,数学思维直播课,本周可预约一节体验课,2026-07-15,点击预约,https://example.com/book,"一定提分;仅剩3席;名师保过"
```

### 用户状态

```csv
user_id,parent_name,student_grade,segment,intent_level,risk_flag,weakness_tag,last_summary
U001,小雨妈妈,一年级,trial_parent,high,0,图形找规律,"最近看过数学思维课，家长关注图形题"
U002,乐乐爸爸,二年级,quiet_user,medium,1,计算粗心,"近期触达较多，家长回复变少"
U003,安安妈妈,一年级,active_parent,high,0,应用题理解,"家长主动问过暑期课安排"
```

### 触达历史

```csv
user_id,touch_date,channel,topic_key,message_hash,result
U001,2026-07-08,wechat,math_live,hash_001,clicked
U002,2026-07-09,wechat,math_live,hash_002,no_reply
U002,2026-07-10,wechat,renewal,hash_003,complaint
U003,2026-07-05,community,summer_plan,hash_004,replied
```

### 主题周期

用主题周期避免每天推同一个角度。

```csv
week,topic_key,angle,priority
2026-W28,math_live,薄弱点补强,1
2026-W28,summer_plan,暑期规划,2
2026-W29,math_live,课前提醒,1
2026-W29,practice,课后练习,2
```

### 季节背景

季节变量用于增强相关性，不用于制造虚假紧迫感。

```csv
date_range,season_key,usable_angle,avoid_angle
2026-07-01/2026-07-15,summer_start,暑期刚开始，适合建立学习节奏,不要制造落后焦虑
2026-08-20/2026-08-31,back_to_school,开学前查漏补缺,不要承诺开学排名提升
```

## 2. 变量归属

| 变量 | 来源 | 负责人 | 示例 |
| --- | --- | --- | --- |
| 家长称呼 | 用户状态 | 代码插入 | 小雨妈妈 |
| 年级 | 用户状态 | 代码插入 | 一年级 |
| 薄弱点标签 | 用户状态 | 代码插入 | 图形找规律 |
| 权益/截止时间/链接 | 活动事实 | 代码插入 | 2026-07-15 |
| 主题角度 | 主题周期 | 确定性选择 | 薄弱点补强 |
| 季节角度 | 季节背景 | 确定性选择 | 暑期刚开始 |
| opening/CTA wording | 模板池 | 轮换 | 可以先帮孩子占一个体验名额 |
| final tone | AI | 受控改写 | 温和、短、不焦虑 |

## 3. 批量生成逻辑

```text
for each user:
  1. 读取用户状态。
  2. 读取活动事实。
  3. 从当前周选择主题角度。
  4. 从当前日期选择季节角度。
  5. 检查近期触达历史：
     - 最近 N 天发过同主题则跳过。
     - 用户有投诉/风险标记则跳过或降级。
     - 避免相同 message_hash。
  6. 用代码渲染固定字段。
  7. 从轮换模板池选择一个模板。
  8. 要求 AI 在严格边界内改写。
  9. 运行审核门。
  10. 导出审核表，默认不直接发送。
```

## 4. 去重和频控规则

示例：

```json
{
  "max_user_touches_per_7_days": 2,
  "same_topic_cooldown_days": 5,
  "risk_user_max_touches_per_7_days": 1,
  "skip_if_recent_result": ["complaint", "opt_out"],
  "dedupe_keys": ["user_id", "topic_key", "campaign_id"]
}
```

去重应由代码处理，不应由模型决定。

## 5. AI 提示词边界

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

## 6. 审核表输出

批量生成应导出审核表：

| user_id | topic_key | seasonal_angle | generated_text | dedupe_status | frequency_status | risk_note | reviewer_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U001 | 数学直播 | 暑期开始 | ... | 通过 | 通过 | 无 | 通过 |
| U002 | 数学直播 | 暑期开始 | 已跳过 | 近期同主题 | 风险用户 | 7 天内投诉 | 驳回 |

## 7. AI 不应控制什么

AI 不应决定：

- 谁有资格接收推送。
- 频控规则是否可以绕过。
- 投诉用户是否还能继续触达。
- 是否可以提及未经批准的权益。
- 最终发送动作。

AI 可以帮助：

- 改写已批准信息。
- 生成受控变体。
- 适配渠道长度。
- 基于规则输出，总结某个用户为什么被跳过。
