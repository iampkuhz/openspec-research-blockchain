---
name: CONTRACT
description: Agent 合同基线。每个 `.qoder/agents/*.md` 必须满足的最小合同要求。
---

# Qoder Agent Contract 规范

本文件定义 `.qoder/agents/` 中每个 agent 必须满足的最小合同要求。

**注意**：本文件定义的是 Qoder 侧的合同要求。共享 agent 合同字段、跨工具的 adapter 约定，
以 `harness/adapters/agent-adapter-contract.md` 为准；
agent 完整分类与协作边界以 `harness/governance/agent-boundaries.md` 为准。

---

## 一、Frontmatter 必填字段

每个 agent `.md` 文件必须以 YAML frontmatter 开头：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | agent 唯一标识符，kebab-case，与文件名（不含 `.md`）一致 |
| `description` | string | 是 | 一句话描述职责 + 何时被主会话调用 |
| `tools` | string | 否 | 允许使用的工具列表，逗号分隔；省略时继承主会话所有工具 |
| `skills` | list | 否 | 允许调用的 skill 列表 |
| `mcpServers` | list | 否 | 需要启用的 MCP server 名称 |

**校验规则**：
- `name` 必须与文件名（不含 `.md`）一致
- `description` 必须包含"由主会话在什么情况下调用"
- 若填写 `tools`，author agent 不得包含 `Agent`（禁止嵌套）
- 需要 MCP 工具时，优先省略 `tools` 并填写 `mcpServers`

---

## 二、正文必填段落

### 1. 角色定位

短段落。说明本 agent 只负责某个 capsule，不拥有完整 pipeline。

### 2. 共享合同

必须声明读取并遵守：
- `harness/adapters/agent-adapter-contract.md`
- `harness/governance/agent-boundaries.md`
- `.qoder/agents/CONTRACT.md`

### 3. 主会话边界

表格：主会话决定 / 你自主决定 / 你不得决定。

### 4. 读取输入

列出具体文件/目录。

### 5. 写入范围

列出可以创建/修改的文件/目录。超出此范围不得修改任何文件。

### 6. 工作合同

编号列表，每条是可验证的行为约束。

### 7. 禁止事项

编号列表，必须包含：
- **不要调用其他 subagent**
- **不要超出写入范围修改文件**
- **不要在未满足前置条件时声称完成**

### 8. Qoder 降级路径

列出 Qoder 工具不可见或能力缺失时如何停止和返回 blocker。

### 9. 完成信号

说明返回主会话时的字段格式：status、outputs、handoff、blockers。

---

## 三、Agent 源文件

所有 agent 的完整合同定义（正文、workflow、质量规则）在 `.claude/agents/*.md`。
本目录下的 agent 文件应优先通过引用指向源文件，不复制完整正文。

---

## 四、校验清单

创建或修改 agent 后，逐项检查：

- [ ] frontmatter 可被 YAML 解析
- [ ] `name` 与文件名一致
- [ ] `description` 包含调用方和调用时机
- [ ] 如填写 `tools`，author agent 不包含 `Agent`
- [ ] 角色定位段落存在
- [ ] 共享合同段落存在，引用了 adapter / agent-boundaries / CONTRACT
- [ ] 主会话边界段落存在
- [ ] 读取输入列出具体路径
- [ ] 写入范围列出具体文件
- [ ] 工作合同是编号的可验证行为
- [ ] 禁止事项包含"不要调用其他 subagent"
- [ ] 包含 Qoder 降级路径
- [ ] 完成信号说明返回格式
