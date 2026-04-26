# Traceability Rules

## 追溯链

```
knowledge artifact claim
  → draft.md claim
    → evidence-map.md mapping
      → source-pack.md source
        → URL / 本地归档
```

## 要求

- 每个核心 claim 必须有 source 引用
- source 引用格式：`[L1: 来源名称]`
- 从 draft 提炼为 artifact 时，source 引用必须保留（可简化格式）
- 证据缺口必须在 draft 和 artifact 中明确列出

## 检查方式

- 手工检查：遍历 draft 中的核心主张，确认每个都有 source 引用
- Hook 检查：`traceability` validator 可检查 claim → source 映射
- 评审检查：review-critic-agent 评审时检查 traceability

## 与 evidence policy 的关系

- Traceability rules 定义 claim → source 的追溯机制
- Evidence policy 定义来源的证据等级
- 两者配合使用
