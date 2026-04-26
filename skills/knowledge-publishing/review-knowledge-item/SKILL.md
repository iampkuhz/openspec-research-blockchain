---
name: review-knowledge-item
description: 评审知识产出物，校验 artifact contract 与质量门。
---

# Skill: Review Knowledge Item

## Purpose

评审知识产出物，确保准确性、一致性、完整性、可读性。

## Triggers

用户请求：
- "评审这个研究"
- "检查 <topic> 的质量"
- "完成评审"

## Required Inputs

- **change_id** 或 **topic**: 评审对象
- **review_type**: 类型 (technical/readability/diagram/full)

## Forbidden Inputs / Anti-patterns

- 不要跳过 checklist 直接给结论
- 不要只给模糊评价
- 不要忽略 high severity 问题
- 不要在没有依据的情况下要求修改

## Files to Read

根据评审对象加载：

- `harness/workflows/review-workflow.md` - 评审流程
- `harness/rules/research/atom-definition-rules.md` (如适用)
- `harness/rules/research/atom-mechanism-rules.md` (如适用)
- `harness/rules/diagrams/diagram-review-checklist.md` (如图评审)
- `openspec/specs/evidence-policy/spec.md` - 证据政策

## Files to Write

### 1. Review Checklist

`openspec/changes/<change-id>/review/checklist.yaml`

### 2. Review Issues

`openspec/changes/<change-id>/review/issues.md`

### 3. Review Summary

`openspec/changes/<change-id>/review/review-summary.md`

## Local Validation Steps

1. 完成所有 checklist 检查项
2. 记录所有发现的问题
3. 给出明确的评审结论
4. 区分问题严重性

## Output Contract

```yaml
review_type: <类型>
issues_found: <数量>
by_severity:
  high: <数量>
  medium: <数量>
  low: <数量>
conclusion: approved|approved-with-minor-fixes|needs-revision
review_path: openspec/changes/<change-id>/review/
```

## Quality Gate

- [ ] 所有 checklist 完成
- [ ] 问题记录具体
- [ ] 严重性分级正确
- [ ] 评审结论明确
- [ ] 修复建议可操作

## Failure Modes

### 发现重大事实错误

**处理**：标记为 high severity，要求暂停 merge，重新研究。

### 发现证据缺口

**处理**：标记为 medium/high，要求补充来源或降低结论强度。

### 发现术语不一致

**处理**：标记为 medium，要求检查 glossary 并统一。

## When to Stop and Ask for Manual Triage

- 发现系统性错误需要重新研究
- 评审意见之间存在重大分歧
- 发现超出评审范围的问题
