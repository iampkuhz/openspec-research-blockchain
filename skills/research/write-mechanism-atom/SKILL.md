# Skill: Write Mechanism Atom

## Purpose

编写机制分析原子，包括：
- 先做实体分类
- 先决定必要图表集合
- 再写设计动机、核心流程、状态转换、关键决策和边界情况

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
- 不要跳过实体分类表和图表清单表
- 不要把角色、组件、状态混在一张图里

## Files to Read

- `harness/workflows/principle-atom-workflow.md` - Atom 写作流程
- `harness/rules/research/atom-mechanism-rules.md` - 机制分析规则
- `harness/rules/diagrams/diagram-selection-matrix.md` - 图表选择矩阵
- `harness/rules/diagrams/component-abstraction-rules.md` - 角色/组件/状态边界
- `openspec/changes/<change-id>/sources/` - 来源

## Files to Write

### 1. Mechanism Atom

`openspec/changes/<change-id>/atoms/core-mechanism.md`

### 2. Claims

`openspec/changes/<change-id>/claims/facts.yaml` (新增或更新)

### 3. Diagram Model / Package（如适用）

- `openspec/changes/<change-id>/diagrams/models/<diagram-id>-model.yaml`
- 或正式 diagram package（若该 atom 的图会进入 draft）

## Execution Steps

1. **先做实体分类**
   - 把关键实体分成 `role / component / data object / state / external system`
   - 标明控制方、是否跨信任边界、应落入哪类图

2. **再做图表清单**
   - 明确每张图要回答的问题
   - 判断哪些图是必需、哪些可以省略
   - 若省略，必须写明原因

3. **按机制语义决定必要视图**
   - 有多角色或 trust assumption → 必须有角色与信任边界图
   - 需要解释单角色内部实现 → 必须有角色内部组件图
   - 依赖跨角色交互 → 必须有跨角色核心流程图
   - 依赖命名状态 / round / epoch / timeout / challenge → 必须有状态图或状态表

4. **生成图表**
   - Architecture / Sequence 类型遵守仓库 diagram policy
   - State 类型使用 Mermaid / Markdown 表格 / ASCII fallback
   - 同构角色优先复用 canonical 内部组件图，并补差异表

5. **撰写正文**
   - 图承担主干结构
   - 文字只补充设计原因、trade-off、边界情况和失败条件

6. **回写 claims 并自检**
   - 检查必要视图是否覆盖
   - 检查是否混用了角色、组件、状态

## Local Validation Steps

1. 检查是否有实体分类表
2. 检查是否有图表清单表
3. 检查设计动机是否解释
4. 检查核心流程是否完整
5. 检查关键决策是否有替代方案对比
6. 检查边界情况是否覆盖
7. 检查必要视图是否按条件补齐

## Output Contract

```yaml
atom_path: openspec/changes/<change-id>/atoms/core-mechanism.md
claims_count: <定义的 claims 数量>
entity_inventory: present|missing
diagram_inventory: present|missing
required_views:
  - role-boundary|internal-components|cross-role-flow|state-transition
diagrams: [<diagram IDs>]
status: draft|review-ready
```

## Quality Gate

- [ ] 有实体分类表
- [ ] 有图表清单表
- [ ] 设计动机清晰
- [ ] 关键设计有对比
- [ ] 边界情况覆盖
- [ ] 复杂度分析（如适用）
- [ ] 多角色机制有角色与信任边界图
- [ ] 需要内部结构时有角色内部组件图
- [ ] 跨角色机制有核心流程图
- [ ] 显式状态机制有状态图或状态表
- [ ] diagram 准确且未混用抽象层

## Failure Modes

### 机制细节在来源中不明确

**处理**：标注 evidence gap，记录不确定性。

### 流程图过于复杂

**处理**：分解为 happy path / failure path，多图表达。

### 抽象层混用

**处理**：重新做实体分类，再拆成角色图、组件图、状态图。

### 同构角色被重复作图

**处理**：保留 1 张 canonical 内部组件图，补差异表，删除重复图。

## When to Stop and Ask for Manual Triage

- 关键机制在来源中完全缺失
- 不同来源对机制描述严重冲突
- 机制范围过大无法在一个 atom 中覆盖
