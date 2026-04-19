# MCP 工具使用指南

## fastmcp-gateway: 联网搜索

**工具**：`searxng_search_web`

| 参数 | 必填 | 说明 |
|------|------|------|
| `query` | 是 | 搜索关键词 |
| `category` | 否 | 搜索类别 |
| `max_results` | 否 | 最大返回条数 |
| `language` | 否 | 语言过滤 |
| `time_range` | 否 | 时间范围 |

**约束**：
- 任务明确要求"联网搜索 / 在线检索 / web search / search"时默认使用。
- 若该 MCP 在当前会话不可用，应先明确说明，再选择替代方式；不要无提示地切换到其他搜索通道。

## crawl4ai: 网页内容提取

当需要提取网页内容、获取网页详情、将网页转换为 Markdown 时使用。

### 工具列表

| 工具 | 用途 |
|------|------|
| `md` | 将网页转换为 Markdown（默认 fit 模式，支持 raw/bm25/llm 过滤） |
| `html` | 获取并清理网页 HTML 结构 |
| `screenshot` | 获取网页截图 |
| `pdf` | 生成网页 PDF |
| `execute_js` | 在浏览器上下文中执行 JavaScript |
| `crawl` | 完整网页爬取（支持 hooks 配置） |
| `ask` | 查询 Crawl4AI 库的使用文档 |

### md 工具参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 是 | 目标网页 URL |
| `f` | 否 | 过滤模式：`fit`（默认）、`raw`、`bm25`、`llm` |
| `q` | 否 | 查询字符串（用于 bm25/llm 模式） |
| `provider` | 否 | LLM provider 覆盖 |
| `temperature` | 否 | LLM temperature（0.0-2.0） |

**优先使用 `md` 工具**提取网页内容。
