# Playwright 路径

当可靠流程依赖浏览器操作时，使用这条路径：登录、选择筛选项、点击导出、下载文件或截图。

## 典型人工流程

```text
1. 打开报表后台。
2. 通过 SSO 或二维码登录。
3. 选择日期范围。
4. 点击查询。
5. 点击导出。
6. 等待 CSV 下载。
7. 检查下载文件并生成汇总。
```

## Playwright 自动化形态

```text
1. 打开浏览器。
2. 使用已有登录态，或允许人工登录。
3. 进入报表页面。
4. 填写日期范围和筛选项。
5. 点击导出。
6. 保存下载的 CSV。
7. 运行确定性校验/聚合脚本。
```

## 如何捕获 UI 流程

当初学者问“我怎么写 Playwright 脚本”时，用下面的方法。

### 方案 A：Playwright codegen

```bash
npx playwright codegen https://example.com/report
```

然后手动执行流程：

1. 如有需要，先登录。
2. 打开报表页。
3. 选择日期范围。
4. 点击查询。
5. 点击导出。

Codegen 会生成 locator 草稿。把它当起点，不要当最终代码。

清理生成代码：

- 用 `getByRole`、`getByLabel` 或 `getByText` 替换脆弱 CSS 选择器。
- 删除不必要的等待。
- 导出点击前加入 `waitForEvent("download")`。
- 筛选条件应用后截图。
- 处理前先保存下载的原始文件。

### 方案 B：手动检查 locator

用 DevTools 或 Playwright Inspector 找稳定 UI 句柄：

```bash
PWDEBUG=1 node export_report.js
```

优先使用：

```js
await page.getByLabel("Start date").fill("2026-07-01");
await page.getByRole("button", { name: "Export" }).click();
await page.getByText("No data").isVisible();
```

避免：

```js
await page.locator("div:nth-child(4) > span > button").click();
```

## 登录态方案

内部工具里，登录方式往往决定 Playwright 是否可行。

### 每次人工登录

最适合第一个原型：

```text
1. 启动有界面浏览器。
2. 让操作者手动登录。
3. 在终端按回车。
4. 脚本继续导出。
```

### 保存 storage state

第一个原型跑通后再使用：

```js
await context.storageState({ path: "storage-state.json" });
```

下次运行：

```js
const context = await browser.newContext({
  acceptDownloads: true,
  storageState: "storage-state.json",
});
```

不要提交 `storage-state.json`，它可能包含 Cookie 或 token。

## 最小 Node 骨架

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

## 选择器规则

优先：

- `getByRole`
- `getByLabel`
- 稳定 test ID
- 产品负责人会维护的可见文本

避免：

- 很长的 CSS 链。
- 自动生成的 class 名。
- 除非没有替代方案，不用 nth-child 选择器。

## 校验清单

- 筛选条件应用后保存截图。
- 下载文件存在。
- 文件修改时间属于本次运行。
- CSV 表头匹配预期字段。
- 文件内日期范围匹配页面选择的日期范围。
- 行数合理。

## 什么时候不要用这条路径

- 已经有稳定 API。
- 运行需要高频批处理。
- UI 选择器每天变化。
- 脚本会点击破坏性按钮。
- 没有回读或下载产物可验证。

## 安全写回规则

初学者通常应让 Playwright 停在导出/下载。如果必须写回：

```text
1. 只写一个受控表格/范围。
2. 写前写后都截图。
3. 从页面读取结果值。
4. 和来源汇总比较。
5. 第一个不匹配就停止。
```
