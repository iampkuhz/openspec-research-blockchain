---
description: 评审或实施 governance、routing 与 repository architecture 相关改动
argument-hint: "[scope | change-path | target-files]"
---

# spec-governance-review

governance 与 routing 类任务的主会话 orchestrator 入口。

用户传入参数：`$ARGUMENTS`

## 语言输出约束

- 主会话所有过程说明、阶段汇报与完成总结默认使用简体中文。
- 术语、命令、路径、文件名、schema key 与关键技术标识符优先保留英文。
- 不要使用英文过程提示句，例如 `Let me...`、`Now I will...`。

## 何时使用

当任务会对以下路径做 governance-significant 变更时，使用本 command：

- `openspec/**`
- `harness/**`
- `.claude/**`
- `AGENTS.md`
- `docs/governance/**`

尤其是影响以下内容时：

- schema
- spec
- template
- workflow
- rule
- subagent routing
- command routing
- repository architecture

如果目标是 **周期性 repo-wide 规约体系体检**，例如排查孤岛文件、死引用、失效脚本 gate、索引链缺口，而不是评审某次具体治理改动，则不要使用本 command，改用 `spec-system-audit.md`。

## 执行模型

- 本 command 是 governance / routing / repository architecture 变更的评审入口，保持在主会话执行。
- 主会话负责 scope 判断、影响范围分析、实际改动与最终集成。
- 由主会话显式调用 `governance-review-agent` subagent 做边界评审与一致性检查。
- 如果任务既包含 governance review，也包含具体实现修改，治理评审先做，实际文件改动仍由主会话负责整合。
- 不要让一个 subagent 再去调用另一个 subagent。

## 规则来源

执行前读取并遵循：

- `docs/governance/openspec-harness-boundary.md`
- `harness/workflows/governance-review-workflow.md`
- `harness/rules/_index.yaml`
- 所有受影响的 schema / spec / workflow / rule / command / agent 文件

## 执行步骤

1. 从 `$ARGUMENTS`、当前工作目录或当前 diff 中解析目标 scope。
2. 在编辑前先读取 boundary 文档。
3. 由主会话显式调用 `governance-review-agent` subagent，检查 boundary ownership、duplicated policy 与 downstream impact。
4. 由主会话实施具体修改。
5. 如果当前 change 维护治理评审产物，则在实现一致后同步更新 governance review artifact。

## 完成总结

汇报：

- 本次变更覆盖的文件或目录
- 是否启用了 `governance-review-agent`
- 关键 boundary decision
- 受影响的 workflow / rule / command / agent
- 是否仍需要 follow-up migration work
