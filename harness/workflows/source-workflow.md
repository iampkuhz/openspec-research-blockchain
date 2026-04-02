# Source Workflow - 来源处理

## Goal

获取、验证、归档研究来源，提取关键信息。

## Trigger

- Intake workflow 完成后
- request.md 已填写

## Required Inputs

- request.md 中的研究范围
- plan.md 中的来源规划

## Optional Inputs

- 用户提供的来源列表
- 已有来源包

## Rule Set to Load

- harness/rules/general/evidence-policy.md
- harness/rules/general/traceability-policy.md
- harness/rules/research/source-validation-rules.md
- harness/rules/research/uncertainty-rules.md

## Step-by-Step Procedure

### Step 1: 创建 Sources 目录结构

```
openspec/changes/<change-id>/sources/
├── inbox.yaml         # 原始来源入口
├── fetched/           # 抓取的来源
├── excerpts/          # 来源摘录
└── source-review.md   # 来源评审
```

### Step 2: 收集来源

根据 plan.md 的来源规划，收集：

#### L1 来源
- [ ] EIP / RFC / 标准文档
- [ ] 白皮书
- [ ] 官方规范

#### L2 来源
- [ ] 参考实现代码
- [ ] SDK / API 文档
- [ ] 官方开发者文档

#### L3 来源
- [ ] 官方博客
- [ ] Release notes
- [ ] Roadmap

#### L4 来源
- [ ] 第三方分析
- [ ] 技术博客
- [ ] 社区讨论

### Step 3: 记录来源到 inbox.yaml

```yaml
version: "1.0"
change_id: <change-id>
created_at: <date>

sources:
  - source_id: <unique-id>
    title: <标题>
    url: <链接>
    type: standard|implementation|blog|discussion
    tier: L1|L2|L3|L4
    status: pending|read|verified
    priority: high|medium|low
    relevant_sections:
      - <章节/内容描述>
    notes: <说明>
```

### Step 4: 获取来源内容

**对于在线来源**：
1. 访问 URL
2. 抓取内容
3. 归档（PDF/截图/文本）
4. 保存到 fetched/

**归档元数据**：
```yaml
archive:
  original_url: https://...
  archived_at: <date>
  archive_type: pdf|screenshot|text
  archive_path: sources/fetched/<filename>
```

### Step 5: 提取关键信息

为每个核心来源创建 excerpt：

```markdown
# Excerpt: <source_id>-<section>

**Source**: <title>
**Source ID**: <source_id>
**URL**: <url>
**Location**: <文档中的位置>
**Extracted At**: <date>

## Content

> [引用原文]

## Relevance

[为什么这个来源重要，支持哪些 claims]

## Related Atoms

- definition
- core-mechanism
```

### Step 6: 验证来源

**验证维度**：

| 维度 | 检查项 |
|------|--------|
| 权威性 | 是否官方发布 |
| 时效性 | 是否最新 |
| 完整性 | 是否覆盖所需 |
| 一致性 | 与其他来源是否一致 |

**验证记录**：
```yaml
validation:
  source_id: <source_id>
  validated_at: <date>
  authority: high|medium|low
  timeliness: current|outdated|historical
  consistency: consistent|conflicts_with_X
  notes: <说明>
```

### Step 7: 处理来源冲突

如发现冲突：

1. 记录冲突：
```yaml
conflict_id: CONF-SRC-001
sources:
  - source_a: <说法 A>
  - source_b: <说法 B>
discrepancy: <差异描述>
resolution: <解决方式>
```

2. 解决优先级：L1 > L2 > L3 > L4

3. 在 source-review.md 中记录

### Step 8: 创建 Source Pack

```yaml
# sources/source-pack.yaml
version: "1.0"
topic: <topic>
generated_at: <date>

sources:
  - source_id: <unique-id>
    title: <标题>
    url: <链接或本地引用>
    source_type: standard|implementation|blog|discussion
    source_tier: L1|L2|L3|L4
    accessed_at: <日期>
    relevant_atoms:
      - definition
      - core-mechanism
    supported_claims:
      - claim-001
      - claim-002
    confidence: high|medium|low
    notes: <可选说明>
```

### Step 9: 编写 Source Review

```markdown
# Source Review

## 来源概览

| 类型 | 数量 |
|------|------|
| L1 | X |
| L2 | X |
| L3 | X |
| L4 | X |

## 核心来源

[列出最关键的 3-5 个来源]

## 证据缺口

[哪些重要内容缺乏来源支持]

## 来源冲突

[是否有冲突，如何解决]

## 待确认问题

[需要进一步验证的内容]
```

## Outputs

- sources/inbox.yaml
- sources/fetched/*
- sources/excerpts/*
- sources/source-pack.yaml
- sources/source-review.md

## Done Criteria

- [ ] 所有计划的来源已收集
- [ ] 来源已归档
- [ ] 关键 excerpts 已提取
- [ ] 来源冲突已记录
- [ ] 证据缺口已识别

## Failure Handling

### 关键来源无法访问

**处理**：
1. 尝试替代来源
2. 记录证据缺口
3. 在 uncertainty 中标注

### 来源之间存在重大冲突

**处理**：
1. 优先采用 L1/L2
2. 记录冲突
3. 降低相关结论置信度

### 只有 L3/L4 来源

**处理**：
1. 降低结论强度
2. 明确标注证据等级
3. 列为待验证
