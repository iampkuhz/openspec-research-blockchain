---
name: write-synthesis-draft
description: 编写横向比较笔记，对比多个 primitive/synthesis 的差异与演进。
---

# Skill: Write Comparison Note

## Purpose

编写比较分析 note，对比多个对象在固定维度上的差异。

## Triggers

用户请求：
- "比较 A 和 B"
- "写对比分析"
- "完成 comparison note"

## Required Inputs

- **objects**: 比较对象列表
- **dimensions**: 比较维度
- **purpose**: 比较目的
- **sources**: 各方来源

## Forbidden Inputs / Anti-patterns

- 不要随意切换维度
- 不要主观判断无证据支持
- 不要混用不同抽象层的对象
- 不要缺少适用场景分析

## Files to Read

- `harness/workflows/comparison-workflow.md` - 比较分析流程
- `harness/rules/research/note-comparison-rules.md` - 比较分析规则
- `harness/rules/writing/table-rules.md` - 表格规则
- 各比较对象的 atoms

## Files to Write

### 1. Comparison Note

`openspec/changes/<change-id>/comparison-note.md`

### 2. Comparison Matrix

`openspec/changes/<change-id>/comparisons/matrix.yaml`

### 3. Claims

`openspec/changes/<change-id>/claims/facts.yaml` (比较相关 claims)

## Local Validation Steps

1. 检查维度是否固定
2. 检查每个主张都有证据
3. 检查适用场景分析
4. 检查不适用场景分析

## Output Contract

```yaml
note_path: openspec/changes/<change-id>/comparison-note.md
matrix_path: openspec/changes/<change-id>/comparisons/matrix.yaml
dimensions: <维度列表>
objects: <对象列表>
status: draft|review-ready
```

## Quality Gate

- [ ] 比较目的明确
- [ ] 维度固定且相关
- [ ] 数据有证据支撑
- [ ] 适用场景清晰
- [ ] 不适用场景列出
- [ ] 证据等级标注

## Failure Modes

### 对象不可比

**处理**：说明不可比原因，或重新定义比较范围。

### 某对象数据不足

**处理**：标注证据缺口，降低相关结论置信度。

### 维度选择不当

**处理**：重新选择与比较目的相关的维度。

## When to Stop and Ask for Manual Triage

- 比较对象完全不属于同一范畴
- 关键比较维度数据全部缺失
- 比较目的不清晰
