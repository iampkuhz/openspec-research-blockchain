# Diagram Workflow - 图表创建

## Goal

创建 PlantUML 图表，辅助说明机制/架构/流程。

## Trigger

- 需要可视化机制/架构/流程
- `plan.md` 或 `draft.md` 需要图表支撑

## Required Inputs

- 研究主题/内容描述
- 图表用途说明

## Rule Set to Load

- harness/rules/diagrams/diagram-selection-matrix.md
- harness/rules/diagrams/abstraction-boundaries.md
- harness/rules/diagrams/relationship-rules.md
- harness/rules/diagrams/annotation-rules.md
- harness/rules/diagrams/simplification-policy.md

## Primary Skills（优先使用）

**架构图/组件图** → `feipi-gen-plantuml-arch-diagram`（全局 skill）
**时序图** → `feipi-gen-plantuml-sequence-diagram`（全局 skill）

这两个 skills 提供完整的 brief→PlantUML→校验流程。

## Step-by-Step Procedure

### Step 1: 确定图表类型

根据内容选择：

| 内容 | 推荐类型 | 使用 Skill |
|------|----------|------------|
| 系统架构/组件关系 | Architecture Diagram | `feipi-gen-plantuml-arch-diagram` |
| 交互流程/调用链路 | Sequence Diagram | `feipi-gen-plantuml-sequence-diagram` |
| 状态变化 | State Diagram | 手动创建 |
| 部署架构 | Deployment Diagram | 手动创建 |

### Step 2: 创建 Brief

**架构图**使用 `architecture-brief.yaml` 格式（由 user skill 定义）：
```yaml
title: <图标题>
summary: <系统摘要>
layers:
  - id: <layer-id>
    label: <显示名称>
    components:
      - id: <component-id>
        label: <显示名称>
        description: <组件说明>
flows:
  - id: <flow-id>
    from: <component-id>
    to: <component-id>
    description: <流程说明>
```

**时序图**使用 `sequence-brief.yaml` 格式（由 user skill 定义）：
```yaml
title: <图标题>
summary: <场景摘要>
participants:
  - id: <participant-id>
    label: <显示名称>
    type: actor|system|database
messages:
  - id: <message-id>
    from: <participant-id>
    to: <participant-id>
    description: <消息说明>
```

### Step 3: 调用 Skill 生成

**架构图**：
```
# 直接调用 skill（Claude Code 会自动识别）
使用 feipi-gen-plantuml-arch-diagram skill，传入 brief
```

**时序图**：
```
# 直接调用 skill（Claude Code 会自动识别）
使用 feipi-gen-plantuml-sequence-diagram skill，传入 brief
```

### Step 4: Skill 内部校验流程

用户级 skills 会自动执行：

1. **brief 校验** - `scripts/validate_brief.py`
2. **覆盖校验** - `scripts/check_coverage.py`（所有组件/参与者落图）
3. **布局校验** - `scripts/lint_layout.sh`
4. **渲染校验** - `scripts/check_render.sh`

**注意**：这些脚本由用户级 skill 管理，不在本仓库 `scripts/` 目录。

### Step 5: 手动创建图表（备选）

当图表类型不属于架构/时序图，或用户级 skill 不可用时：

1. 创建 PlantUML source
2. 使用 `scripts/check_plantuml.sh` 校验语法
3. 使用 `scripts/diagrams/render.sh` 渲染（如需要）

### Step 6: 集成到 draft.md

在 `draft.md` 中引用图：

```markdown
## 核心架构

![架构图标题](../diagrams/build/<diagram-id>.svg)

图 1: 架构说明
```

## Outputs

- brief.yaml（规范化后的）
- `.puml` 源码
- `.svg`（环境可用时）
- 校验摘要

## Done Criteria

- [ ] brief 已创建
- [ ] PlantUML source 已生成
- [ ] 语法校验通过
- [ ] 渲染完成（或明确标注未完成）

## Failure Handling

### 渲染失败

**处理**：
1. 检查 PlantUML 语法
2. 简化复杂结构
3. 检查渲染服务可用性

### Skill 不可用

**处理**：
1. 使用备选手动流程
2. 标注"未完成真实渲染校验"
