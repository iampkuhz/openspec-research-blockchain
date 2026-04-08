---
description: 为 research change 生成或修订 request.md
argument-hint: "[change-path | change-name]"
---

# spec-request

`request` 阶段的主会话 orchestrator 入口。

用户传入参数：`$ARGUMENTS`

## 执行模型

- 保持在主会话执行。主会话负责路由判断、目标路径解析、质量门控与最终写入。
- `request.md` 的主写作者由主会话显式调用 `research-author-agent` subagent。
- 如果当前任务实际是在改 OpenSpec / Harness / `.claude/` / `AGENTS.md` / `docs/governance/`，不要走 research pipeline，改走 governance review 路由，并显式调用 `governance-review-agent`。
- 不要让一个 subagent 再去调用另一个 subagent。所有 delegation 都由主会话决定。

## 规则来源

执行前读取并遵循：

- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/schemas/blockchain-research/templates/request.md`
- `openspec/specs/request-generation/spec.md`

## 执行步骤

1. 从 `$ARGUMENTS`、当前工作目录或上下文中解析目标 change 目录。
2. 如果无法安全确定目标，询问用户 change 路径或 change 名称。
3. 读取 schema、template、stage spec 与现有 `request.md`。
4. 由主会话显式调用 `research-author-agent` subagent 生成或修订 `request.md`。
5. 完成前检查最终文件是否遵循 canonical template，且没有漂移到 plan / draft 职责。

## 完成总结

汇报：

- 最终使用的 change 路径
- 对象类型与研究路径
- 记录了哪些核心问题
- 下一步是否建议进入 `/spec-plan`
- 是否还有 fridge items / unresolved inputs
