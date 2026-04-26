---
name: merge-change-into-knowledge
description: 将通过评审的 change 产物提炼并发布到长期 knowledge/ 主线。
---

# Skill: Merge Change into Knowledge

## Purpose

将通过评审的 change 产物提炼并发布到长期 `knowledge/` 主线。

## Triggers

用户请求：
- "合并这个 change"
- "完成 merge"
- "发布到 knowledge"

## Required Inputs

- **change_id**: Change ID
- **review_status**: 评审状态（必须允许继续 publish）

## Forbidden Inputs / Anti-patterns

- 不要在评审未完成时 merge
- 不要把过程文件整包复制到长期目录
- 不要继续沿用 `knowledge/topics` 旧路径

## Files to Read

- `harness/workflows/merge-workflow.md`
- `harness/rules/general/repo-governance.md`
- `harness/rules/general/update-policy.md`
- `openspec/changes/<change-id>/review/review-summary.md`

## Files to Write

### 1. Long-term Outputs

- `knowledge/analysis/.../artifact.md`
- `knowledge/decisions/.../artifact.md`
- `knowledge/decisions/.../verdict.md`（如适用）

### 2. Optional Impact Note

- update 场景需要时，在 change packet 或相关 review 中记录 impact scan

## Local Validation Steps

1. 确认 review gate 满足
2. 判断对象类型与目标路径
3. 提炼 durable 内容到长期目录
4. 如为 update，执行 impact scan
5. 提交 git 变更

## Output Contract

```yaml
change_id: <change-id>
publish_type: new-artifact|update-artifact|refactor-artifact
knowledge_paths:
  - knowledge/analysis/...
impact_scan: yes|no
commit_hash: <git commit hash>
```

## Quality Gate

- [ ] 评审结论允许继续
- [ ] 长期路径正确
- [ ] 过程文件未被直接提升
- [ ] update 场景已做 impact scan

## Failure Modes

### Merge 冲突

**处理**：手动解决冲突，确保不丢失内容。

### 评审后有新来源

**处理**：如 minor 则记录 follow-up，如 major 则创建新 change。
