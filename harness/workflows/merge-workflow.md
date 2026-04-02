# Merge Workflow - 合并到知识库

## Goal

将通过评审的 change 产物合并到 knowledge/主线。

## Trigger

- Review workflow 完成
- 评审结论为 approved 或 approved with minor fixes
- 所有 high severity 问题已修复

## Required Inputs

- openspec/changes/<change-id>/ 完整内容
- review/review-summary.md（结论为 approved）

## Optional Inputs

- 现有 knowledge/中的相关 topic
- 依赖的 topics 更新

## Rule Set to Load

- harness/rules/general/repo-governance.md
- harness/rules/general/update-policy.md
- harness/rules/general/traceability-policy.md

## Step-by-Step Procedure

### Step 1: 确认 Merge 条件

检查：
```yaml
# merge-checklist.yaml
prerequisites:
  - item: review 结论为 approved
    status: pass|fail

  - item: 所有 high 问题已修复
    status: pass|fail

  - item: sources 完整
    status: pass|fail

  - item: claims 有 sources 支撑
    status: pass|fail

  - item: 术语一致
    status: pass|fail
```

### Step 2: 确定 Merge 类型

| 类型 | 描述 | 处理 |
|------|------|------|
| new-topic | 新主题 | 创建完整 topic 目录 |
| update-topic | 更新现有 | 合并变更内容 |
| refactor-topic | 重构 | 重组目录结构 |

### Step 3: New-Topic Merge

创建 topic 目录结构：

```bash
# 创建目录
mkdir -p knowledge/topics/<domain>/<topic>/{atoms,claims,comparisons,diagrams,reviews,sources,terms}

# 复制 atoms
cp openspec/changes/<change-id>/draft.md knowledge/topics/<domain>/<topic>/overview.md
cp atoms/*.md knowledge/topics/<domain>/<topic>/atoms/

# 复制 claims
cp claims/*.yaml knowledge/topics/<domain>/<topic>/claims/

# 复制 sources
cp sources/source-pack.yaml knowledge/topics/<domain>/<topic>/sources/
cp sources/excerpts/* knowledge/topics/<domain>/<topic>/sources/excerpts/

# 复制 diagrams（如有）
cp diagrams/build/* knowledge/topics/<domain>/<topic>/diagrams/build/
cp diagrams/source/* knowledge/topics/<domain>/<topic>/diagrams/source/
cp diagrams/reviews/* knowledge/topics/<domain>/<topic>/diagrams/reviews/
```

创建 changelog：

```yaml
# knowledge/topics/<domain>/<topic>/changelog.md
changelog:
  - version: "1.0"
    date: <date>
    change_id: <change-id>
    type: new-topic

    summary: "<change 摘要>"

    atoms_created:
      - overview
      - definition
      - core-mechanism

    claims_count: <数量>
    diagrams_count: <数量>

    merged_at: <date>
    merge_commit: <commit hash>
```

### Step 4: Update-Topic Merge

更新现有 topic：

```bash
# 对比现有内容
diff knowledge/topics/<topic>/atoms/core-mechanism.md \
     openspec/changes/<change-id>/atoms/core-mechanism.md

# 合并变更
# 使用 git merge 或手动合并
```

更新 changelog：

```yaml
# knowledge/topics/<topic>/changelog.md
changelog:
  - version: "1.1"
    date: <date>
    change_id: <change-id>
    type: update-topic

    summary: "<更新摘要>"

    changes:
      - atom: core-mechanism
        action: updated
        sections:
          - "Gas Calculation"
        summary: "补充 EIP-3860 影响"

      - atom: definition
        action: updated
        sections:
          - "Key Terms"
        summary: "更新术语定义"

    new_claims:
      - claim-025
      - claim-026

    deprecated_claims:
      - claim-020
      reason: "旧数据不再准确"
```

### Step 5: 更新 Indexes

更新 topic 索引：

```markdown
# knowledge/indexes/topic-index.md

## Topics

| Topic | Domain | Type | Last Updated | Change ID |
|-------|--------|------|--------------|-----------|
| eip-4337 | account-abstraction | primitive | 2024-01-15 | primitive-eip-4337-deep-dive-pass-1 |
```

更新 diagram 索引（如有）：

```markdown
# knowledge/indexes/diagram-index.md

## Diagrams

| ID | Topic | Type | Description |
|----|-------|------|-------------|
| erc4337-arch | eip-4337 | component | ERC-4337 架构 |
```

### Step 6: 更新依赖此 Topic 的内容

检查是否有 topics 依赖此 topic：

```bash
# 查找依赖
grep -r "eip-4337" knowledge/topics/*/dependencies.md
```

如有依赖，通知相关 topic 维护者或触发 refresh。

### Step 7: 提交 Commit

```bash
git add knowledge/topics/<topic>/
git commit -m "Merge <change-id>: <summary>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
"
```

### Step 4: Archive Change（可选）

将完成的 change 移到 archive：

```bash
mv openspec/changes/<change-id>/ openspec/archive/
```

或在 changes/README.md 中标记为 completed。

## Outputs

- knowledge/topics/<topic>/ 更新或创建
- knowledge/indexes/ 更新
- Git commit

## Done Criteria

- [ ] 所有产物已复制
- [ ] changelog 已更新
- [ ] indexes 已更新
- [ ] Commit 已创建
- [ ] Change 已归档

## Failure Handling

### Merge 冲突

**处理**：
1. 手动解决冲突
2. 确保不丢失内容
3. 记录冲突原因

### 评审后又有新来源

**处理**：
1. 如 minor，记录到 changelog
2. 如 major，创建新的 change

### 发现遗漏内容

**处理**：
1. 记录遗漏
2. 创建 follow-up change
