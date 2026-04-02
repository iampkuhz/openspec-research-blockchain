# Skill: Write Mechanism Atom

## Purpose

编写机制分析原子，包括设计动机、核心流程、关键决策、边界情况。

## Triggers

用户请求：
- "写机制分析"
- "解释 <mechanism> 如何工作"
- "完成 mechanism atom"

## Required Inputs

- **topic**: 主题名称
- **mechanism_name**: 机制名称
- **sources**: 相关来源
- **definition_atom**: 定义 atom（如已有）

## Forbidden Inputs / Anti-patterns

- 不要只描述"是什么"而不解释"为什么"
- 不要混入演进历史（属于 evolution atom）
- 不要忽略边界情况
- 不要混用不同抽象层

## Files to Read

- `harness/workflows/principle-atom-workflow.md` - Atom 写作流程
- `harness/rules/research/mechanism-rules.md` - 机制分析规则
- `harness/rules/diagrams/abstraction-boundaries.md` - 抽象边界规则
- `openspec/changes/<change-id>/sources/` - 来源

## Files to Write

### 1. Mechanism Atom

`openspec/changes/<change-id>/atoms/core-mechanism.md`

### 2. Claims

`openspec/changes/<change-id>/claims/facts.yaml` (新增或更新)

### 3. Diagram Model (如适用)

`openspec/changes/<change-id>/diagrams/models/<diagram-id>-model.yaml`

## Local Validation Steps

1. 检查设计动机是否解释
2. 检查核心流程是否完整
3. 检查关键决策是否有替代方案对比
4. 检查边界情况是否覆盖
5. 检查 diagram（如有）是否符合抽象边界

## Output Contract

```yaml
atom_path: openspec/changes/<change-id>/atoms/core-mechanism.md
claims_count: <定义的 claims 数量>
diagrams: [<diagram IDs>]
status: draft|review-ready
```

## Quality Gate

- [ ] 设计动机清晰
- [ ] 核心流程完整
- [ ] 关键决策有对比
- [ ] 边界情况覆盖
- [ ] 复杂度分析（如适用）
- [ ] diagram（如有）准确

## Failure Modes

### 机制细节在来源中不明确

**处理**：标注 evidence gap，记录不确定性。

### 流程图过于复杂

**处理**：分解为 overview + detail 多图。

### 抽象层混用

**处理**：重新组织，使用 stereotype 标注。

## When to Stop and Ask for Manual Triage

- 关键机制在来源中完全缺失
- 不同来源对机制描述严重冲突
- 机制范围过大无法在一个 atom 中覆盖
