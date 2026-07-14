# Path Decision Table

Use this table before writing code.

| Question | API/Cookie path | Playwright path |
| --- | --- | --- |
| Is there a stable endpoint? | Best choice | Usually unnecessary |
| Is login SSO/QR/manual? | Harder unless cookie is available | Better fit |
| Is output JSON/CSV? | Best choice | Good for clicking export |
| Is output only visible in UI? | Harder | Better fit |
| Need screenshots? | No | Yes |
| Need high-volume repeat runs? | Better | Slower and more fragile |
| Selectors change often? | Not affected | Fragile |
| Endpoint parameters are unclear? | Risky | Easier to mirror manual flow |
| Need write-back? | Safer if API supports scoped writes | Risky; must read back |
| New beginner implementation? | Start here if endpoint is obvious | Start here if export button is obvious |

## Recommended Product Wording

```text
本项目的数据自动化分两条路径：

1. API/Cookie 路径：适合已有稳定接口的报表。脚本读取日期、渠道等参数，调用接口导出结构化数据，再做字段校验、聚合和写回。
2. Playwright 路径：适合没有开放接口、只能通过后台页面导出的报表。脚本模拟人工打开页面、选择日期、点击导出，拿到 CSV 后再进入同一套校验和汇总流程。

MVP 阶段优先做只读导出和汇总，不直接自动改线上看板。等读回校验稳定后，再做小范围写回。
```

## Simple Selection Formula

```text
If stable endpoint exists:
  Use API/Cookie script.
Else if export can only be reached through UI:
  Use Playwright to download raw data.
Then:
  Use deterministic validation + aggregation script.
```

