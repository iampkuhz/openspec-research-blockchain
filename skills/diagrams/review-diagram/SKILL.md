# Skill: Review Diagram

## Purpose

评审创建好的图表，确保准确性、一致性、可读性。

## Triggers

用户请求：
- "评审这个图"
- "检查图的质量"
- "图是否符合规范"

## Required Inputs

- **diagram_id**: 图 ID
- **topic**: 主题名称

## Forbidden Inputs / Anti-patterns

- 不要跳过 checklist
- 不要忽略抽象层混用
- 不要只给模糊评价

## Files to Read

- `harness/workflows/diagram-workflow.md` - 图表流程
- `harness/rules/diagrams/diagram-review-checklist.md` - 评审清单
- `harness/rules/diagrams/abstraction-boundaries.md` - 抽象边界
- Diagram source 和 model
- 相关 atoms

## Files to Write

### 1. Diagram Review

`openspec/changes/<change-id>/diagrams/reviews/<diagram-id>-review.md`

### 2. Review Issues

`openspec/changes/<change-id>/diagrams/reviews/<diagram-id>-issues.yaml`

## Local Validation Steps

1. 完成 diagram-review-checklist
2. 检查抽象层一致性
3. 检查关系语义
4. 检查简化标注

## Output Contract

```yaml
diagram_id: <diagram-id>
issues_found: <数量>
by_severity:
  high: <数量>
  medium: <数量>
  low: <数量>
conclusion: approved|approved-with-minor-fixes|needs-revision
review_path: openspec/changes/<change-id>/diagrams/reviews/
```

## Quality Gate

- [ ] 准确性检查完成
- [ ] 一致性检查完成
- [ ] 可读性检查完成
- [ ] 简化标注检查
- [ ] 问题记录具体

## Failure Modes

### 发现抽象层混用

**处理**：标记为 medium/high，要求重新分层。

### 发现事实错误

**处理**：标记为 high，要求对照 atoms 修正。

### 图过于复杂

**处理**：标记为 medium，建议简化或拆分。

## When to Stop and Ask for Manual Triage

- 图需要完全重画
- 源 atom 本身有问题
- 评审意见存在重大分歧
