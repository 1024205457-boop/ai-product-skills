# 原始明细数据到透视脚本

当目标是“我有原始用户状态行和触达历史行，希望脚本自动产出和人工透视表一致的结果”时，读取这个参考。

下面示例使用脱敏模拟数据，但结构对应常见 AI 产品运营数据：

- **用户状态表：** 长期用户状态、分层、意向、风险标记、标签、最新摘要。
- **触达历史表：** 每一次用户/运营/Agent 动作、消息、点击、跟进、转化、投诉或转人工。

## 1. 从人工透视表开始

写代码前，先把人工会怎么建透视表写清楚。

人工透视示例：

```text
行：
- date
- scene

列 / 值：
- state_count：state_id 计数
- active_users：user_id 去重数
- high_intent_users：intent_level = high 的 user_id 去重数
- risk_users：risk_flag = 1 的 user_id 去重数
- followup_count：event_type = followup 的触达记录数
- complaint_count：event_type = complaint 的触达记录数

筛选：
- date 在 2026-07-01 到 2026-07-07 之间
- 排除测试用户
```

这会成为脚本契约。不要一上来就从代码开始。

## 2. 原始用户状态示例

保存为 `user_state.csv`：

```csv
state_id,user_id,created_at,scene,intent_level,risk_flag,tags,latest_summary
S001,U001,2026-07-01 09:12:00,trial_class,high,0,"试听,数学,待跟进","家长关注一年级数学思维，想先看直播课"
S002,U002,2026-07-01 10:20:00,private_push,medium,1,"推送频繁,退订风险","家长反馈最近提醒太频繁，需要降低触达"
S003,U003,2026-07-02 14:05:00,renewal,high,0,"续费,价格咨询","家长询问暑期班价格和优惠"
S004,U004,2026-07-02 16:30:00,trial_class,low,0,"未接通,二次跟进","电话未接通，明天再次跟进"
S005,U001,2026-07-03 19:40:00,trial_class,high,0,"完课,正反馈","孩子完成试听，家长反馈课程节奏可以"
```

重要字段：

| 字段 | 含义 | 透视用途 |
| --- | --- | --- |
| `state_id` | 唯一状态行 | 记录计数 |
| `user_id` | 用户键 | 用户去重 |
| `created_at` | 状态更新时间 | 日期分组 |
| `scene` | 业务场景 | 行维度 |
| `intent_level` | 用户意向 | 高意向统计 |
| `risk_flag` | 风险信号 | 风险用户统计 |
| `tags` | 逗号分隔标签 | 标签频次表 |
| `latest_summary` | 文本明细 | 人工复核来源，不直接作为指标 |

## 3. 原始触达历史示例

保存为 `touch_history.csv`：

```csv
touch_id,user_id,created_at,operator,channel,event_type,note
T001,U001,2026-07-01 09:20:00,teacher_a,wechat,followup,"发送试听课提醒，家长已读"
T002,U002,2026-07-01 10:28:00,teacher_b,wechat,complaint,"家长说提醒太频繁，要求减少推送"
T003,U003,2026-07-02 14:12:00,teacher_a,phone,followup,"解释暑期班价格，家长要求发优惠说明"
T004,U004,2026-07-02 16:35:00,teacher_c,phone,no_answer,"电话未接通，计划明天再打"
T005,U001,2026-07-03 20:00:00,teacher_a,wechat,conversion,"家长预约下一节直播课"
```

重要字段：

| 字段 | 含义 | 透视用途 |
| --- | --- | --- |
| `touch_id` | 唯一触达行 | 触达记录计数 |
| `user_id` | 关联用户状态的键 | 触达用户去重 |
| `created_at` | 动作时间 | 日期分组 |
| `operator` | 老师/Agent/运营 | 运营人员透视 |
| `channel` | 微信/电话/社群等渠道 | 渠道透视 |
| `event_type` | 跟进/投诉/转化/未接通等事件类型 | 指标列 |
| `note` | 详细文本 | 可选 AI/人工标签来源 |

## 4. 输出透视表

脚本应生成类似 `detail_pivot.xlsx` 的 Excel 文件，包含这些 sheet：

| 工作表 | 用途 |
| --- | --- |
| `state_by_scene` | 来自用户状态行的每日场景汇总 |
| `touch_by_operator` | 来自触达历史的每日运营/渠道/事件汇总 |
| `tag_frequency` | 来自用户状态标签的标签计数 |
| `quality_checks` | 行数、缺失字段、日期范围、重复键 |

这比创建原生 Excel 透视表对象更适合初学者。它产生相同业务输出，但 Excel 自动化风险更低。

## 5. 脚本映射

| 人工透视动作 | 脚本动作 |
| --- | --- |
| 把 `date` 拖到行 | 解析 `created_at`，生成 `date` 列 |
| 把 `scene` 拖到行 | `groupby(["date", "scene"])` |
| 统计状态行 | `state_id.nunique()` |
| 用户去重 | `user_id.nunique()` |
| 筛选高意向 | 统计 `intent_level == "high"` 的去重用户 |
| 筛选风险用户 | 统计 `risk_flag == 1` 的去重用户 |
| 把事件类型拖到列 | `pivot_table(columns="event_type")` |
| 统计标签 | 拆分 `tags`，展开为多行，再按标签分组 |

## 6. 起步脚本

使用本技能目录里的 `../scripts/build_detail_pivot.py`。

运行：

```bash
python scripts/build_detail_pivot.py \
  --state user_state.csv \
  --touch touch_history.csv \
  --output detail_pivot.xlsx \
  --start 2026-07-01 \
  --end 2026-07-07
```

脚本应做：

1. 加载用户状态和触达历史 CSV。
2. 校验必需列。
3. 解析日期。
4. 过滤目标周期。
5. 生成透视式汇总工作表。
6. 写出 Excel。
7. 写出质量检查。

## 7. AI 放在哪里

透视脚本之前，AI 可以帮助：

- 阅读很长的 `latest_summary` 或 `note` 文本。
- 把文本分类为标签：`price_interest`、`push_risk`、`complaint`、`followup_needed`。
- 总结异常原因。

代码应该负责：

- 计数。
- 日期过滤。
- 用户去重。
- 透视表输出。
- 回读和校验。

不要让 AI 直接从文本“估算”指标。指标必须来自行数据。

## 8. 初学者清单

运行前：

- 原始用户状态 CSV 已导出。
- 原始触达历史 CSV 已导出。
- 目标日期范围已确认。
- 必需列已确认。
- 测试用户已排除，或明确包含。

运行后：

- 输出 Excel 能打开。
- 日期过滤后的行数和原始文件匹配。
- 每个工作表都有非空行。
- 手动抽查 3 个用户，对照原始明细行。
- 信任自动化之前，至少和上一版人工透视对比一次。
