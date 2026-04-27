---
name: cleanup-legacy-flow
description: 识别并清理过时的 change 流程产物（孤立目录、过期引用、残留旧文件）。
---

# 清理旧流程产物

## 适用场景

- 发现 change 目录引用了已不存在的 skill 或命令。

## 输入

- `.claude/commands/` 目录。
- `.claude/skills/` 目录。
- `skills/` 目录。
- `openspec/changes/` 目录。

## 输出

- 清理清单（需要更新的文件、可安全删除的孤立目录）。
- 实际清理操作（高置信度项目）。

## 读取文件

- `.claude/commands/*.md`。
- `.claude/skills/` 下的 symlink。
- `skills/` 下的 `SKILL.md`。
- `openspec/changes/` 下的 change 文件。

## 写入文件

- 高置信度的清理修复（更新过时的 skill 引用为新的）。
- 清理报告（含已处理项与需人工确认项）。

## 禁止事项

- 不得删除含有用户可能在用的 change 目录。
- 不得清理需要人工判断的治理文件。

## 自检

- 清理操作是否只影响高置信度项目？
- 是否有 need-human-review 的项未处理？
