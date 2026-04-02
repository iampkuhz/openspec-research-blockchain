# Evaluation Plan: <Change Title>

## Evaluation Goals

[评估目标]

## Evaluation Criteria

### Accuracy

| Criterion | Method | Pass Threshold |
|-----------|--------|----------------|
| 所有 claims 有 sources 支撑 | 检查 claims/facts.yaml | 100% |
| 证据等级适当 | 评审检查 | 无 high severity issues |
| 无事实错误 | 技术评审 | 无 high severity issues |

### Consistency

| Criterion | Method | Pass Threshold |
|-----------|--------|----------------|
| 术语一致 | 检查全文 | 无 high severity issues |
| 与其他知识不冲突 | 对比现有知识 | 无 unresolved conflicts |

### Completeness

| Criterion | Method | Pass Threshold |
|-----------|--------|----------------|
| 核心内容完整 | 对照 template | 所有必选章节 |
| 边界条件说明 | 评审检查 | 明确列出 |
| 待决问题列出 | 检查 open-questions | 所有已知问题 |

### Readability

| Criterion | Method | Pass Threshold |
|-----------|--------|----------------|
| 5 秒理解主旨 | 非专家评审 | 能说出核心 |
| 结构清晰 | 评审检查 | 无 medium+ issues |
| 图表帮助理解 | diagram review | approved |

## Evaluation Methods

### Self Review

**Checklist**: harness/workflows/review-workflow.md 中的 checklist

**When**: 完成所有 writing 后

**Output**: review/checklist.yaml

### Technical Review

**Reviewer**: 领域专家或 Claude

**Focus**: 准确性、完整性

**Output**: review/issues.md

### Readability Review

**Reviewer**: 非本领域人员或 Claude

**Focus**: 可读性、结构

**Output**: review/issues.md

## Evaluation Schedule

| Review Type | Planned Date | Actual Date | Status |
|-------------|--------------|-------------|--------|
| Self Review | date | date | pending/in-progress/completed |
| Technical Review | date | date | pending/in-progress/completed |
| Readability Review | date | date | pending/in-progress/completed |

## Acceptance Criteria

- [ ] 所有 high severity issues 已修复
- [ ] medium severity issues 已修复或记录
- [ ] 评审结论为 approved 或 approved with minor fixes

## Post-Merge Evaluation

- [ ] 更新 indexes
- [ ] 通知依赖者
- [ ] 收集使用反馈
