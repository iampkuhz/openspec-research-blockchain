# Draft 阶段规范

## 目的

定义本仓库 blockchain research change 中 `draft.md` artifact 的正式规则，包括：
- draft 在 research change 中的定位
- 进入 draft 阶段的前置条件
- draft 必须满足的形式要求
- draft 完成标准

## 适用范围

本规范适用于本仓库所有 research change 的 draft 阶段。

## draft.md 的定位

`draft.md` 是 research change 的第二轮集中 review artifact，负责：
- 合并关键术语、分析正文、有限结论为单一交付物
- 承载该 change 的核心图表（演进、架构、流程、对比）
- 作为从 plan 阶段迈向 synthesis 阶段的过渡交付物

## 进入 draft 阶段的前置条件

必须满足以下条件方可进入 draft 阶段：

1. **plan.md 已完成 review**
   - `plan.md` 已存在且通过 review

2. **来源规划足以支撑正文**
   - `evidence-matrix.md`（如有）已足以支撑第一轮分析

## draft 阶段的正式要求

### 结构要求

`draft.md` 必须包含以下章节（顺序固定）：

1. 概述
2. 术语表
3. 组件架构
4. 核心流程（如必要）
5. 设计取舍
6. 能力边界
7. 相关协议对比
8. 结论
9. 待确认问题
10. 参考资料

### 术语表要求

- 必须使用**表格形式**（三列：术语、定义、作用）
- 不得采用按词分标题的卡片式写法

### 图表要求

draft 阶段必须遵守：

- `openspec/specs/diagram-policy/spec.md`
- `openspec/specs/architecture-diagram-quality/spec.md`
- `openspec/specs/component-abstraction-level/spec.md`

**draft 阶段落点**：
- 必须包含核心图表：演进时间线图、组件架构图、核心流程图、能力归属表、对比表格
- 图表必须承载主干信息（演进脉络、架构关系、流程步骤）

### 内容要求

- 必须区分 live / planned / promotional
- 必须写边界、失败条件、前提条件
- 证据不足时必须明确写不确定性
- 结论只能是 bounded conclusions，不得写绝对化判断
- 先写机制，再写价值
- 必须回答"为什么这样设计，而不是那样设计"

### 风格要求

draft 阶段必须遵守：

- `openspec/specs/language-style/spec.md`
- `openspec/specs/evidence-policy/spec.md`

**draft 阶段落点**：
- 不确定性必须显式声明，不得脑补
- 不得把 promotional 能力写成 live

### 流程图步骤说明要求

- 必须使用**无序列表**，禁止使用有序列表（避免与图中序号错位）
- 必须使用 `【S1→S3】` 格式与图中序号关联
- 每个要点聚焦一个关键机制，而非罗列步骤

### PlantUML 要求

- PlantUML 图必须经过语法校验并通过后才可写入 draft

## draft 阶段完成标准

draft 阶段视为完成，当且仅当：

1. **结构完整**
   - 包含所有必须章节
   - 包含目录

2. **图表完备**
   - 包含所有核心图表类型
   - 所有 PlantUML 通过语法校验

3. **内容合规**
   - 遵守所有上位规范要求
   - 满足本规范"正式要求"所有条款

## 与上位规范的关系

本规范是以下规范的 draft 阶段特化：

| 上位规范 | 约束范围 |
|----------|----------|
| `openspec/schemas/blockchain-research/schema.yaml` | change 整体结构 |
| `openspec/specs/diagram-policy/spec.md` | 图表政策 |
| `openspec/specs/architecture-diagram-quality/spec.md` | 架构图质量 |
| `openspec/specs/component-abstraction-level/spec.md` | 组件抽象层级 |
| `openspec/specs/language-style/spec.md` | 语言风格 |
| `openspec/specs/evidence-policy/spec.md` | 证据政策 |
| `openspec/specs/canonical-output-model/spec.md` | 输出模型 |

本规范不重复上位规范的正文，仅定义：
- draft 阶段的入口条件
- draft 阶段的形式要求
- draft 阶段的完成标准

## 相关规范

- `openspec/schemas/blockchain-research/templates/draft.md` —— draft 模板
- `openspec/specs/diagram-policy/spec.md` —— 图表政策
- `openspec/specs/architecture-diagram-quality/spec.md` —— 架构图质量
- `openspec/specs/component-abstraction-level/spec.md` —— 组件抽象层级
- `openspec/specs/language-style/spec.md` —— 语言风格
- `openspec/specs/evidence-policy/spec.md` —— 证据政策
- `openspec/specs/canonical-output-model/spec.md` —— 输出模型
