# Comparison Workflow - 比较分析

## 目标

编写比较分析笔记，对比多个研究对象的差异。

## 触发条件

- 需要对比多个 primitive/synthesis
- request.md 中指定 comparison 需求

## 必需输入

- 比较对象列表
- 比较目的
- 目标读者/场景

## 规则加载策略

### 初始加载（workflow 开始时）

- `harness/rules/research/note-comparison-rules.md` — 比较分析的整体框架和质量标准

### 按需加载（执行到对应步骤前）

| 步骤 | 规则 | 用途 |
|------|------|------|
| 步骤 4 | `harness/rules/writing/table-rules.md` | 创建对比表格 |
| 步骤 5 | `harness/rules/writing/summary-rules.md` | 编写摘要和分析 |
| 步骤 7（自审） | `harness/rules/research/note-comparison-rules.md` | 重新读取，对照检查清单 |

**注意**：规则文件在对话中可能被压缩，**自审前必须重新读取**核心规则。

## 步骤

### 步骤 1：确定比较对象

在 `request.md` 或 `plan.md` 中声明：

```yaml
comparison:
  objects:
    - topic: tendermint
      scope: consensus-mechanism
    - topic: qbft
      scope: consensus-mechanism

  purpose: <比较目的>
  audience: <目标读者>
  decision_context: <决策场景>
```

### 步骤 2：确定比较维度

选择 3-5 个核心维度：

| 维度类型 | 示例 |
|----------|------|
| 技术机制 | 共识算法、数据流 |
| 性能 | 延迟、吞吐量 |
| 安全性 | 安全假设、攻击成本 |
| 成熟度 | 实现数、部署案例 |
| 生态 | 工具、文档、社区 |

### 步骤 3：收集各对象数据

为每个对象读取 `knowledge/analysis/` 中的 `artifact.md`：

```bash
cat knowledge/analysis/primitives/<domain>/<topic>/artifact.md
```

### 步骤 4：创建对比表格

```markdown
**表 1**: [维度名称] 对比

| 维度 | 对象 A | 对象 B | 对象 C |
|------|--------|--------|--------|
| 子维度 1 | ... | ... | ... |
| 子维度 2 | ... | ... | ... |
```

### 步骤 5：编写比较正文

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

## 综合对比

[跨维度综合分析]

## 适用场景

| 场景 | 推荐 | 理由 |
|------|------|------|
| ... | ... | ... |

## 证据等级

| 主张 | 来源 | 等级 |
|------|------|------|
| ... | ... | ... |
```

### 步骤 6：标注证据等级

为每个比较主张标注证据：

```markdown
Tendermint 延迟约 1s [L2 - Cosmos benchmarks]。

Malachite 吞吐量 10000 TPS [L3 - 官方博客，需验证]。
```

### 步骤 7：自审

检查：
- [ ] 维度是否固定
- [ ] 是否有 `evidence` 支撑
- [ ] 是否区分事实和观点
- [ ] 是否有适用场景
- [ ] 是否有不适用场景

## 输出

- 比较分析内容写入 `draft.md` 的比较章节
- 或独立的比较笔记文件

## 完成标准

- [ ] 比较维度明确
- [ ] 数据已填充
- [ ] 证据已标注
- [ ] 场景分析完成
- [ ] 自审通过

## 异常处理

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
