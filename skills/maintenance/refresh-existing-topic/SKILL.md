# Skill: Refresh Existing Topic

## Purpose

刷新现有主题，更新过时的内容。

## Triggers

用户请求：
- "更新 <topic>"
- "刷新这个主题"
- "检查是否有新内容"

## Required Inputs

- **topic**: 主题名称
- **update_reason**: 更新原因 (spec-update/error-fix/ecosystem-change)

## Forbidden Inputs / Anti-patterns

- 不要直接修改 knowledge/（必须通过 OpenSpec change）
- 不要跳过影响范围评估
- 不要忽略向后兼容性

## Files to Read

- `harness/workflows/update-existing-knowledge.md` - 更新流程
- `harness/rules/general/update-policy.md` - 更新政策
- `knowledge/topics/<topic>/` - 现有知识
- `knowledge/topics/<topic>/changelog.md` - 历史变更

## Files to Write

### 1. OpenSpec Change

`openspec/changes/update-<topic>-<reason>-pass-1/`

### 2. Content Comparison

`openspec/changes/<change-id>/content-comparison.md`

### 3. Updated Atoms

在 change 目录中更新 atoms

## Local Validation Steps

1. 读取现有知识
2. 评估更新范围
3. 创建 change
4. 对比新旧内容
5. 执行更新
6. 更新 changelog
7. 处理向后兼容

## Output Contract

```yaml
change_id: <change-id>
update_type: atom-update|topic-update|topic-refactor
atoms_updated: [<atom list>]
breaking_changes: [yes|no]
dependencies_notified: [<topic list>]
```

## Quality Gate

- [ ] 更新原因明确
- [ ] 影响范围评估
- [ ] changelog 更新
- [ ] 向后兼容处理
- [ ] 依赖者通知

## Failure Modes

### 更新导致重大破坏

**处理**：考虑版本并存或创建新 topic。

### 依赖者反对

**处理**：记录意见，评估是否继续。

### 新来源与旧内容严重冲突

**处理**：可能需要重新研究而非简单更新。

## When to Stop and Ask for Manual Triage

- 更新范围超出预期
- 发现系统性错误需要重新研究
- 向后兼容无法保证
