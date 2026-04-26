---
name: write-primitive-evolution
description: 编写演进型 primitive 笔记，聚焦技术演进阶段与变化。
---

# Skill: Write Evolution Atom

## Purpose

编写演进分析原子，包括演进阶段、驱动因素、不变原则、分歧点。

## Triggers

用户请求：
- "写演进历史"
- "<topic> 是如何发展的"
- "完成 evolution atom"

## Required Inputs

- **topic**: 主题名称
- **time_range**: 时间范围（可选）
- **sources**: 相关来源，特别是历史文档

## Forbidden Inputs / Anti-patterns

- 不要跳跃式叙述（必须按时间线）
- 不要只描述"发生了什么"而不解释"为什么"
- 不要忽略未采用的方案
- 不要把不同变化类型混为一谈

## Files to Read

- `harness/workflows/principle-atom-workflow.md` - Atom 写作流程
- `harness/rules/research/atom-evolution-rules.md` - 演进分析规则
- `openspec/changes/<change-id>/sources/` - 来源

## Files to Write

### 1. Evolution Atom

`openspec/changes/<change-id>/atoms/module-evolution.md`

### 2. Claims

`openspec/changes/<change-id>/claims/facts.yaml` (新增时间线相关 claims)

### 3. Timeline (可选)

`openspec/changes/<change-id>/sources/timeline.yaml`

## Local Validation Steps

1. 检查时间线是否连续
2. 检查变化类型是否区分（breaking/additive/clarification）
3. 检查驱动因素是否说明
4. 检查关键分歧点是否记录

## Output Contract

```yaml
atom_path: openspec/changes/<change-id>/atoms/module-evolution.md
time_range: <时间范围>
stages: <阶段数量>
claims_count: <定义的 claims 数量>
status: draft|review-ready
```

## Quality Gate

- [ ] 时间线清晰
- [ ] 阶段划分合理
- [ ] 驱动因素说明
- [ ] 不变原则列出
- [ ] 关键分歧点记录
- [ ] 当前状态更新

## Failure Modes

### 历史信息不足

**处理**：标注证据缺口，仅记录可验证的事实。

### 时间线存在冲突

**处理**：记录多个来源的说法，优先 L1/L2。

### 演进范围过大

**处理**：按阶段拆分为多个 atoms 或 passes。

## When to Stop and Ask for Manual Triage

- 关键历史事件来源完全缺失
- 时间线冲突无法解决
- 演进范围无法合理界定
