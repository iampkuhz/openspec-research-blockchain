# Principle Atom Workflow - 知识原子写作

## Goal

基于来源编写知识原子（definition / mechanism / evolution）。

## Trigger

- Source workflow 完成后
- 已有 source-pack.yaml 和 excerpts

## Required Inputs

- source-pack.yaml
- sources/excerpts/*
- request.md

## Optional Inputs

- 现有 knowledge/中的相关 atoms
- 依赖的 topics

## Rule Set to Load

根据 atom 类型加载：

| Atom 类型 | Rules |
|----------|-------|
| definition | definition-rules.md, structure-rules.md |
| mechanism | mechanism-rules.md, structure-rules.md, table-rules.md |
| evolution | evolution-rules.md, structure-rules.md |

## Step-by-Step Procedure

### Step 1: 创建 Atom 目录结构

```
knowledge/topics/<topic>/
├── atoms/
│   ├── definition.md
│   ├── prerequisites.md
│   ├── core-mechanism.md
│   ├── module-evolution.md
│   ├── limits-and-assumptions.md
│   └── open-questions.md
├── claims/
│   ├── facts.yaml
│   ├── inferences.yaml
│   └── estimates.yaml
└── terms/
    └── .gitkeep
```

### Step 2: 提取 Claims

从 excerpts 中提取 claims：

```yaml
# claims/facts.yaml
version: "1.0"
topic: <topic>

facts:
  - claim_id: claim-001
    statement: <事实陈述>
    sources:
      - source_id: <source>
        excerpt: <引用>
        location: <位置>
    evidence_level: L1|L2|L3|L4
    confidence: high|medium|low
    related_atoms:
      - definition
      - core-mechanism
    notes: <说明>
```

**Claim 分类**：
- **facts**: 事实性主张
- **inferences**: 推论
- **estimates**: 估算

### Step 3: 提取术语

从来源中提取关键术语：

```yaml
# terms/terms.yaml
terms:
  - term: UserOperation
    aliases:
      - UserOp
    category: protocol-entity
    layer: protocol
    definition: <简洁定义>
    source: <source_id>
```

### Step 4: 编写 Definition Atom

按照 definition-rules.md 编写：

```markdown
# 定义

[1-2 句简洁定义]

## 形式化描述

[伪代码/接口定义]

## 关键术语

**术语 1**
: 定义

**术语 2**
: 定义

## 边界条件

### 包含的内容
- ...

### 不包含的内容
- ...

## 前提条件

[前置知识]

## 相关概念

[区分相关概念]
```

### Step 5: 编写 Mechanism Atom

按照 mechanism-rules.md 编写：

```markdown
# 概述

[机制的核心作用]

## 设计动机

[为什么需要这个机制]

## 核心流程

### 流程概述

[高层描述]

### 详细步骤

[逐步详解]

## 关键设计决策

[为什么这样设计]

## 边界情况

[特殊情况处理]

## 复杂度分析

[时间/空间/Gas]
```

### Step 6: 编写 Evolution Atom

按照 evolution-rules.md 编写：

```markdown
# 演进概述

[时间范围、里程碑]

## 演进阶段

### 阶段 1: [名称]

- 时间范围
- 关键事件
- 主要变化
- 驱动因素

## 演进驱动因素

## 不变的原则

## 关键分歧点

## 当前状态
```

### Step 7: 关联 Claims

在 atoms 中引用 claims：

```markdown
UserOperation 是基本单位 [← claim-001]。

处理流程包括验证 [← claim-015] 和执行 [← claim-016]。
```

### Step 8: 创建术语表

```markdown
## 关键术语

**UserOperation** (category: protocol-entity, layer: protocol)
: EIP-4337 定义的用户操作原子。
  来源：[EIP-4337](url)

**EntryPoint** (category: protocol-entity, layer: protocol)
: 单例合约，处理 UserOperations。
  来源：[EIP-4337](url)
```

### Step 9: 自审

检查：
- [ ] 所有 claims 都有 sources
- [ ] 所有 atoms 都有 claims 支撑
- [ ] 术语一致性
- [ ] 边界清晰
- [ ] 符合 rules

## Outputs

- atoms/*.md
- claims/*.yaml
- terms/terms.yaml

## Done Criteria

- [ ] 所有 atoms 已编写
- [ ] claims 已提取并关联
- [ ] 术语已定义
- [ ] 自审通过

## Failure Handling

### 证据不足

**处理**：
1. 降低结论置信度
2. 标注 evidence gap
3. 列入 open-questions

### 来源冲突

**处理**：
1. 优先 L1/L2
2. 记录冲突
3. 标注不确定性

### 术语不一致

**处理**：
1. 检查 glossary
2. 统一定义
3. 记录术语决策
