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

## Command 定位

`/spec-governance-review` 是治理入口，不执行普通 research artifact flow。

它负责：

- 审查 OpenSpec / Harness / command / agent / skill / hook / script 的职责边界
- 发现 stale reference、duplicated policy、routing gap、loading overreach
- 按需调用 governance review 或 spec system audit agent
- 输出治理问题清单、修复建议，或在高置信范围内执行小修复

它不负责：

- 生成普通 research `request.md` / `plan.md` / `draft.md`
- 收集来源或写研究正文
- 发布 `knowledge/**`

## 必读文件

| 文件 | 作用 |
|---|---|
| `docs/governance/openspec-harness-boundary.md` | 判断 OpenSpec / Harness / command 分层 |
| `harness/governance/command-skill-boundary.md` | 判断 command、skill、workflow、rule、hook 边界 |
| `harness/governance/agent-boundaries.md` | 判断 multi-agent 与 capsule 边界 |
| `.claude/agents/CONTRACT.md` | 修改或审查 agent 时校验最小合同 |
| `harness/workflows/governance-review-workflow.md` | 治理评审执行流程 |
| `harness/workflows/_index.yaml`、`harness/rules/_phase_index.yaml` | 检查 workflow / phase 引用链 |

## 可用 Skill packages

| Capability | Skill name | Skill path | Fallback |
|---|---|---|---|
| 审查 skill 职责边界 | `governance-review-boundaries` | `skills/governance/review-execution-boundaries/SKILL.md` | 使用本命令的内联步骤 |
| 清理旧流程产物 | `governance-cleanup-legacy` | `skills/governance/cleanup-legacy-flow/SKILL.md` | 使用本命令的内联步骤 |
| 审查 OpenSpec/Harness/Command 一致性 | `governance-review-system` | `skills/governance/review-research-system/SKILL.md` | 使用本命令的内联步骤 |

如果 Claude Code 未自动加载上述 skill，必须按本命令内联步骤执行，不得中止。

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
