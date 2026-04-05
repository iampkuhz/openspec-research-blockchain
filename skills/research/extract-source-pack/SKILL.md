# Skill: Extract Source Pack

## Purpose

从原始来源提取来源包，包括来源获取、验证、摘录和归档。

## Triggers

用户请求：
- "提取来源"
- "处理这些来源"
- "创建 source pack"

## Required Inputs

- **topic**: 主题名称
- **change_id**: OpenSpec change ID
- **source_urls**: 来源 URL 列表或来源描述

## Forbidden Inputs / Anti-patterns

- 不要仅保存 URL 而不获取内容
- 不要混用不同证据等级的来源
- 不要把 L3/L4 来源作为技术主张的唯一证据

## Files to Read

- `harness/workflows/source-workflow.md` - 来源处理流程
- `openspec/specs/evidence-policy/spec.md` - 证据政策
- `harness/rules/research/source-validation-rules.md` - 来源验证规则
- `openspec/changes/<change-id>/plan.md` - 来源规划

## Files to Write

### 1. Sources Inbox

`openspec/changes/<change-id>/sources/inbox.yaml`

### 2. Source Excerpts

`openspec/changes/<change-id>/sources/excerpts/<source-id>-<section>.md`

### 3. Source Pack

`openspec/changes/<change-id>/sources/source-pack.yaml`

### 4. Source Review

`openspec/changes/<change-id>/sources/source-review.md`

## Local Validation Steps

1. 检查每个来源都有 source_id
2. 检查来源 tier 标注正确
3. 检查 accessed_at 日期
4. 检查 supported_claims 关联

## Output Contract

```yaml
sources_count: <来源数量>
by_tier:
  L1: <数量>
  L2: <数量>
  L3: <数量>
  L4: <数量>
evidence_gaps: [<缺口列表>]
source_pack_path: openspec/changes/<change-id>/sources/source-pack.yaml
```

## Quality Gate

- [ ] 所有来源已获取内容（不仅 URL）
- [ ] 证据等级标注正确
- [ ] 关键来源已归档
- [ ] excerpts 已提取
- [ ] 来源冲突已记录

## Failure Modes

### 来源无法访问

**处理**：记录证据缺口，尝试替代来源。

### 来源之间存在冲突

**处理**：优先 L1/L2，记录冲突和解决方式。

### 只有 L3/L4 来源

**处理**：降低结论强度，明确标注证据缺口。

## When to Stop and Ask for Manual Triage

- 关键来源全部无法访问
- 来源冲突无法通过证据等级解决
- 用户提供的来源完全不相关
