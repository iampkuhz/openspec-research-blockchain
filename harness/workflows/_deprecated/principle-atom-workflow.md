# Principle Note Workflow - 知识笔记写作

## 目标

基于来源编写知识笔记（definition / mechanism / evolution / comparison），作为 `draft.md` 的组成部分。

## 触发条件

- source workflow 完成后
- 已有 `source-pack.yaml` 和 `excerpts`
- `plan.md` 已填写

## 必需输入

- `source-pack.yaml`
- `sources/excerpts/*`
- `plan.md`

## 规则加载策略

### 初始加载（workflow 开始时）

根据笔记类型加载核心规则：

| 笔记类型 | 核心规则 | 路径 |
|----------|----------|------|
| definition | `atom-definition-rules.md` | `harness/rules/research/` |
| mechanism | `atom-mechanism-rules.md` | `harness/rules/research/` |
| evolution | `atom-evolution-rules.md` | `harness/rules/research/` |
| comparison | `note-comparison-rules.md` | `harness/rules/research/` |

### 按需加载（执行到对应步骤前）

| 步骤 | 规则 | 路径 |
|------|------|------|
| 所有类型 | `structure-rules.md` | `harness/rules/writing/` |
| mechanism/comparison | `table-rules.md` | `harness/rules/writing/` |
| comparison | `summary-rules.md` | `harness/rules/writing/` |
| 步骤 7（自审） | 重新读取核心规则 | 对照检查清单 |

**注意**：规则文件在对话中可能被压缩，**自审前必须重新读取**核心规则。

## 步骤

### 步骤 1：创建笔记结构

在 `openspec/changes/<change-id>/` 中创建：

```
openspec/changes/<change-id>/
├── notes/                # 知识笔记
│   ├── definition.md
│   ├── mechanism.md
│   └── evolution.md
└── comparisons/          # 比较分析（如适用）
```

### 步骤 2：编写 Definition Note

按照 `atom-definition-rules.md` 编写：

```markdown
# 定义

[1-2 句简洁定义]

## 形式化描述

[伪代码/接口定义]

## 关键术语

| 术语 | 定义 |
|------|------|
| 术语 1 | 定义 |
| 术语 2 | 定义 |

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

### 步骤 3：编写 Mechanism Note

按照 `atom-mechanism-rules.md` 编写：

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

### 步骤 4：编写 Evolution Note

按照 `atom-evolution-rules.md` 编写：

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

### 步骤 5：编写 Comparison Note

按照 `note-comparison-rules.md` 编写：

```markdown
# 比较分析

## 比较对象

[列出比较的对象]

## 比较维度

| 维度 | 对象 A | 对象 B |
|------|--------|--------|
| 维度 1 | ... | ... |
| 维度 2 | ... | ... |

## 分析

[逐项分析]

## 总结

[高层判断]
```

### 步骤 6：关联来源

在笔记中引用来源：

```markdown
UserOperation 是基本单位 [L1: EIP-4337]。

处理流程包括验证和执行 [L2: reference-impl]。
```

### 步骤 7：自审

检查：
- [ ] 所有 `claim` 都有 `source` 支撑
- [ ] 证据等级适当
- [ ] 术语一致性
- [ ] 边界清晰
- [ ] 符合 rules

## 输出

- `notes/*.md`
- `comparisons/*.md`

## 完成标准

- [ ] 所有必要笔记已编写
- [ ] 来源关联完整
- [ ] 自审通过

## 下一步

→ 由主会话 orchestrator 整合笔记到 `draft.md`

## 异常处理

### 证据不足

**处理**：
1. 降低结论置信度
2. 标注 `evidence-gap`
3. 列入 `draft.md` 的 open questions

### 来源冲突

**处理**：
1. 优先 L1/L2
2. 记录冲突
3. 标注不确定性

### 术语不一致

**处理**：
1. 检查 `harness/rules/general/terminology-policy.md` 与 `GLOBAL-GLOSSARY.md`
2. 统一定义
3. 记录术语决策
