# Skill: Simplify Diagram

## Purpose

简化现有图表，在保证准确性的前提下提高可读性。

## Triggers

用户请求：
- "简化这个图"
- "让图更易懂"
- "创建简化版"

## Required Inputs

- **diagram_id**: 原图 ID
- **target_level**: 目标简化级别 (L1/L2/L3)
- **purpose**: 简化目的

## Forbidden Inputs / Anti-patterns

- 不要为简化牺牲准确性
- 不要省略核心机制
- 不要忽略简化标注
- 不要改变原图的语义

## Files to Read

- `harness/workflows/diagram-workflow.md` - 图表流程
- `harness/rules/diagrams/simplification-policy.md` - 简化政策
- 原 diagram source 和 model

## Files to Write

### 1. Simplified Diagram Source

`openspec/changes/<change-id>/diagrams/source/<diagram-id>-simplified.puml`

### 2. Simplification Notes

`openspec/changes/<change-id>/diagrams/reviews/<diagram-id>-simplification.md`

## Local Validation Steps

1. 确定简化策略
2. 应用简化
3. 验证语义不变
4. 添加简化标注

## Output Contract

```yaml
original_diagram_id: <diagram-id>
simplified_diagram_id: <diagram-id>-simplified
simplification_level: L1|L2|L3
source_path: openspec/changes/<change-id>/diagrams/source/<simplified-id>.puml
status: success|needs-review
```

## Quality Gate

- [ ] 核心组件保留
- [ ] 关键关系保留
- [ ] 简化标注添加
- [ ] 组件数量合理
- [ ] 准确性未受损

## Failure Modes

### 简化后语义改变

**处理**：恢复被错误简化的元素。

### 无法进一步简化

**处理**：建议拆分而非简化。

### 简化标注缺失

**处理**：补充标注说明简化内容。

## When to Stop and Ask for Manual Triage

- 简化导致重大语义改变
- 用户要求过度简化
- 原图已经是最简
