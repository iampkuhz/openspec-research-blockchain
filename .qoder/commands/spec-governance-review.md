---
name: spec-governance-review
description: 规约治理入口，审查 openspec / commands / skills / harness 的一致性，不作为普通研究任务入口。
---

# spec-governance-review

规约治理入口。审查 `openspec` / `commands` / `skills` / `harness` / `hooks` / `scripts` 的一致性。

## 语言

所有过程说明、阶段汇报默认使用简体中文。

## Action Scope

- 审查 OpenSpec / Harness / command / agent / skill / hook / script 的职责边界
- 发现 stale reference、duplicated policy、routing gap、loading overreach
- 输出治理问题清单、修复建议
- **不作为普通研究任务入口**

## 必读文件

| 文件 | 作用 |
|------|------|
| `AGENTS.md` | 仓库导航、任务路由 |
| `docs/governance/openspec-harness-boundary.md` | 判断 OpenSpec / Harness / command 分层 |
| `harness/governance/command-skill-boundary.md` | 判断 command、skill、workflow、rule、hook 边界 |
| `harness/governance/agent-boundaries.md` | 判断 multi-agent 与 capsule 边界 |
| `harness/adapters/agent-adapter-contract.md` | 修改或审查 agent 时校验最小合同 |
| `harness/workflows/governance-review-workflow.md` | 治理评审执行流程 |

## 职责

1. 审查 `openspec` / `commands` / `skills` / `harness` / `hooks` / `scripts` 的一致性
2. 发现 schema、command、skill、harness workflow、rule 之间的 drift
3. 输出治理问题清单、修复建议
4. **不修改 knowledge/** 正文

## 执行步骤

1. 确定审查 scope
2. 读取 `docs/governance/openspec-harness-boundary.md`
3. 按 scope 检查一致性
4. 输出治理问题清单与修复建议

## 完成总结

汇报：
- 审查覆盖的范围
- 发现的一致性问题数量与严重程度
- 已自动修复项
- 需人工确认项
- 受影响的 workflow / rule / command / agent
