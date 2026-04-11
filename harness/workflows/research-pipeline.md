# Research Pipeline - 端到端研究流程

## 目标

端到端完成一个 research change 的完整生命周期，同时把执行面升级为第一版由主会话 authoring、specialist subagent 按需介入的编排：

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

### 默认模式：主会话 orchestrator + specialist subagent

执行入口保持在**主会话**：

- 主会话负责读取 workflow / spec / template
- 主会话负责判断目标 change、阶段推进、`request / plan / draft` 主链写作、质量门控与最终落盘
- 主会话按需**显式**拉起 specialist subagent
- subagent 只负责各自专长，不负责跨阶段路由或嵌套继续拉起其他 subagent

执行入口先读取：

1. `harness/workflows/_index.yaml`
2. `.claude/agents/` 中的 agent 合同
3. 当前 workflow
4. 对应 OpenSpec spec

### 默认 active agents

| 角色 | 模式 | 责任 |
|------|------|------|
| @source-evidence-agent | on-demand | 来源收集与证据缺口盘点 |
| @review-critic-agent | review gate | 独立技术评审与 traceability audit |
| @publish-agent | publish gate | artifact 提炼与 update impact scan |
| @diagram-agent | conditional | primitive / mechanism-heavy / 明确需要图表时启用 |

### fallback

若运行环境不支持真实 subagent：

- 仍按 active agents 的 contract 顺序执行
- 不得跳过 handoff artifact 与 quality gate
- 必须在最终总结中说明哪些角色被串行折叠执行

### 冰箱策略

当某个子任务被上游信息、网络限制、diagram contract 或 review gate 阻塞时：

1. 不让整个 pipeline 一起停摆
2. 将该子任务放入冰箱清单
3. 继续推进所有独立部分
4. 记录解冻条件与下游影响

冰箱清单至少应包含：

- blocked item
- blocked by
- wake condition
- downstream impact

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

**orchestrator**：主会话

**主链写作**：主会话

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

**orchestrator**：主会话

**主链写作**：主会话

**并行支持**：@source-evidence-agent

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

**并行窗口**：
- 主会话可以先写问题拆解、交付范围、完成标准
- @source-evidence-agent 并行收集来源并生成 `source-review.md`
- `plan.md` 定稿前必须回收 `source-review.md`

### 阶段 3：draft

**orchestrator**：主会话

**主链写作**：主会话

**条件角色**：@diagram-agent

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

**并行窗口**：
- 主会话可并行推进概述、术语表、设计取舍、能力边界
- @diagram-agent 可并行准备实体分类、图表清单、diagram package
- 如发现证据缺口，可短暂唤回 @source-evidence-agent 定向补证据

### 阶段 4：review gate

**orchestrator**：主会话

**primary specialist**：@review-critic-agent

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

**并行窗口**：
- @review-critic-agent 可在 author 收尾阶段预热 checklist 结构与审查重点
- 但正式 severity 与结论必须基于冻结后的 `draft.md`

### 阶段 5：artifact / publish

**orchestrator**：主会话

**primary specialist**：@publish-agent

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

**并行窗口**：
- @publish-agent 可提前计算目标路径与 impact scan 范围
- 但在 review 通过前不得写长期资产

## 关键 handoff artifact

| From | To | Artifact |
|------|----|----------|
| 命令层 / 主会话 | @source-evidence-agent | 研究问题、来源优先级、当前计划约束 |
| @source-evidence-agent | 命令层 / 主会话 | `source-review.md`、核心 excerpts、evidence gaps |
| 命令层 / 主会话 | @review-critic-agent | 待审 `draft.md`、未决问题 |
| @review-critic-agent | @publish-agent | `approved` / `approved with minor fixes` / `needs revision` 结论、必须修复项 |

## 完成后的总结要求

最终应汇报：

- active agents 列表
- 哪些角色并行、哪些串行
- 各阶段状态
- 使用的 change 路径
- 研究对象类型和路径
- 是否生成 diagram package
- 是否完成 publish / apply
