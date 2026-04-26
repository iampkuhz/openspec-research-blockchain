---
name: refresh-existing-topic
description: 刷新现有知识主题，更新过时内容与补充新证据。
---

# Skill: Refresh Existing Topic

## Purpose

刷新现有长期资产，处理规范更新、事实错误或生态变化。

## Triggers

用户请求：
- "更新 <topic>"
- "刷新这个主题"
- "检查是否有新内容"

## Required Inputs

- **target_path**: 目标长期资产路径或 topic 标识
- **update_reason**: 更新原因 (`spec-update` / `error-fix` / `ecosystem-change`)

## Forbidden Inputs / Anti-patterns

- 不要直接修改 `knowledge/`
- 不要跳过影响范围评估
- 不要假定所有 update 都只是局部修补

## 术语漂移检测（整合自 detect-term-drift）

刷新过程中如发现术语用法与既有 glossary/taxonomy 不一致，应记录为术语漂移报告，包含：
- 不一致的术语位置
- 冲突描述
- 建议的标准化用法

## Files to Read

- `harness/workflows/update-existing-knowledge.md`
- `harness/rules/general/update-policy.md`
- 目标 `artifact.md` / `verdict.md`

## Files to Write

### 1. OpenSpec Change

- `openspec/changes/update-<topic>-<reason>-pass-1/`

### 2. Content Comparison / Impact Note

- `openspec/changes/<change-id>/content-comparison.md`
- 或在 `plan.md` / `draft.md` 中显式记录

## Local Validation Steps

1. 读取现有长期资产
2. 评估 update 类型与影响范围
3. 创建 change
4. 完成 request / plan / draft
5. 评审并 publish

## Output Contract

```yaml
change_id: <change-id>
update_type: minor-update|major-update|refactor
target_paths:
  - knowledge/analysis/...
impact_scan: yes|no
breaking_changes: yes|no
```

## Quality Gate

- [ ] 更新原因明确
- [ ] 影响范围已评估
- [ ] 向后兼容处理已说明
- [ ] 如有上层依赖，已记录 follow-up 计划
