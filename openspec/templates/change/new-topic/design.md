# Design：<Change 标题>

## 概述

[设计方案概述]

## 研究问题

### Q1: \<问题\>

**动机**: [为什么问这个问题]

**期望回答类型**: definition/mechanism/comparison/evaluation

### Q2: \<问题\>

...

## 来源计划

### L1 来源

| 来源 | 类型 | 状态 |
|------|------|------|
| EIP-XXX | standard | pending/read/verified |
| Whitepaper | standard | pending/read/verified |

### L2 来源

| 来源 | 类型 | 状态 |
|------|------|------|
| Reference Repo | implementation | pending/read/verified |
| Docs | documentation | pending/read/verified |

### L3 来源（仅用于背景）

| 来源 | 类型 | 用途 |
|------|------|------|
| Blog | official-blog | background/motivation |

## 输出结构

```
knowledge/topics/<domain>/<topic>/
├── overview.md
├── atoms/
│   ├── definition.md
│   ├── prerequisites.md
│   ├── core-mechanism.md
│   ├── module-evolution.md
│   ├── limits-and-assumptions.md
│   └── open-questions.md
├── claims/
│   ├── facts.yaml
│   └── inferences.yaml
├── sources/
│   ├── source-pack.yaml
│   └── primary-notes.md
└── diagrams/（如有）
```

## 待提取的关键 Claims

- [ ] 关于 definition 的 claim
- [ ] 关于 mechanism 的 claim
- [ ] 关于 performance 的 claim

## 待创建的图表

| ID | 类型 | 用途 |
|----|------|------|
| arch-overview | component | 展示架构 |
| flow | sequence | 展示流程 |

## 术语计划

| 术语 | Category | Layer | Source |
|------|----------|-------|--------|
| Term 1 | protocol-entity | protocol | EIP-XXX |
| Term 2 | protocol-action | protocol | EIP-XXX |

## 待记录的证据缺口

- [ ] 关于 X 的 gap
- [ ] 关于 Y 的 gap

## 验证计划

- [ ] 自审 checklist
- [ ] 技术评审
- [ ] 可读性评审
