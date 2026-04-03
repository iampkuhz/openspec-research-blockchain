# Update Existing Knowledge Workflow - 更新现有知识

## Goal

安全地更新 `knowledge/` 中的现有研究，确保一致性和向后兼容。

## Trigger

- 规范更新（EIP 版本升级）
- 发现错误需要修正
- 生态有重大变化

## Required Inputs

- 现有研究路径
- 更新原因
- 新来源或新信息

## Rule Set to Load

- harness/rules/general/update-policy.md
- harness/rules/general/traceability-policy.md
- harness/rules/general/repo-governance.md

## Step-by-Step Procedure

### Step 1: 读取现有知识

```bash
# 读取现有 artifact.md
cat knowledge/analysis/<path>/<topic>/artifact.md
```

### Step 2: 评估更新范围

确定更新类型：

| 类型 | 描述 | 示例 |
|------|------|------|
| `minor-update` | 小幅更新 | 补充细节、修正错误 |
| `major-update` | 大幅更新 | 规范版本升级、核心机制变化 |
| `refactor` | 重构 | 结构调整、内容重组 |

### Step 3: 创建 OpenSpec Change

**必须**创建 change，禁止直接修改 `knowledge/`。

```bash
openspec new change <name> --schema blockchain-research
```

命名：`update-<topic>-<reason>-pass-1`

示例：
- `update-eip-4337-spec-v07-pass-1`
- `update-eip-7702-scope-expansion-pass-1`

### Step 4: 对比新旧内容

在 `openspec/changes/<change-id>/` 中创建对比文档：

```markdown
# Content Comparison

## 主要变化

1. [变化 1]
2. [变化 2]

## 影响分析

- 哪些部分需要更新
- 是否影响依赖者
```

### Step 5: 执行更新

在 change 目录中更新 `draft.md`，反映新内容。

### Step 6: 处理向后兼容

**Breaking Changes 处理**：

1. 在 `draft.md` 中明确标注变化
2. 保留旧内容为 historical context（如需要）
3. 记录影响范围

### Step 7: 评审

执行 `review-workflow.md`。

### Step 8: Apply

通过 OpenSpec apply 流程提升到 `knowledge/`。

## Outputs

- `openspec/changes/<change-id>/` 完整内容
- 评审记录
- Git commit

## Done Criteria

- [ ] 更新内容已记录
- [ ] breaking changes 已标注
- [ ] 评审通过
- [ ] Apply 完成

## Failure Handling

### 更新导致重大破坏

**处理**：
1. 回滚
2. 重新评估更新范围
3. 考虑版本并存

### 依赖者反对

**处理**：
1. 记录反对意见
2. 评估是否继续
3. 可能考虑版本并存
