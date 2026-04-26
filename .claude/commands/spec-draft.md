---
description: 为 research change 生成或修订 draft.md
argument-hint: "[change-path | change-name]"
---

# spec-draft

`draft` 阶段的主会话 orchestrator 入口。

用户传入参数：`$ARGUMENTS`

## 语言输出约束

- 主会话所有过程说明、阶段汇报与完成总结默认使用简体中文。
- 术语、命令、路径、文件名、schema key 与关键技术标识符优先保留英文。
- 不要使用英文过程提示句，例如 `Let me...`、`Now I will...`。

## 执行模型

- 本 command 是**渐进式执行**模式下的 draft 阶段入口，保持在主会话执行。
- 适用于用户只想完成 draft 阶段、暂不推进完整 pipeline 的场景。
- 如果需要端到端执行（request → plan → draft → review → artifact），应使用 `/spec-research` 而非本 command。
- 主会话负责路由、artifact 组装与 draft 完成状态判定。
- `draft.md` 的主链写作保留在主会话；不要再额外拆出 author subagent。
- **所有 PlantUML 图必须调用 `diagram-agent`**：当 plan.md 或图表清单中包含 PlantUML Architecture 或 PlantUML Sequence 图时，必须显式调用 `diagram-agent` subagent 进行生成和验证。
- 遇到 evidence gap 或需要链接重验证时，由主会话显式调用 `source-evidence-agent` subagent。
- 如果当前任务实际属于 governance / routing / repository architecture 工作，切换到 governance review 路由，并显式调用 `governance-review-agent`。治理路由判断以 `docs/governance/openspec-harness-boundary.md` 为准。
- 不要让一个 subagent 再去调用另一个 subagent。所有 delegation 都留在主会话。

## 规则来源

执行前读取并遵循：

- `harness/rules/_phase_index.yaml`（读取 `draft` 阶段依赖）
- `openspec/config.yaml`
- `openspec/schemas/blockchain-research/schema.yaml`
- 当前 change 的 `change.yaml`
- `openspec/schemas/blockchain-research/templates/draft.md`
- 根据 `change.yaml` 的 `task_type` 读取对应 profile：`openspec/schemas/blockchain-research/profiles/<task_type>.schema.yaml`
- 根据 `change.yaml` 的 `change_operation` 读取对应 operation：`openspec/schemas/blockchain-research/operations/<change_operation>.schema.yaml`
- `harness/rules/diagrams/diagram-policy.md`
- 需要图表时读取 `harness/workflows/diagram-workflow.md`

## OpenSpec Research Flow Contract

本命令必须遵守当前仓库的 blockchain-research schema：

```text
request.md -> plan.md -> sources/source-pack.md -> sources/evidence-map.md -> [notes/<source-slug>.md]* -> [claims/<claim-slug>.md]* -> draft.md -> review.md -> publish.md -> knowledge/**
```

约束：

- `draft.md` 是本 change 的唯一主候选产物。
- 不得生成 `work-products/*.md`。
- 不得直接写 `knowledge/**`。
- 复杂任务必须拆成 child changes。
- 必须遵守 `schema.yaml` 的 `x_artifact_flow`。

## 执行步骤

1. 从 `$ARGUMENTS`、当前工作目录或上下文中解析目标 change 目录。

2. 先读取 `change.yaml`、`request.md`、`plan.md`、`sources/source-pack.md`、现有 `draft.md` 与 draft template。

3. **术语依赖检查**：
   - 检查 plan.md 中依赖的 primitive 有哪些
   - 检查这些 primitive 的核心术语是否需要在【关键术语】章节定义
   - 如缺失，必须在生成 draft 时补充

4. 由主会话直接生成或修订 `draft.md` 主体：
   - 一个 change 只能有一个 `draft.md`
   - Candidate type 必须是 `source_note` | `primitive` | `synthesis` | `decision` 之一
   - 必须包含 Target Knowledge path
   - 必须包含 traceability 章节
   - decision 类型必须补充 Decision Analysis 与 Verdict Draft
   - 先生成【关键术语】章节（包含依赖 primitive 的术语）
   - 生成实体分类表和图表决策树
   - 生成图表清单表
   - **对于 PlantUML 图，调用 `diagram-agent` 生成和验证**（不得手写 PlantUML）
   - 对于 Mermaid/Markdown/ASCII 图，由主会话直接生成
   - 确保每张图表都有上下文引入段落

5. **图表质量检查**：
   - 检查 PlantUML 图是否通过 diagram-agent 验证
   - 检查图内 note 数量是否 ≤ 3 个
   - 检查每张图表是否有上下文引入段落
   - 检查依赖术语是否已定义

6. 当存在 evidence gap 时，由主会话显式调用 `source-evidence-agent`，并把结果并回 `draft.md`。

7. 只有在 required diagram 已验证或被明确标注为 unresolved，且 PlantUML diagram contract 检查通过时，才能声称 draft 完成。

8. 如果发现任务需要多个独立 final artifact，必须停止并建议拆 child changes。

## 完成总结

汇报：

- 最终使用的 change 路径
- 更新了哪些 section
- 是否启用了 `diagram-agent` 或 `source-evidence-agent`
- **diagram contract validation 结果**（必须汇报以下内容）：
  - PlantUML 图数量及验证状态（成功/失败）
  - 图内 note 数量检查（每张图 ≤ 3 个）
  - 图表上下文引入检查（每张图都有引入段落）
- **术语依赖检查**结果：
  - 依赖 primitive 的核心术语是否已定义
  - 如未定义，是否已补充或标注为 unresolved
- review 前仍未解冻的 fridge items
