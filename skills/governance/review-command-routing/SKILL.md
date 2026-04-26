---
name: review-command-routing
description: 审查 .claude/commands/ 中的 command 文件是否与 skills、workflow 索引保持一致。
---

# 审查 Command 路由

## 适用场景

- 新增、删除或重命名 command 后，需要检查引用链是否完整。
- 发现 command 调用的 skill 不存在或已改名。

## 输入

- `.claude/commands/` 目录。
- `skills/` 目录。
- `harness/workflows/_index.yaml`。

## 输出

- 路由问题清单（死引用、缺失 skill、command 与 workflow 不一致）。
- 修复建议。

## 读取文件

- `.claude/commands/*.md`。
- `skills/*/SKILL.md`。
- `harness/workflows/_index.yaml`。

## 写入文件

- 治理评审报告（由调用方决定写入位置）。

## 禁止事项

- 不得直接删除 command 文件，只输出审查报告与修复建议。

## 自检

- 每个 command 引用的 skill 路径是否可解析？
- 是否存在 deprecated command 但缺少迁移提示？
