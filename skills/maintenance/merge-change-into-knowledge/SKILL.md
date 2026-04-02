# Skill: Merge Change into Knowledge

## Purpose

将通过评审的 change 产物合并到 knowledge/主线。

## Triggers

用户请求：
- "合并这个 change"
- "完成 merge"
- "发布到 knowledge"

## Required Inputs

- **change_id**: Change ID
- **review_status**: 评审状态（必须为 approved）

## Forbidden Inputs / Anti-patterns

- 不要在评审未完成时 merge
- 不要跳过 merge 检查清单
- 不要忽略更新 indexes

## Files to Read

- `harness/workflows/merge-workflow.md` - 合并流程
- `harness/rules/general/repo-governance.md` - 仓库治理
- `harness/rules/general/update-policy.md` - 更新政策
- `openspec/changes/<change-id>/review/review-summary.md` - 评审总结

## Files to Write

### 1. Knowledge Files

`knowledge/topics/<domain>/<topic>/` 下的所有文件

### 2. Changelog

`knowledge/topics/<domain>/<topic>/changelog.md` (新增或更新)

### 3. Indexes

`knowledge/indexes/topic-index.md` (更新)

## Local Validation Steps

1. 确认 merge 条件满足
2. 确定 merge 类型
3. 复制产物到 knowledge/
4. 更新 changelog
5. 更新 indexes
6. 提交 commit
7. 归档 change

## Output Contract

```yaml
change_id: <change-id>
merge_type: new-topic|update-topic|refactor-topic
knowledge_path: knowledge/topics/<domain>/<topic>/
commit_hash: <git commit hash>
indexes_updated: yes|no
change_archived: yes|no
```

## Quality Gate

- [ ] 评审 approved
- [ ] 所有产物复制
- [ ] changelog 更新
- [ ] indexes 更新
- [ ] commit 创建
- [ ] change 归档

## Failure Modes

### Merge 冲突

**处理**：手动解决冲突，确保不丢失内容。

### 评审后有新来源

**处理**：如 minor 则记录，如 major 则创建新 change。

### 发现遗漏内容

**处理**：记录遗漏，创建 follow-up change。

## When to Stop and Ask for Manual Triage

- Git merge 冲突复杂
- 发现未评审的问题
- knowledge 结构与预期不符
