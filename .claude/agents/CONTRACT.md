# Agent Contract 规范

本文件定义 `.claude/agents/` 中每个 agent 必须满足的最小合同要求。
创建或修改 agent 时，以此文件为校验基准。

---

## 一、Frontmatter 必填字段

每个 agent `.md` 文件必须以 YAML frontmatter 开头，包含：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | agent 唯一标识符，kebab-case，与文件名一致（不含 `.md`） |
| `description` | string | 是 | 一句话描述，说明职责 + 何时被谁调用 |
| `model` | string | 是 | `"inherit"` 继承主会话模型，或指定模型名 |
| `tools` | list | 是 | 允许使用的工具列表，最小权限原则 |
| `skills` | list | 是 | 允许调用的 skill 列表，空列表填 `[]` |
| `color` | string | 否 | 终端显示颜色标识 |
| `effort` | string | 否 | `"low"` / `"medium"` / `"high"` |

**校验规则**：
- `name` 必须与文件名（不含 `.md`）一致
- `description` 必须包含 **"由谁在什么情况下调用"**
- `tools` 不得包含 `Agent`（禁止 agent 嵌套调用）

---

## 二、正文必填段落

### 1. 角色定位

一段话说明：
- 你是谁
- 你负责什么
- **主会话 orchestrator 保留什么决策权**

### 2. 主会话边界

明确列出：
- 主会话决定什么（路由、目标路径、是否进入下一阶段）
- agent 自主决定什么（具体实现细节）
- agent 不得决定什么

### 3. 读取输入

列出 agent 执行前必须读取的文件/目录。
使用具体路径，不使用模糊描述。

### 4. 写入范围

列出 agent 可以创建/修改的文件/目录。
**超出此范围不得修改任何文件。**

### 5. 工作合同

编号列表，每条是**可验证的行为约束**。
禁止模糊描述如"做好工作"、"高质量输出"。

### 6. 禁止事项

编号列表，每条是**明确的负面约束**。
必须包含：
- **不要调用其他 subagent**（除非主会话显式授权）
- **不要超出写入范围修改文件**
- **不要在未满足前置条件时声称完成**

### 7. 完成信号

说明：
- 什么条件视为完成
- 返回主会话时汇报什么内容
- 遇到阻塞时如何回报

---

## 三、Agent 分类

### Author Agents（研究型）

| Agent | 职责 | 调用方 |
|-------|------|--------|
| `primitive-author` | 单个 primitive 的全链路研究写作 | 主会话 orchestrator |
| `synthesis-author` | 多 primitive 的横向对比合成 | 主会话 orchestrator |
| `decision-author` | 场景决策分析写作 | 主会话 orchestrator |

Author agents 的特点：
- 负责 `request.md` → `plan.md` → `draft.md` 的主链写作
- 不直接调用 specialist agent；如需 `sources/` 或 `diagrams/`，向主会话返回明确 handoff 需求
- 完成后将 draft 交回主会话，由主会话决定是否调用 review-critic-agent

### Specialist agents（专长型）

| Agent | 职责 | 调用方 |
|-------|------|--------|
| `source-evidence-agent` | sources/ 创建、链接验证、evidence gap | 主会话 orchestrator |
| `diagram-agent` | 图表生成与验证 | 主会话 orchestrator |
| `review-critic-agent` | 独立技术评审 | 主会话 orchestrator |
| `publish-agent` | 长期 artifact 提炼 | 主会话 orchestrator |
| `governance-review-agent` | 治理边界评审 | 主会话 orchestrator |
| `spec-system-audit-agent` | 仓库规约体系审计与清理 | 主会话 orchestrator |

Specialist agents 的特点：
- 不负责 `request.md` / `plan.md` / `draft.md` 的写作
- 输出结构化产物（inbox.yaml、diagram package、review checklist 等）
- **不得调用其他 subagent**

---

## 四、校验清单

创建或修改 agent 后，逐项检查：

- [ ] frontmatter 包含所有必填字段
- [ ] `name` 与文件名一致
- [ ] `description` 包含调用方和调用时机
- [ ] `tools` 不包含 `Agent`
- [ ] 角色定位段落存在
- [ ] 主会话边界段落存在
- [ ] 读取输入列出具体路径
- [ ] 写入范围列出具体文件
- [ ] 工作合同是编号的可验证行为
- [ ] 禁止事项包含"不要调用其他 subagent"
- [ ] 禁止事项包含"不要超出写入范围修改文件"
- [ ] 完成信号说明返回值格式

---

## 五、文件命名约定

- 文件名：`{agent-role}.md`，kebab-case
- Author agents：`{research-type}-author.md`
- Specialist agents：`{capability}-agent.md`
