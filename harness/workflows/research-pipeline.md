# Research Pipeline - 端到端研究流程

## 目标

端到端完成一个 research change 的完整生命周期，由主会话 orchestrator 按 `research_type` 路由到对应 author agent，specialist subagent 按需介入。

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
- `artifact.md` / `verdict.md`

## 执行模式

### 默认模式：主会话 orchestrator + author agent + specialist subagent

执行入口保持在**主会话**：

- 主会话负责读取 workflow / spec / template
- 主会话负责判断目标 change、路由到对应 author agent、阶段推进、质量门控与最终落盘
- author agent 负责 `request` / `plan` / `draft` 主链写作
- 主会话按需要显式拉起 specialist subagent

### Author Agent 路由

| research_type | 路由到的 author agent | 执行模式 |
|---------------|----------------------|----------|
| `primitive` | `primitive-author` | 单个 primitive 全链路写作 |
| `synthesis` | `synthesis-author` | 先并行执行依赖 primitive，再合成对比 |
| `decision` | `decision-author` | 先并行执行依赖 primitive，再场景决策分析

### 默认 active agents

| 角色 | 模式 | 责任 |
|------|------|------|
| `source-evidence-agent` | 主会话按 handoff 调用 | 来源收集与证据缺口盘点 |
| `diagram-agent` | 主会话按 handoff 调用 | 图表生成与验证 |
| `review-critic-agent` | 主会话在 draft 后调用 | 独立技术评审与 traceability audit |
| `publish-agent` | 主会话在 review 通过后调用 | artifact 提炼与 update impact scan |

### Synthesis 三阶段执行

当 `research_type` 为 `synthesis` 时：

```
阶段 1: 依赖发现
  主会话读取 synthesis request.md 的依赖声明
  对每个缺失的 primitive: 创建 change + 调用 primitive-author 执行全链路

阶段 1.5: primitive quality gate（不可跳过）
  对阶段 1 产生的每个 primitive change:
    → review-critic-agent 评审 draft.md
    → publish-agent 提炼 artifact 到 knowledge/
  只有当所有 primitive 均通过 review + publish 后，才允许进入阶段 2

阶段 2: synthesis 合成
  主会话调用 synthesis-author
  synthesis-author 从各 primitive draft.md（以及已 publish 的 knowledge/ artifact）中提取信息做横向对比
  draft 冻结后 → review-critic-agent → publish-agent
```

### Decision 三阶段执行

当 `research_type` 为 `decision` 时：

```
阶段 1: 依赖发现
  主会话读取 decision request.md 的依赖声明
  对每个缺失的 primitive: 创建 change + 调用 primitive-author 执行全链路
  对每个缺失的 synthesis: 创建 change + 调用 synthesis-author 执行全链路
  对已有的 primitive/synthesis: 校验深度是否满足所需深度，不足时同样补齐

阶段 1.5: 依赖 quality gate（不可跳过）
  对阶段 1 产生的每个 primitive 和 synthesis change:
    → review-critic-agent 评审 draft.md
    → publish-agent 提炼 artifact 到 knowledge/
  只有当所有依赖 change 均通过 review + publish 后，才允许进入阶段 2

阶段 2: decision 合成
  主会话调用 decision-author
  decision-author 从各 primitive/synthesis draft.md（以及已 publish 的 knowledge/ artifact）中提取候选方案的能力评估和边界
  draft 冻结后 → review-critic-agent → publish-agent
```

**依赖层级**：
- `primitive`：单个协议、机制、产品的底层研究
- `synthesis`：多个 primitive 的横向对比、演进分析（如需要）
- `decision` 从这两层提取证据，不得脱离依赖 draft 独立撰写候选方案评估

**约束**：阶段 3 禁止在阶段 2 所有依赖（primitive + synthesis）的 draft 完成前开始。
decision-author 不得脱离 primitive draft / synthesis draft 独立撰写候选方案评估。

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

**执行者**：author agent（primitive-author / synthesis-author / decision-author）

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

**执行者**：author agent

**并行支持**：`source-evidence-agent`（由主会话根据 author handoff 调用）

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

**执行者**：author agent

**条件角色**：`diagram-agent`（由主会话根据 author handoff 调用）

**输入**：
- `request.md`
- `plan.md`
- `sources/`
- 已有 `draft.md`（如有）
- 依赖 primitive 的 `draft.md`（synthesis 模式）

**输出**：
- `draft.md`
- `diagrams/`（如适用）

**强制要求**：

1. 先做实体分类
2. 再做图表决策树
3. 如需 PlantUML，只能通过用户级 skill 生成 diagram package
4. draft 完成后必须执行 diagram contract 校验

### 阶段 4：review gate

**orchestrator**：主会话

**primary specialist**：`review-critic-agent`

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

**orchestrator**：主会话

**primary specialist**：`publish-agent`

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
| 主会话 | author agent | 研究问题、change 路径、预算约束 |
| author agent | 主会话 | 来源 / 图表 handoff、未决问题、正文主链草稿 |
| 主会话 | source-evidence-agent | 研究问题、来源优先级、当前计划约束 |
| source-evidence-agent | 主会话 | `source-review.md`、核心 excerpts、evidence gaps |
| 主会话 | diagram-agent | 图表需求单、正文上下文、diagram type |
| diagram-agent | 主会话 | diagram package、validation 结果、contract issue |
| 主会话 | author agent | 已完成的 `sources/` / `diagrams/` handoff |
| author agent | 主会话 | 完成的 `draft.md`、未决问题列表 |
| 主会话 | review-critic-agent | 待审 `draft.md`、未决问题 |
| review-critic-agent | 主会话 | `approved` / `approved with minor fixes` / `needs revision` 结论、必须修复项 |
| 主会话 | publish-agent | 通过 review 的 change packet、目标路径 |

## 完成后的总结要求

最终应汇报：

- active agents 列表
- 哪些角色并行、哪些串行
- 各阶段状态
- 使用的 change 路径
- 研究对象类型和路径
- 是否生成 diagram package
- **每个 change 的 review 状态**：review-critic-agent 结论
- **每个 change 的 publish 状态**：publish-agent 是否执行、artifact 提升路径
- 是否完成 publish / apply

**阶段间 quality gate（必须执行）**：

- 在 synthesis 模式中，阶段 1.5（primitive quality gate）必须对所有依赖 primitive 执行 review + publish 后，才允许进入阶段 2
- 在 decision 模式中，阶段 1.5（依赖 quality gate）必须对所有依赖 primitive/synthesis 执行 review + publish 后，才允许进入阶段 2
- **不得以"后续 change 还需要这个 draft 做依赖"为由跳过 review/publish**——synthesis 消费的是 openspec/changes/ 下的 draft.md，publish 提升的是 knowledge/ 下的 artifact.md，两者不冲突

**任务状态清理（必须执行）**：
- 所有通过 `TaskCreate` 创建的任务，在对应阶段完成后必须调用 `TaskUpdate` 标记为 `completed`
- 总结输出前确保 TaskList 状态与实际进度一致，不得遗留 `in_progress` 的脏任务
