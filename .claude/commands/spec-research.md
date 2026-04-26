---
description: 由主会话 orchestrator 执行端到端 research pipeline，按 research_type 路由到对应 author agent
argument-hint: "[change-path | research-topic]"
---

# spec-research

本仓库的端到端 command 入口。

用户传入参数：`$ARGUMENTS`

## 语言输出约束

- 主会话所有过程说明、阶段汇报与完成总结默认使用简体中文。
- 术语、命令、路径、文件名、schema key 与关键技术标识符优先保留英文。
- 不要使用英文过程提示句，例如 `Let me...`、`Now I will...`。

## 执行模型与边界

本 command 是端到端 pipeline 的**用户入口**和**orchestrator 驱动**。
职责边界遵循三层分离原则：

| 层 | 负责内容 | 入口 |
|----|----------|------|
| Command（本文件） | 用户入口、路由判断、orchestrator 调度、完成总结 | `.claude/commands/spec-research.md` |
| Harness | Pipeline 阶段展开、Concurrency 控制、Fallback 策略、Subagent 路由与调度 | `harness/workflows/research-pipeline.md` |
| OpenSpec | Artifact graph、Artifact flow、Schema 约束、Profile/Operation 差异化规则 | `openspec/config.yaml` + `openspec/schemas/blockchain-research/schema.yaml` |

**Command 不应该做**：

- 不在 command 中内联 harness 的并发参数、分批策略、fallback 步骤
- 不在 command 中重新定义 schema.yaml 已有的 artifact graph 和 flow
- 不在 command 中硬编码 profile/operation 的路径

**Command 应该做**：

- 声明任务类型（research vs governance）
- 读取 OpenSpec 配置获取 artifact 模型
- 委托给 harness workflow 执行阶段展开
- 调度 subagent 并回收 handoff
- 输出完成总结

## 规则来源

执行前读取并遵循：

- `openspec/config.yaml`（workflow 配置、artifact 依赖与 apply 规则）
- `openspec/schemas/blockchain-research/schema.yaml`（artifact graph、x_artifact_flow、profiles、operations）
- 当前 change 的 `change.yaml`（实例化 manifest）
- `harness/workflows/research-pipeline.md`（端到端 pipeline 的阶段展开、Concurrency、Fallback、Subagent 路由）
- `harness/rules/_phase_index.yaml`（阶段依赖索引）
- `.claude/agents/CONTRACT.md`（agent 合同校验规范）
- 按 `change.yaml` 的 `task_type` 读取对应 profile：`openspec/schemas/blockchain-research/profiles/<task_type>.schema.yaml`

## OpenSpec Research Flow Contract

本命令必须遵守当前仓库的 blockchain-research schema：

```text
request.md -> plan.md -> sources/source-pack.md -> sources/evidence-map.md -> [notes/<source-slug>.md]* -> [claims/<claim-slug>.md]* -> draft.md -> review.md -> publish.md -> knowledge/**
```

约束：

- `draft.md` 是本 change 的唯一主候选产物。
- 不得生成 `work-products/*.md`。
- 不得直接写 `knowledge/**`，必须通过 `publish.md` 映射。
- 复杂任务必须拆成 child changes。
- 必须遵守 `schema.yaml` 的 `x_artifact_flow`。

## 路由守卫

执行前先判断任务类型：

- 如果是普通 research change，按下方 pipeline 执行。
- 如果任务会修改 `openspec/**`、`harness/**`、`.claude/**`、`AGENTS.md`、`docs/governance/**`，且影响 routing、governance、schema、spec、template、workflow、rule 或 repository architecture，则**不要**走 research pipeline，改走 governance review 路由，并显式调用 `governance-review-agent`。

治理路由判断以 `docs/governance/openspec-harness-boundary.md` 和 `harness/workflows/governance-review-workflow.md` 为准。

## 执行步骤

### 0. Change 初始化

如果 `$ARGUMENTS` 是研究主题而不是现有 change 路径：

- 创建 change 目录
- 从 `request.md` 开始推进

如果 `$ARGUMENTS` 指向现有 change，则复用现有 change packet。

### 1. 读取 artifact 模型

创建或读取 `request.md` 后：

- 读取当前 change 的 `change.yaml`，获取 `task_type` 和 `change_operation`
- 根据 `task_type` 加载对应 profile
- 根据 `change_operation` 加载对应 operation
- 读取 `schema.yaml` 的 `x_artifact_flow` 确认阶段依赖

### 2. 路由到 author agent

根据 `task_type` 路由到对应 author agent：

| `task_type` | Author Agent |
|-------------|-------------|
| `primitive` | `primitive-author` |
| `synthesis` | `synthesis-author` |
| `decision` | `decision-author` |

主会话负责：

- 路由判断（根据 `task_type` 选择 author agent）
- 阶段推进
- specialist subagent 调度（`source-evidence-agent`、`diagram-agent`、`review-critic-agent`、`publish-agent`）
- handoff 回收
- 质量门控

详细阶段展开（primitive/synthesis/decision 的阶段步骤、Concurrency 控制、Fallback 策略、review + publish gate）由 `harness/workflows/research-pipeline.md` 定义，不在本 command 中重复。

### 3. 二次研究来源保护

在创建或校验 `request.md` 时，必须检查"范围与非目标"段：

- **二次研究禁止切断来源验证**：request.md 的"非目标"中**不得**包含"不扩展研究新来源"、"不引入新外部来源"、"基于既有分析已确认的事实"等切断来源搜索的表述。
- **既有 artifact 是起点，不是天花板**：二次研究的 request 必须明确既有 artifact 仅作为参考基线，仍需回源到原始项目仓库、文档、commit 历史等验证和补充信息。
- 如发现 request.md 已包含此类自我设限表述，**必须先修正 request.md 再继续**。

### 4. Fallback

**禁止直接 fallback**。必须先尝试调用 subagent，确认失败后向用户请求二次确认，用户明确同意后才可按相同 contract 串行继续。详见 `harness/workflows/research-pipeline.md` 的 Fallback 段。

- 如果网络限制阻塞来源收集，记录 evidence gap，不要伪造确定性。
- 如果 required PlantUML package 未通过 validation，不要声称 draft 已完成。

## 完成总结

汇报：

- 当前任务最终走的是 research flow 还是 governance routing
- 路由到的 author agent 类型（`primitive-author` / `synthesis-author` / `decision-author`）
- 使用了哪些 specialist subagent
- 各阶段状态
- 最终使用的 change 路径（如有 synthesis/decision，列出所有依赖 change 路径）
- **每个 change 的 review 状态**：是否调用了 `review-critic-agent`、评审结论
- **每个 change 的 publish 状态**：是否调用了 `publish-agent`、artifact 提升路径（`knowledge/` 下的具体路径）
- 是否生成了 `sources/`、`diagrams/`、`review/` 与 artifact 文件
- 是否还有 fridge items / evidence gap 未关闭

**强制检查**：在输出完成总结前，必须确认每个 change 均已通过 review gate + publish gate。如有 change 未完成 review/publish，必须在总结中明确列出，不得隐去。

**任务状态校验**：输出完成总结前，调用 `TaskList` 读取任务列表，逐项核对：
- 每个 change 对应的 task 是否已标记为 `completed`
- 是否有 `pending` 或 `in_progress` 的 task 实际已完成（说明漏标记）
- 如有不匹配，先调用 `TaskUpdate` 修正后再输出总结
- 禁止在 task 状态不正确的情况下口头声称"全部完成"
