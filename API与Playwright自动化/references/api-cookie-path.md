# API/Cookie 路径

当系统有稳定接口，并且任务可以表达成请求参数时，使用这条路径。

## 典型人工流程

```text
1. 打开内部报表页。
2. 选择日期范围：2026-07-01 到 2026-07-07。
3. 选择渠道：全部。
4. 点击搜索。
5. 下载 CSV 或复制表格。
6. 生成周度汇总。
```

## API/Cookie 自动化形态

```text
1. 操作者提供日期范围。
2. 操作者在运行时提供 cookie/token。
3. 脚本请求报表接口。
4. 脚本保存原始响应。
5. 脚本校验字段和行数。
6. 脚本聚合指标。
7. 脚本输出汇总 CSV 和异常说明。
```

## 如何捕获 API 请求

当初学者问“我怎么知道该调用哪个 API”时，用这套步骤：

1. 打开 Chrome DevTools。
2. 进入 **Network** 标签。
3. 按 **Fetch/XHR** 过滤。
4. 清空旧请求。
5. 在页面上执行完整人工动作：
   - 选择日期范围。
   - 选择筛选项。
   - 点击查询/导出。
6. 点击新出现的请求。
7. 检查：
   - **Request URL：** 接口路径。
   - **Payload/Query String：** 日期、分页、筛选项、ID。
   - **Response/Preview：** 是否包含表格数据。
   - **Headers：** 鉴权头、Cookie、内容类型。
8. 右键请求，选择 **Copy as cURL**。
9. 把 cURL 保存在本地私有笔记里，再转换成脚本。

不要把生产 Cookie 粘贴到公开文档、提示词、提交或截图里。

## 在 Network 里看什么

好的 API 候选：

- URL 包含 `report`、`list`、`query`、`export`、`search`、`metrics` 等词。
- 响应是 JSON 或 CSV。
- 参数可读，例如 `startDate`、`endDate`、`page`、`size`、`channel`。
- 重放请求能返回相同数据。

不好的 API 候选：

- 响应是 HTML 外壳，不是数据。
- 请求需要一次性加密签名。
- Payload 是二进制或不可读。
- 请求只返回任务 ID，而且还需要你暂时不了解的轮询流程。

## 把 cURL 转成脚本

脱敏后的 cURL 示例：

```bash
curl 'https://example.com/api/report?start=2026-07-01&end=2026-07-07' \
  -H 'accept: application/json' \
  -H 'cookie: SESSION=replace-at-runtime'
```

转换成 requests：

```python
import os
import requests

cookie = os.environ["REPORT_COOKIE"]

resp = requests.get(
    "https://example.com/api/report",
    params={"start": "2026-07-01", "end": "2026-07-07"},
    headers={
        "accept": "application/json",
        "cookie": cookie,
    },
    timeout=30,
)
resp.raise_for_status()
data = resp.json()
```

只保留必要 headers。浏览器复制出来的很多 headers 是噪音：

- 通常保留：`authorization`、`cookie`、`content-type`、`accept`。
- 通常删除：`sec-ch-ua`、`sec-fetch-*`、`user-agent`、`referer`、追踪头、浏览器专用头。

## 凭证处理

推荐：

```bash
export REPORT_COOKIE="paste-short-lived-cookie-here"
python fetch_report.py --start 2026-07-01 --end 2026-07-07
```

不要这样：

```python
COOKIE = "real_cookie_committed_to_git"
```

不要提交 Cookie、token、生产用户 ID 或原始私有导出。

## 最小 Python 骨架

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

## 校验清单

- 记录了请求 URL 和参数。
- 响应里的日期范围匹配请求日期范围。
- 行数非零。
- 必需字段存在。
- 检查了重复主键。
- 空指标被标记。
- 转换前保存了原始响应。

## 什么时候不要用这条路径

- 接口每个会话都变化。
- 参数被加密或签名且机制不清楚。
- Cookie 过期太快，无法稳定复跑。
- 条款或权限不允许脚本访问。
- 任务依赖 API 暴露不出来的视觉 UI 状态。
