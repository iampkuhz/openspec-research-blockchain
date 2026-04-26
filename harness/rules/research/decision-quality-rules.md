# Decision Quality Rules

## 适用场景

场景驱动的选型或决策分析，产出 `knowledge/decisions/**/artifact.md` + `knowledge/decisions/**/verdict.md`。

## 质量要求

### 场景定义

- 必须明确约束条件、优先级、非功能需求
- 必须说明决策的适用范围

### 候选方案评估

- 必须从依赖的 primitive/synthesis 提取能力评估和边界
- 不得脱离依赖 draft 独立撰写候选方案评估
- 必须覆盖所有 plan 中声明的候选方案

### 决策分析

- 必须按决策标准（decision-criteria.md）逐项判断
- 必须说明每个维度的权衡
- 不得给出绝对化推荐

### Verdict

- 必须是条件性结论
- 必须明确适用场景和边界
- 必须追溯到 decision-criteria.md
- 必须追溯到 draft.md 的 Decision Analysis / Verdict Draft
