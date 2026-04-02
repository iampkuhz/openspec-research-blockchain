# Diagram Workflow - 图表创建

## Goal

基于 knowledge atoms 创建图表，经历建模→渲染→验证→评审流程。

## Trigger

- 需要可视化机制/架构/流程
- atom 写作完成

## Required Inputs

- atoms/*.md
- claims/facts.yaml
- terms/terms.yaml

## Optional Inputs

- 现有 diagrams
- 简化级别要求

## Rule Set to Load

- harness/rules/diagrams/diagram-selection-matrix.md
- harness/rules/diagrams/abstraction-boundaries.md
- harness/rules/diagrams/relationship-rules.md
- harness/rules/diagrams/annotation-rules.md
- harness/rules/diagrams/simplification-policy.md

## Step-by-Step Procedure

### Step 1: 确定图表类型

根据内容选择：

| 内容 | 推荐类型 |
|------|----------|
| 组件关系 | Component Diagram |
| 时序流程 | Sequence Diagram |
| 状态变化 | State Diagram |
| 部署架构 | Deployment Diagram |

记录选择：
```yaml
# diagrams/diagram-plan.yaml
diagrams:
  - id: arch-overview
    type: component
    purpose: 展示核心组件关系
    target_atoms:
      - core-mechanism
    simplification_level: L2
```

### Step 2: 提取 Diagram Model

从 atoms 中提取图元素：

```yaml
# diagrams/models/<diagram-id>-model.yaml
diagram_id: arch-overview
source_atoms:
  - atoms/core-mechanism.md

components:
  - id: UserOperation
    label: UserOperation
    type: component
    layer: protocol
    stereotype: "<<protocol>>"
    source_claims:
      - claim-001

  - id: EntryPoint
    label: EntryPoint
    type: component
    layer: protocol
    stereotype: "<<protocol>>"
    source_claims:
      - claim-002

relationships:
  - from: UserOperation
    to: EntryPoint
    type: processes
    label: "processed by"
    source_claims:
      - claim-003
```

### Step 3: 创建 PlantUML Source

```plantuml
@startuml
title <标题>

skinparam <样式>

' 组件定义
component "UserOperation" as UO <<protocol>>
component "EntryPoint" as EP <<protocol>>

' 关系
UO --> EP : processed by

' 注释
note right of UO
  <b>说明</b>
  EIP-4337 定义的用户操作原子
end note

@enduml
```

### Step 4: 渲染 Diagram

```bash
scripts/diagrams/render.sh <diagram-id>
```

输出到：
- `diagrams/build/<diagram-id>.svg`
- `diagrams/build/<diagram-id>.png`

### Step 5: 验证 Diagram Model

```bash
scripts/diagrams/validate_diagram_model.py <diagram-id>
```

检查：
- [ ] 组件命名一致
- [ ] 关系语义正确
- [ ] 抽象层不混用
- [ ] stereotype 标注

### Step 6: 检查引用

```bash
scripts/diagrams/check_diagram_references.py <diagram-id>
```

检查：
- [ ] 所有组件在 atoms 中有定义
- [ ] 所有关系有 claim 支撑
- [ ] 简化已标注

### Step 7: 创建 Diagram Review

```markdown
# Diagram Review: <diagram-id>

**Diagram**: <diagram-id>
**Created At**: <date>
**Author**: <author>

## 准确性

- [ ] 组件/概念准确
- [ ] 关系语义正确
- [ ] 符合官方规范

## 抽象层一致性

- [ ] 未混用不同层
- [ ] stereotype 正确标注

## 可读性

- [ ] 组件数量合适
- [ ] 布局清晰
- [ ] 注释必要

## 问题

| ID | 维度 | 严重性 | 描述 | 状态 |
|----|------|--------|------|------|
| ISSUE-001 | accuracy | high | ... | open |

## 结论

- [ ] approved
- [ ] approved with minor fixes
- [ ] needs revision
```

### Step 8: 简化（可选）

如需要简化版本：

```plantuml
' 简化版 - 仅核心组件
component "UserOperation" as UO
component "EntryPoint" as EP

note bottom
  <b>简化说明</b>
  仅展示核心组件
  完整版见 architecture-full
end note
```

### Step 9: 集成到 Atoms

在 atoms 中引用图：

```markdown
## 核心架构

如图 1 所示，系统包含 UserOperation 和 EntryPoint 两个核心组件。

![图 1: ERC-4337 架构](../diagrams/build/erc4337-architecture.svg)

图 1: ERC-4337 架构。展示核心组件及其关系。
```

## Outputs

- diagrams/models/<diagram-id>-model.yaml
- diagrams/source/<diagram-id>.puml
- diagrams/build/<diagram-id>.svg
- diagrams/reviews/<diagram-id>-review.md

## Done Criteria

- [ ] Diagram model 已创建
- [ ] PlantUML source 已编写
- [ ] 渲染成功
- [ ] 验证通过
- [ ] Review 完成
- [ ] 简化已标注（如适用）

## Failure Handling

### PlantUML 渲染失败

**处理**：
1. 检查语法
2. 简化复杂结构
3. 使用在线渲染器验证

### 验证不通过

**处理**：
1. 修复命名问题
2. 修正关系语义
3. 重新验证

### Review 发现问题

**处理**：
1. 记录问题
2. 修复 High 严重性
3. 酌情修复 Medium/Low
