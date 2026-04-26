# Primitive Quality Rules

## 适用场景

单个协议/机制/产品的底层研究，产出 `knowledge/analysis/primitives/**/artifact.md`。

## 质量要求

### 定义层

- 必须明确研究对象是什么、管什么、不管什么
- 必须区分角色（role）、组件（component）、数据对象（data object）、状态（state）、外部系统（external system）
- 必须写边界条件（包含什么、不包含什么）

### 机制层

- 必须描述核心机制如何工作
- 必须描述关键设计决策和为什么这样设计
- 必须描述边界情况和异常路径

### 能力边界

- 必须区分协议原生能力、角色职责、外部依赖和非目标
- 必须写失败条件和前提假设
- 不得把 promotional 能力写成 live

### 图表要求

- 必须先做实体分类，再决定图表集合
- 必须回答图表决策树的四个判定问题
- PlantUML 仅限 Architecture Diagram 和 Sequence Diagram，必须通过 skill 生成

## 旧 atom 规则迁移

以下内容已从旧的 atom-definition/evolution/mechanism rules 迁入本文件：
- 定义写作规范（原 atom-definition-rules.md）
- 机制分析规范（原 atom-mechanism-rules.md）
- 演进分析规范（原 atom-evolution-rules.md）

不再使用 "atom" 作为正式分类名称，统一使用 "primitive"。
