---
description: 为 research change 生成或修订 draft.md
argument-hint: "[change-path | change-name]"
---

# spec-draft

`draft` 阶段的主会话 orchestrator 入口。

用户传入参数：`$ARGUMENTS`

## 执行模型

- 保持在主会话执行。主会话负责路由、artifact 组装与 draft 完成状态判定。
- `draft.md` 的主链写作保留在主会话；不要再额外拆出 author subagent。
- 需要 diagram decision tree、brief、diagram package 或 contract validation 支持时，由主会话显式调用 `diagram-agent` subagent。
- 遇到 evidence gap 或需要链接重验证时，由主会话显式调用 `source-evidence-agent` subagent。
- 如果当前任务实际属于 governance / routing / repository architecture 工作，切换到 governance review 路由，并显式调用 `governance-review-agent`。
- 不要让一个 subagent 再去调用另一个 subagent。所有 delegation 都留在主会话。

## 规则来源

执行前读取并遵循：

- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/schemas/blockchain-research/templates/draft.md`
- `openspec/specs/draft-generation/spec.md`
- `openspec/specs/diagram-policy/spec.md`
- 需要图表时读取 `harness/workflows/diagram-workflow.md`

## 执行步骤

1. 从 `$ARGUMENTS`、当前工作目录或上下文中解析目标 change 目录。
2. 先读取 `request.md`、`plan.md`、现有 `draft.md` 与 draft template。
3. 由主会话直接生成或修订 `draft.md` 主体，并负责把 sources / diagrams 的稳定结果吸收到正文。
4. 当需要图表时，由主会话显式调用 `diagram-agent`；draft 是否可视为完成，仍由主会话判断。
5. 当存在 evidence gap 时，由主会话显式调用 `source-evidence-agent`，并把结果并回 `draft.md`。
6. 只有在 required diagram 已验证或被明确标注为 unresolved，且 PlantUML diagram contract 检查通过时，才能声称 draft 完成。

## 完成总结

汇报：

- 最终使用的 change 路径
- 更新了哪些 section
- 是否启用了 `diagram-agent` 或 `source-evidence-agent`
- diagram contract validation 结果
- review 前仍未解冻的 fridge items
