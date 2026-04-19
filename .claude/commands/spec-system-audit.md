---
description: 对仓库规约体系做周期性触发链、索引链和死引用审计；可只审计，也可审计后顺手修复高置信问题
argument-hint: "[scope | audit-only | audit-fix | report-path]"
---

# spec-system-audit

仓库规约体系卫生检查的专用 command 入口。

用户传入参数：`$ARGUMENTS`

## 语言输出约束

- 主会话所有过程说明、阶段汇报与完成总结默认使用简体中文。
- 术语、命令、路径、文件名、schema key 与关键技术标识符优先保留英文。
- 不要使用英文过程提示句，例如 `Let me...`、`Now I will...`。

## 何时使用

当目标不是“修改某一条具体规约”，而是对整个规约体系做卫生检查或定期清理时，使用本 command：

- 周期性审查 `AGENTS.md`、`CLAUDE.md`、`.claude/**`、`openspec/**`、`harness/**`
- 排查 direct orphan / low-probability orphan
- 排查 dead references、旧命令名、旧脚本路径、失效示例
- 复核渐进式加载是否合理
- 在大批 governance 改动后做一次 repo-wide cleanup

## 默认范围

如果 `$ARGUMENTS` 未指定范围，默认审计：

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/**`
- `openspec/**`（不含 `openspec/changes/**`）
- `harness/**`
- `docs/governance/**`
- `skills/**`
- `scripts/**`

## 执行模型

- 本 command 由主会话 orchestrator 驱动。
- 主会话显式调用 `spec-system-audit-agent` 执行仓库规约体系审计。
- 如审计中发现职责边界争议或分层重构问题，主会话再决定是否补调 `governance-review-agent`。
- 不要让 subagent 再去调用其他 subagent。

## 规则来源

执行前读取并遵循：

- `harness/workflows/spec-system-audit-workflow.md`
- `docs/governance/openspec-harness-boundary.md`
- `harness/workflows/_index.yaml`
- `harness/rules/_index.yaml`
- `harness/rules/_phase_index.yaml`
- `.claude/README.md`
- 受影响的 command / agent / workflow / rule / spec / script / skill 文件

## 执行步骤

1. 解析 `$ARGUMENTS`，确定 scope、模式（`audit-only` / `audit-fix`）与是否需要 report-path。
2. 主会话调用 `spec-system-audit-agent`，要求其先从索引层构建触发链，再按需展开叶子文件。
3. 先输出 findings 和 cleanup queue：
   - direct orphan
   - low-probability orphan
   - dead reference
   - loading gap / loading overreach
   - boundary drift
4. 若模式为 `audit-fix`，按 cleanup queue 顺序修复高置信问题。
5. 修复后重新做引用可达性与配置解析复检。
6. 如用户要求落盘，则把审计结果写到指定 report path。

## 手工触发方式

定期手工清理时，优先用以下说法触发：

- `运行 spec-system-audit，范围 AGENTS.md、CLAUDE.md、.claude、openspec、harness，只审计不修改`
- `运行 spec-system-audit，范围 .claude、harness、docs/governance，审计并修复高置信问题`
- `运行 spec-system-audit，默认全仓范围，输出一份 cleanup queue`
- `运行 spec-system-audit，并把结果落盘到 harness/reports/spec-system-audit-YYYY-MM-DD.md`

如果你已经知道想清理哪一层，也可以直接说：

- `请用 spec-system-audit 检查 command / agent 路由`
- `请用 spec-system-audit 检查 openspec 与 harness 的触发链`
- `请用 spec-system-audit 只扫描孤岛文件和死引用`

## 完成总结

汇报：

- 本次审计范围
- 运行模式（`audit-only` / `audit-fix`）
- 是否启用了 `spec-system-audit-agent`
- direct orphan / low-probability orphan 结果
- dead reference / invalid gate 结果
- cleanup queue
- 已修复文件与复检结果
- 是否建议升级到 `governance-review-agent`
