# Agent Adapter Contract

**本文件位置**：`harness/adapters/agent-adapter-contract.md`
**用途**：定义 Claude Code 与 Qoder 共用的 agent 合同字段，`.claude/agents/CONTRACT.md` 与未来 `.qoder/agents/CONTRACT.md` 都应引用此文件。

---

## 一、共享字段定义

以下字段是所有 agent 定义的最小共享集合，不依赖特定 tool 的 frontmatter 语法。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | agent 唯一标识符，kebab-case，与文件名一致 |
| `description` | string | 是 | 一句话描述职责 + 何时被谁调用 |
| `model` | string | 条件必填 | 模型选择策略；Qoder 不支持此字段，默认继承主会话模型 |
| `tools` | list / string | 条件必填 | 允许使用的工具列表；Claude Code 用 YAML 列表，Qoder 用逗号分隔字符串 |
| `mcpServers` | list | 否 | 需要显式启用的 MCP server 名称 |
| `skills` | list | 是 | 允许调用的 skill 列表，空列表填 `[]` |

### 共享正文段落

以下段落应在所有 agent 定义中出现，无论 tool 是否要求固定结构：

1. **角色定位**：你是谁、负责什么、主会话保留什么决策权
2. **主会话边界**：主会话决定什么、agent 自主决定什么、agent 不得决定什么
3. **读取输入**：执行前必须读取的文件/目录，使用具体路径
4. **写入范围**：可以创建/修改的文件/目录，超出此范围不得修改任何文件
5. **工作合同**：编号的可验证行为约束
6. **禁止事项**：编号的负面约束，必须包含"不要调用其他 subagent"、"不要超出写入范围修改文件"、"不要在未满足前置条件时声称完成"
7. **完成信号**：什么条件视为完成、返回什么内容、遇到阻塞时如何回报

---

## 二、Tool 特定格式

### Claude Code

- Frontmatter 字段：`name`、`description`、`model`、`tools`（YAML 列表）、`mcpServers`、`skills`、`color`（可选）、`effort`（可选）
- 正文结构：必须包含上述 7 个段落
- 校验基线：`.claude/agents/CONTRACT.md`

### Qoder

- Frontmatter 字段：`name`、`description`、`tools`（逗号分隔字符串）、`skills`、`mcpServers`
- 无 `model`、`color`、`effort` 字段
- 正文结构：自由 Markdown，但 Qoder thin wrapper **必须**在正文中包含一条显式指令，要求 agent 启动时读取源文件并遵守其中的角色定位、读写范围、禁止事项、完成信号
- 不支持 agent 嵌套（subagent 不能调 subagent）

**Thin wrapper 正文要求**：

Qoder agent wrapper（`.qoder/agents/{name}.md`）的正文不能只写一行 `@see` 引用。必须在正文中显式写入类似如下指令：

```
启动时请先读取并遵守 .claude/agents/{name}.md 中的完整合同定义，
包括角色定位、主会话边界、读取输入、写入范围、工作合同、禁止事项和完成信号。

辅助引用（仅供参考）：@see .claude/agents/{name}.md
```

其中：
- **"启动时请先读取并遵守…"** 是执行指令，Qoder agent 启动后会据此去读取源文件的完整合同正文
- **`@see`** 只作为人类浏览时的索引/辅助引用，不假设 Qoder 会自动展开或识别 `@see` 语法
- 当未来存在共享 agent 源文件时，路径应改为共享源文件的位置

---

## 三、复用原则

1. Agent 正文不复制到 `.qoder/agents/`。Qoder thin wrapper 必须在正文中包含显式指令，要求 agent 启动时读取源文件（`.claude/agents/{name}.md` 或未来共享 agent 源文件）并遵守其中的完整合同定义
2. `@see` 只作为人类索引/辅助引用，不假设 Qoder 会自动展开或识别此语法
3. 字段映射差异由 `harness/adapters/tool-capability-matrix.md` 处理
4. 正式规则引用 `openspec/specs/**` 与 `harness/rules/**`，不复制到 adapter 层
