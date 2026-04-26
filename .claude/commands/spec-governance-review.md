---
description: 规约治理入口，审查 openspec / commands / skills / harness 的一致性，不作为普通研究任务入口
argument-hint: "[scope | target-files]"
---

# spec-governance-review

规约治理入口。审查 `openspec` / `commands` / `skills` / `harness` / `hooks` / `scripts` 的一致性。

用户传入参数：`$ARGUMENTS`

## 语言输出约束

- 所有过程说明、阶段汇报默认使用简体中文。
- 术语、命令、路径、文件名、schema key 与关键技术标识符优先保留英文。
- 不要使用英文过程提示句，例如 `Let me...`、`Now I will...`。

## OpenSpec Research Flow Contract

本命令必须遵守当前仓库的 `blockchain-research` schema。

主流程：

```text
request.md -> plan.md -> sources/source-pack.md -> sources/evidence-map.md -> [notes/<source-slug>.md]* -> [claims/<claim-slug>.md]* -> draft.md -> review.md -> publish.md -> knowledge/**
```

执行前必须读取：

- `openspec/config.yaml`
- `openspec/schemas/blockchain-research/schema.yaml`
- 当前 change 的 `change.yaml`
- `openspec/schemas/blockchain-research/profiles/<task_type>.schema.yaml`
- `openspec/schemas/blockchain-research/operations/<change_operation>.schema.yaml`

硬性约束：

- `draft.md` 是当前 change 的唯一主候选产物。
- 不得生成 `work-products/*.md`。
- 不得直接写 `knowledge/**`，除非当前命令是 `/spec-research-publish`，且 `publish.md` 已定义合法映射。
- 复杂任务必须拆成多个 child changes。
- decision 任务必须明确 `decision-criteria.md -> draft.md#Verdict Draft -> decision-verdict.md -> knowledge/decisions/**/verdict.md` 的关系。

## 参考 Skills

本命令会调用以下 skills：

- `skills/governance/review-openspec-contracts` — 审查 OpenSpec 合约一致性
- `skills/governance/review-command-routing` — 审查 command 与 skill 路由
- `skills/governance/review-skill-boundaries` — 审查 skill 职责边界
- `skills/governance/review-harness-rules` — 审查 Harness 规则一致性
- `skills/governance/review-hook-coverage` — 审查 Hook 覆盖率
- `skills/governance/cleanup-legacy-flow` — 清理旧流程产物

## 职责

1. 审查 `openspec` / `commands` / `skills` / `harness` / `hooks` / `scripts` 的一致性。
2. 发现 schema、command、skill、harness workflow、rule、hook validator 之间的 drift。
3. 输出治理问题清单、修复建议，必要时执行小范围规约修复。
4. **不作为普通研究任务入口**。
5. **不修改 knowledge/** 正文。

## 执行步骤

1. 从 `$ARGUMENTS` 确定审查 scope。
2. 读取 `docs/governance/openspec-harness-boundary.md`。
3. 调用对应 governance skill 做专项审查。
4. 输出治理问题清单与修复建议。
5. 高置信度项目可直接修复，其余建议转人工。

## 完成总结

汇报：

- 审查覆盖的范围
- 发现的一致性问题数量与严重程度
- 已自动修复项
- 需人工确认项
- 受影响的 workflow / rule / command / agent
