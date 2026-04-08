# Research Pipeline - 端到端研究流程

## 目标

端到端完成一个 research change 的完整生命周期，同时把执行面升级为第一版 multi-agent 编排：

- `request.md`
- `plan.md`
- `draft.md`
- `review/`
- `artifact.md` / `verdict.md`

## 适用范围

- 适用于本仓库大多数 research change
- **不适用于**规约、治理、仓库分层、AGENTS 路由类改造；这类任务应走 `governance-review-workflow.md`

## 输入输出

**输入：**
- 目标 change 目录路径
- 用户意图与研究问题

**输出：**
- `request.md`
- `plan.md`
- `sources/`
- `draft.md`
- `review/`
- `knowledge/analysis/.../artifact.md` 或 `knowledge/decisions/.../artifact.md`

## 执行模式

### 默认模式：orchestrator 驱动的 multi-agent 执行

执行入口先读取：

1. `harness/workflows/_index.yaml`
2. `harness/agents/_index.yaml`
3. 当前 workflow
4. 对应 OpenSpec spec

### 默认 active agents

| 角色 | 模式 | 责任 |
|------|------|------|
| `orchestrator` | always | 任务分类、激活 agent、控制 handoff、整合结果 |
| `research-author-agent` | always | `request / plan / draft` 主链写作 |
| `source-evidence-agent` | always | 来源收集与证据缺口盘点 |
| `review-critic-agent` | always | 独立技术评审与 traceability audit |
| `publish-agent` | always | artifact 提炼与 update impact scan |
| `diagram-agent` | conditional | primitive / mechanism-heavy / 明确需要图表时启用 |

### fallback

若运行环境不支持真实 subagent：

- 仍按 active agents 的 contract 顺序执行
- 不得跳过 handoff artifact 与 quality gate
- 必须在最终总结中说明哪些角色被串行折叠执行

## Supporting Track：Sources

`sources/` 不是长期主链 artifact，但在 plan / draft 阶段必须作为支撑轨存在：

```text
request ──┐
          ├─> plan ──┐
sources ──┘          ├─> draft ──> review ──> artifact
diagrams ────────────┘
```

## 阶段顺序

### 阶段 1：request

**owner**：`research-author-agent`

**输入**：
- 用户意图
- 现有 change 目录（如有）

**输出**：
- `request.md`

**完成标准**：
- 对象类型明确
- 研究路径明确
- 核心问题、范围、非目标、预期输出完整

### 阶段 2：plan

**owner**：`research-author-agent`

**并行支持**：`source-evidence-agent`

**输入**：
- `request.md`
- `sources/`（可边生成边消费）

**输出**：
- `plan.md`
- `sources/source-review.md`

**完成标准**：
- 研究深度明确
- 来源规划符合 L1/L2/L3/L4
- 图表范围明确
- 证据缺口和完成标准明确

### 阶段 3：draft

**owner**：`research-author-agent`

**条件角色**：`diagram-agent`

**输入**：
- `request.md`
- `plan.md`
- `sources/`
- 已有 `draft.md`（如有）

**输出**：
- `draft.md`
- `diagrams/`（如适用）

**强制要求**：

1. 先做实体分类
2. 再做图表决策树
3. 如需 PlantUML，只能通过用户级 skill 生成 diagram package
4. draft 完成后必须执行 diagram contract 校验

### 阶段 4：review gate

**owner**：`review-critic-agent`

**输入**：
- `draft.md`
- `plan.md`
- `sources/`
- `diagrams/`（如有）

**输出**：
- `review/checklist.yaml`
- `review/issues.md`
- `review/review-summary.md`

**通过条件**：
- high severity 问题已清零
- 评审结论明确
- 如存在图表，diagram contract 与内容质量均通过

### 阶段 5：artifact / publish

**owner**：`publish-agent`

**输入**：
- `request.md`
- `plan.md`
- `draft.md`
- `review/review-summary.md`

**输出**：
- `knowledge/analysis/.../artifact.md`
- `knowledge/decisions/.../artifact.md`
- `knowledge/decisions/.../verdict.md`（如适用）

**完成标准**：
- 长期内容已提炼，而非整包复制
- 目标路径正确
- update 场景已完成 impact scan

## 关键 handoff artifact

| From | To | Artifact |
|------|----|----------|
| orchestrator | research-author-agent | 目标 change、对象类型、active agents |
| research-author-agent | source-evidence-agent | 研究问题、来源优先级 |
| source-evidence-agent | research-author-agent | `source-review.md`、核心 excerpts、evidence gaps |
| research-author-agent | review-critic-agent | 待审 `draft.md`、未决问题 |
| review-critic-agent | publish-agent | approved / blocked 结论、必须修复项 |

## 完成后的总结要求

最终应汇报：

- active agents 列表
- 哪些角色并行、哪些串行
- 各阶段状态
- 使用的 change 路径
- 研究对象类型和路径
- 是否生成 diagram package
- 是否完成 publish / apply
