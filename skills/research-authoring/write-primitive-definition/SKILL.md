---
name: write-primitive-definition
description: 编写定义型 primitive 笔记，聚焦概念定义与边界。
---

# Skill: Write Definition Atom

## Purpose

基于来源编写定义原子，包括形式化定义、关键术语、边界条件。

## Triggers

用户请求：
- "写定义"
- "定义 <topic>"
- "完成 definition atom"

## Required Inputs

- **topic**: 主题名称
- **sources**: source-pack.yaml 或来源列表
- **claims**: 相关 claims（可选，如已有）

## Forbidden Inputs / Anti-patterns

- 不要在没有 L1/L2 来源的情况下写定义
- 不要混入机制细节（属于 mechanism atom）
- 不要使用模糊或非正式术语

## Files to Read

- `harness/workflows/principle-atom-workflow.md` - Atom 写作流程
- `harness/rules/research/atom-definition-rules.md` - 定义写作规则
- `harness/rules/general/terminology-policy.md` - 术语政策
- `openspec/changes/<change-id>/sources/source-pack.yaml` - 来源包

## Files to Write

### 1. Definition Atom

`openspec/changes/<change-id>/atoms/definition.md`

### 2. Claims

`openspec/changes/<change-id>/claims/facts.yaml`

### 3. Terms

`openspec/changes/<change-id>/terms/terms.yaml`

## Local Validation Steps

1. 检查定义是否简洁（1-2 句核心）
2. 检查关键术语是否覆盖
3. 检查边界条件是否清晰
4. 检查所有 claims 都有 sources

## Output Contract

```yaml
atom_path: openspec/changes/<change-id>/atoms/definition.md
claims_count: <定义的 claims 数量>
terms_count: <定义的术语数量>
status: draft|review-ready
```

## Quality Gate

- [ ] 定义简洁准确
- [ ] 形式化描述正确（如适用）
- [ ] 关键术语 3-7 个
- [ ] 边界条件清晰
- [ ] 前提条件列出
- [ ] 相关概念区分

## Failure Modes

### 来源不足以下定义

**处理**：标注 evidence gap，降低置信度。

### 术语定义冲突

**处理**：检查 glossary，记录冲突和解决方式。

### 定义过于复杂

**处理**：拆分为 definition + prerequisites。

## When to Stop and Ask for Manual Triage

- 核心来源缺失导致定义无法完成
- 术语冲突无法解决
- 定义范围无法确定
