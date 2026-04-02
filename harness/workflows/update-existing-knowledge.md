# Update Existing Knowledge Workflow - 更新现有知识

## Goal

安全地更新 knowledge/中的现有主题，确保一致性和向后兼容。

## Trigger

- 规范更新（EIP 版本升级）
- 发现错误需要修正
- 生态有重大变化
- 新的比较维度出现

## Required Inputs

- 现有 topic 路径
- 更新原因
- 新来源或新信息

## Optional Inputs

- 现有 topic 的依赖者列表
- 历史 changelog

## Rule Set to Load

- harness/rules/general/update-policy.md
- harness/rules/general/traceability-policy.md
- harness/rules/general/repo-governance.md

## Step-by-Step Procedure

### Step 1: 读取现有知识

```bash
# 读取 topic 结构
ls -la knowledge/topics/<topic>/

# 读取 changelog
cat knowledge/topics/<topic>/changelog.md

# 读取当前 atoms
cat knowledge/topics/<topic>/atoms/*.md
```

### Step 2: 评估更新范围

确定更新类型：

| 类型 | 描述 | 示例 |
|------|------|------|
| atom-update | 单个 atom 更新 | 补充 gas 计算细节 |
| topic-update | 整个 topic 更新 | 规范版本升级 |
| topic-refactor | 结构重构 | 拆分 atom |

确定影响范围：

```yaml
# update-scope.yaml
target:
  topic: eip-4337
  type: topic-update

atoms_to_update:
  - core-mechanism
  - limits-and-assumptions

atoms_to_review:
  - definition

dependencies_to_notify:
  - topic: aa-eip-evolution
    strength: strong
```

### Step 3: 创建 OpenSpec Change

**必须**创建 change，禁止直接修改 knowledge/。

```bash
openspec new change <name> --schema blockchain-research
```

命名：`update-<topic>-<reason>-pass-1`

示例：
- `update-eip-4337-spec-v07-pass-1`
- `update-eip-4337-gas-details-pass-1`

在 request.md 中说明：

```yaml
topic: eip-4337
type: update-topic

background: |
  EIP-4337 规范从 v0.6 更新到 v0.7，
  gas 计算方式有变化。

update_reason: |
  规范更新导致现有知识过时。

scope: |
  更新 core-mechanism 中的 gas 计算部分。
  更新 limits-and-assumptions 中的参数。

non-goals: |
  不改变整体结构。
  不重新研究已确认的内容。

breaking_changes: |
  gas 计算公式变化，影响成本分析。

dependencies: |
  aa-eip-evolution 可能需要更新。
```

### Step 4: 对比新旧内容

创建对比文档：

```markdown
# Content Comparison

## Atom: core-mechanism

### 当前内容（v1.0）

[当前内容摘要]

### 新内容（v1.1）

[新内容摘要]

### 主要变化

1. Gas 计算公式变化
   - 旧：`gas = A + B`
   - 新：`gas = A + B + C`

2. 新增参数
   - EIP-3860 相关的 initCode 成本

### 影响分析

- claim-020 需要更新
- 成本分析部分需要重写
- aa-eip-evolution 依赖此部分
```

### Step 5: 执行更新

更新 atoms：

```bash
# 备份当前内容
cp knowledge/topics/<topic>/atoms/core-mechanism.md \
   knowledge/topics/<topic>/atoms/core-mechanism.md.bak

# 更新内容
# 编辑文件
```

更新 claims：

```yaml
# claims/facts.yaml
# 更新受影响的 claims
- claim_id: claim-020
  statement: <新陈述>
  sources:
    - source_id: eip-4337-v07  # 新来源
  evidence_level: L1
  confidence: high
  superseded_by: claim-030  # 如有新 claim 替代

# 新增 claims
- claim_id: claim-030
  statement: <新陈述>
  sources:
    - source_id: eip-4337-v07
```

### Step 6: 更新 Changelog

```yaml
# knowledge/topics/<topic>/changelog.md
changelog:
  - version: "1.1"
    date: <date>
    change_id: <change-id>
    type: update-topic

    summary: "更新 EIP-4337 规范到 v0.7"

    changes:
      - atom: core-mechanism
        action: updated
        sections:
          - "Gas Calculation"
        summary: "更新 gas 计算公式，补充 EIP-3860 影响"

      - atom: limits-and-assumptions
        action: updated
        sections:
          - "Parameters"
        summary: "更新 initCode 成本参数"

    breaking_changes:
      - description: "Gas 计算公式变化"
        impact: "成本分析需要调整"
        migration: "使用新公式重新计算"

    deprecated_claims:
      - claim-020
      reason: "旧公式不再准确"

    new_claims:
      - claim-030
      - claim-031

    related_changes:
      - change_id: aa-eip-evolution-pass-2
        relationship: "consumes this update"
        status: pending
```

### Step 7: 处理向后兼容

**Breaking Changes 处理**：

1. 保留旧 claim 为 historical：
```yaml
- claim_id: claim-020
  status: historical
  superseded_by: claim-030
  historical_context: "适用于 EIP-4337 v0.6 及之前版本"
```

2. 在术语变更时保留 alias：
```yaml
term: UserOperation
aliases:
  - UserOp
deprecated_aliases:
  - user-op  # v1.0 使用，v1.1 废弃
```

3. 通知依赖者：
```markdown
## 依赖此 Topic 的内容

以下内容依赖 eip-4337，可能需要更新：

- knowledge/analysis/synthesis/aa-eip-evolution
  - 依赖强度：strong
  - 依赖部分：core-mechanism
  - 建议动作：review gas 计算部分
```

### Step 8: 评审

执行 review workflow：

```bash
# 对于 update，至少需要：
# - 技术准确性评审
# - 向后兼容性评审
```

### Step 9: Merge

执行 merge workflow。

## Outputs

- 更新的 knowledge/topics/<topic>/
- 更新的 changelog.md
- Git commit

## Done Criteria

- [ ] 所有目标 atoms 已更新
- [ ] claims 已更新
- [ ] changelog 已更新
- [ ] breaking changes 已记录
- [ ] 依赖者已通知
- [ ] 评审通过
- [ ] Merge 完成

## Failure Handling

### 更新导致重大破坏

**处理**：
1. 回滚到备份
2. 重新评估更新范围
3. 考虑创建新 topic 而非更新

### 依赖者强烈反对

**处理**：
1. 记录反对意见
2. 评估是否继续
3. 可能考虑版本并存
