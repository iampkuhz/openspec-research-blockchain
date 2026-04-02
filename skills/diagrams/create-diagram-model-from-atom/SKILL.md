# Skill: Create Diagram Model from Atom

## Purpose

从 knowledge atoms 提取图表模型，为创建 PlantUML 图做准备。

## Triggers

用户请求：
- "为这个机制创建图"
- "可视化这个架构"
- "创建 diagram model"

## Required Inputs

- **topic**: 主题名称
- **atom**: 源 atom 名称
- **diagram_type**: 图类型 (component/sequence/state/deployment)
- **purpose**: 图的目的

## Forbidden Inputs / Anti-patterns

- 不要混用不同抽象层的组件
- 不要创建超过 10 个组件的图（考虑拆分）
- 不要忽略关系语义
- 不要直接从 atom 复制而不建模

## Files to Read

- `harness/workflows/diagram-workflow.md` - 图表流程
- `harness/rules/diagrams/diagram-selection-matrix.md` - 图选择矩阵
- `harness/rules/diagrams/abstraction-boundaries.md` - 抽象边界规则
- `harness/rules/diagrams/relationship-rules.md` - 关系规则
- 源 atoms（如 core-mechanism.md）

## Files to Write

### 1. Diagram Model

`openspec/changes/<change-id>/diagrams/models/<diagram-id>-model.yaml`

### 2. Diagram Plan

`openspec/changes/<change-id>/diagrams/diagram-plan.yaml`

## Local Validation Steps

1. 检查组件列表是否完整
2. 检查关系是否都有源和目标
3. 检查抽象层标注
4. 检查是否有循环依赖

## Output Contract

```yaml
diagram_id: <diagram-id>
model_path: openspec/changes/<change-id>/diagrams/models/<diagram-id>-model.yaml
components_count: <数量>
relationships_count: <数量>
status: model-ready|needs-revision
```

## Quality Gate

- [ ] 组件在 atoms 中有定义
- [ ] 关系语义正确
- [ ] 抽象层不混用
- [ ] 组件数量合理 (<10)
- [ ] 无循环依赖

## Failure Modes

### 组件在 atoms 中无定义

**处理**：要求先补充 atom 定义，或在 model 中标注为 external。

### 关系语义不明确

**处理**：检查 atoms 中的描述，明确关系类型。

### 组件过多

**处理**：建议拆分为 overview + detail 多图。

## When to Stop and Ask for Manual Triage

- 组件和关系过于复杂无法合理建模
- 抽象层严重混用无法分离
- 源 atom 本身不清晰
