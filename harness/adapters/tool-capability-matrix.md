# Tool Capability Matrix

**本文件位置**：`harness/adapters/tool-capability-matrix.md`
**用途**：记录 Claude Code 与 Qoder 的字段映射、能力差异与降级策略。

---

## 一、Frontmatter 字段映射

| 共享语义 | Claude Code 字段 | Qoder 字段 | 差异 |
|----------|-----------------|-----------|------|
| Agent 名称 | `name`（kebab-case，与文件名一致） | `name`（kebab-case） | Qoder 不要求与文件名一致 |
| Agent 描述 | `description`（含调用方和调用时机） | `description`（自然语言描述） | Qoder 不需要包含调用方信息 |
| Agent 模型 | `model`（`"inherit"` 或模型名） | **无此字段** | Qoder subagent 自动继承主会话模型 |
| Agent 工具 | `tools`（YAML 列表 `["Read", "Glob"]`） | `tools`（逗号分隔 `"Read,Glob"`） | 格式不同 |
| Agent MCP | `mcpServers`（列表） | `mcpServers`（列表） | 一致 |
| Agent Skills | `skills`（列表） | `skills`（列表） | 一致 |
| Agent 颜色 | `color`（可选） | **不支持** | 仅 Claude Code 终端显示用 |
| Agent 工作量 | `effort`（可选） | **不支持** | 仅 Claude Code 调度参考 |
| Command 名称 | `name`（必填） | `name`（必填） | 一致，文件名应与 name 一致 |
| Command 描述 | `description`（必填） | `description`（必填） | 一致 |
| Skill 名称 | `name`（必填） | `name`（必填，max 64 chars） | Qoder 有长度约束 |
| Skill 描述 | `description`（必填） | `description`（必填，max 1024 chars） | Qoder 有长度约束，对触发至关重要 |

---

## 二、能力差异与降级策略

| 能力 | Claude Code | Qoder | 降级策略 |
|------|-------------|-------|---------|
| AGENTS.md 自动加载 | 根目录自动加载 | 原生兼容 | 优先不复制，Qoder 自动识别根目录 `AGENTS.md` |
| CLAUDE.md | 专属入口自动加载 | 不支持 | 通过 `.qoder/rules/` 的 Always Apply rule 或 `.qoder/AGENTS.md` 引入语言与路由规则 |
| Hook 内联 command | `settings.json` 内联 `command` + `if` 条件 | 外部 shell 脚本 + stdin JSON | 将 Claude Code 内联 hook 重写为 `.qoder/hooks/` 下的独立脚本 |
| Settings 字段 | `language`、`model`、`hooks` | `permissions`、`hooks` | 各自保留 tool 特有字段，不交叉复制 |
| Multi-agent 嵌套 | 支持（有合同约束） | 不支持（subagent 不能调 subagent） | 与现有 agent contract 一致，无额外损失 |
| 后台调用 | `run_in_background` | 无对等字段 | 主会话安静等待系统通知 |
| Worktree | `isolation: "worktree"` | `qodercli --worktree` | CLI 级隔离，非 agent 级字段 |
| Quest Mode | 无 | `/quest` 多 agent 编排 | 与仓库 research pipeline 有重叠，暂不复用 |
| Rules 类型 | 无分类概念 | Always Apply / Model Decision / Apply Manually / Specific Files | 语言规则用 Always Apply，文件规则用 Specific Files |
| MCP 配置 | `.claude/` settings | `.mcp.json` / `~/.qoder.json` | 各自管理，不交叉 |

---

## 三、具体能力标记

| 能力 | Claude Code | Qoder |
|------|-------------|-------|
| Web 搜索 | MCP `mcp__fastmcp-gateway__searxng_search_web` | 内置 `WebSearch` |
| 网页抓取 | MCP `mcp__crawl4ai__md` | 内置 `WebFetch` |
| 文件编辑 | `Edit`、`Write` | `Edit`、`Write` |
| 文件搜索 | `Grep`、`Glob`、`Read` | `Grep`、`Glob`、`Read` |
| Shell 执行 | `Bash` | `Bash` |
| Subagent 调度 | `Agent` tool | 自然语言或 `/agent-name` 触发 |
| 权限控制 | settings.json permissions 段 | settings.json permissions 段（格式不同） |
| Cron / 定时 | `CronCreate` | Qoder Workbench / Scheduled Tasks（IDE 级） |

---

## 四、降级原则

1. 当 Qoder 不支持某能力时，优先用 skill 或 README prompt 替代
2. 不等价的 frontmatter 字段不强行映射，在 wrapper 中标注差异
3. MCP 能力通过 tool 内置字段或 Qoder `mcpServers` 字段分别配置
