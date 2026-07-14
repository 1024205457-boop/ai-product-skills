# 初学者自动化示例

这个参考给还在手动打开导出文件、做透视表、把数字复制到周报看板的人使用。

如果来源数据是用户状态记录或详细触达历史，先读 `raw-detail-to-pivot-script.md`。那个文件是把原始明细转成透视式输出表的主示例。本文件只提供较小的入门模式。

## 示例 1：用脚本替代透视表

### 模拟原始数据

保存为 `mock_events.csv`：

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

人工透视目标：

- 行：`channel`
- 列/指标：浏览、预约、支付、收入
- 衍生指标：预约率 = 预约 / 浏览，支付率 = 支付 / 浏览

### 最小 Python 脚本

保存为 `weekly_summary.py`：

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

运行：

```bash
python weekly_summary.py
```

它替代了：

- 手工透视表。
- 手工计数。
- 口径不清的分母。
- 难以环比的临时结果。

## 示例 2：读取详细日记/备注

有些产品不只有事件行，也会有类似“老师联系家长”“学生缺课”“用户投诉”的日记式记录。

### 模拟日记数据

保存为 `mock_diary.csv`：

```csv
date,user_id,operator,note
2026-07-01,U001,teacher_a,家长说孩子最近图形题听不懂，约了周三直播课
2026-07-01,U002,teacher_b,用户觉得提醒太频繁，要求减少推送
2026-07-02,U003,teacher_a,孩子完成试听，家长问是否有暑期班优惠
2026-07-02,U004,teacher_c,电话未接通，准备明天再跟进
```

### 简单规则抽取

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

AI 可以帮助：

- 总结长备注。
- 分类模糊备注。
- 抽取待办事项。

代码必须负责：

- 读取行。
- 匹配用户 ID。
- 写入标签。
- 统计标签频次。
- 保留原始备注不变。

## 示例 3：Cookie vs Playwright

### Cookie/API 路径

适用条件：

- 页面调用稳定 API。
- 能检查请求参数。
- 操作者能在运行时粘贴临时 Cookie 或 token。

初学者形态：

```text
1. 操作者把 Cookie 导出到本地环境变量。
2. 脚本请求 `/api/report?start=2026-07-01&end=2026-07-07`。
3. 脚本保存原始 JSON/CSV。
4. 脚本校验字段和行数。
5. 脚本写出汇总 CSV。
```

规则：

- 不提交 Cookie。
- 不把 Cookie 粘贴到提示词。
- 优先用只读导出接口。
- 记录请求周期和导出时间。

### Playwright 路径

适用条件：

- 没有文档化 API。
- 唯一稳定操作是“打开页面 -> 选择日期 -> 点击导出”。
- 登录需要浏览器会话或 SSO。

初学者形态：

```text
1. 用 Playwright 打开浏览器。
2. 使用已有登录浏览器配置或人工登录。
3. 进入报表页面。
4. 选择日期范围。
5. 点击导出。
6. 保存下载的 CSV。
7. 运行同一套校验和汇总脚本。
```

规则：

- Playwright 应先抓取/导出，不要直接编辑看板。
- 始终保留下载的原始文件。
- 选择器不稳定时，加截图或 HTML 快照。
- 任何写回后，都要读取目标值并比较。

## 示例 4：安全写回清单

写入看板前：

- 目标周期已确认。
- 原始导出已保存。
- 汇总已生成。
- 必需指标非空。
- 分母已命名。
- 上周期对比已检查。
- 目标位置用表头/日期定位，不用行号。

写入后：

- 回读所有写入值。
- 回读值和汇总 CSV 比较。
- 加入异常说明。
- 准确报告改了什么。
