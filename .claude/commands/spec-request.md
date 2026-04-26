---
description: 为 research change 生成或修订 request.md
argument-hint: "[change-path | change-name]"
---

# spec-request

`request` 阶段的主会话 orchestrator 入口。

用户传入参数：`$ARGUMENTS`

## 语言输出约束

- 主会话所有过程说明、阶段汇报与完成总结默认使用简体中文。
- 术语、命令、路径、文件名、schema key 与关键技术标识符优先保留英文。
- 不要使用英文过程提示句，例如 `Let me...`、`Now I will...`。

## 执行模型

- 本 command 是**渐进式执行**模式下的 request 阶段入口，保持在主会话执行。
- 适用于用户只想先完成 request 阶段、暂不推进完整 pipeline 的场景。
- 如果需要端到端执行（request → plan → draft → review → artifact），应使用 `/spec-research` 而非本 command。
- 主会话负责路由判断、目标路径解析、质量门控与最终写入。
- `request.md` 的主链写作保留在主会话；不要再额外拆出 author subagent。
- 如果当前任务实际是在改 OpenSpec / Harness / `.claude/` / `AGENTS.md` / `docs/governance/`，不要走 research pipeline，改走 governance review 路由，并显式调用 `governance-review-agent`。
- 不要让一个 subagent 再去调用另一个 subagent。所有 delegation 都由主会话决定。

## 规则来源

执行前读取并遵循：

- `harness/rules/_phase_index.yaml`（读取 `request` 阶段依赖）
- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/schemas/blockchain-research/templates/request.md`
- `harness/workflows/request-phase.md`

## 执行步骤

1. 从 `$ARGUMENTS`、当前工作目录或上下文中解析目标 change 目录。
2. 如果无法安全确定目标，询问用户 change 路径或 change 名称。
3. 读取 schema、template、stage spec 与现有 `request.md`。
4. 由主会话直接生成或修订 `request.md`，严格遵循 canonical template 与阶段边界。
5. 完成前检查最终文件是否遵循 canonical template，且没有漂移到 plan / draft 职责。

## 完成总结

汇报：

- 最终使用的 change 路径
- 对象类型与研究路径
- 记录了哪些核心问题
- 下一步是否建议进入 `/spec-plan`
- 是否还有 fridge items / unresolved inputs

## Validation 自检

- [ ] `research_type` / `research_path` 已声明
- [ ] 3-5 个开放性问题已定义，且与对象类型匹配
- [ ] 覆盖范围与非目标已明确
- [ ] 预期输出与对象类型匹配
- [ ] 文件符合 `openspec/schemas/blockchain-research/templates/request.md` 模板结构
