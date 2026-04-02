# Comparison Workflow - 比较分析

## Goal

编写比较分析 note，对比多个对象的差异。

## Trigger

- 需要对比多个 primitive/synthesis
- request.md 中指定 comparison 类型

## Required Inputs

- 比较对象列表
- 比较目的
- 目标读者/场景

## Optional Inputs

- 现有比较分析
- 决策标准

## Rule Set to Load

- harness/rules/research/comparison-rules.md
- harness/rules/writing/table-rules.md
- harness/rules/writing/summary-rules.md

## Step-by-Step Procedure

### Step 1: 确定比较对象

```yaml
# 在 request.md 或独立的 comparison-plan.yaml 中
comparison:
  objects:
    - topic: tendermint
      scope: consensus-mechanism
    - topic: qbft
      scope: consensus-mechanism
    - topic: simplex
      scope: consensus-mechanism

  purpose: <比较目的>
  audience: <目标读者>
  decision_context: <决策场景>
```

### Step 2: 确定比较维度

选择 3-5 个核心维度：

| 维度类型 | 示例 |
|----------|------|
| 技术机制 | 共识算法、数据流 |
| 性能 | 延迟、吞吐量 |
| 安全性 | 安全假设、攻击成本 |
| 成熟度 | 实现数、部署案例 |
| 生态 | 工具、文档、社区 |

### Step 3: 收集各对象数据

为每个对象读取：
- atoms/core-mechanism.md
- atoms/limits-and-assumptions.md
- claims/facts.yaml

### Step 4: 创建对比表格

```markdown
**表 1**: [维度名称] 对比

| 维度 | 对象 A | 对象 B | 对象 C |
|------|--------|--------|--------|
| 子维度 1 | ... | ... | ... |
| 子维度 2 | ... | ... | ... |
```

### Step 5: 编写比较正文

```markdown
# [比较主题]

## 概述

[比较对象、目的、维度]

## 维度 1: [名称]

[为什么选择这个维度]

| 对象 | A | B | C |
|------|---|---|---|
| 描述 | ... | ... | ... |
| 优势 | ... | ... | ... |
| 劣势 | ... | ... | ... |

[分析说明]

## 维度 2: [名称]

...

## 综合对比

[跨维度综合]

## 适用场景

| 场景 | 推荐 | 理由 |
|------|------|------|
| ... | ... | ... |

## 不适用场景

[各方案局限性]

## 证据等级

| 主张 | 来源 | 等级 |
|------|------|------|
| ... | ... | ... |
```

### Step 6: 创建 Matrix（可选）

```yaml
# comparisons/matrix.yaml
version: "1.0"

dimensions:
  - name: latency
    weights: 0.3
    scores:
      tendermint: 3
      qbft: 3
      simplex: 4
      malachite: 5

  - name: maturity
    weights: 0.4
    scores:
      tendermint: 5
      qbft: 4
      simplex: 2
      malachite: 1

summary:
  weighted_scores:
    tendermint: 4.1
    qbft: 3.7
    simplex: 2.8
    malachite: 2.4
```

### Step 7: 标注证据等级

为每个比较主张标注证据：

```markdown
Tendermint 延迟约 1s [L2 - Cosmos benchmarks]。

Malachite 吞吐量 10000 TPS [L3 - 官方博客，需验证]。
```

### Step 8: 自审

检查：
- [ ] 维度是否固定
- [ ] 是否有证据支撑
- [ ] 是否区分事实和观点
- [ ] 是否有适用场景
- [ ] 是否有不适用场景

## Outputs

- comparison-note.md
- comparisons/matrix.yaml（可选）

## Done Criteria

- [ ] 比较维度明确
- [ ] 数据已填充
- [ ] 证据已标注
- [ ] 场景分析完成
- [ ] 自审通过

## Failure Handling

### 数据不足

**处理**：
1. 标注数据缺口
2. 降低结论强度
3. 列为待确认

### 对象不可比

**处理**：
1. 重新定义比较范围
2. 分组比较
3. 说明不可比原因
