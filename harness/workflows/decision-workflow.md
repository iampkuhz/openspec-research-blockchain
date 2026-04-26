# Decision Workflow

**task_type**：`decision`
**对应 Workflow**：`harness/workflows/decision-workflow.md`

---

## 适用场景

- 场景驱动的选型或决策分析
- 在多个选项中基于特定场景约束做出有限判断

## 输入

- `request.md`（声明场景、候选方案、决策目的）
- `plan.md`（声明比较维度、依赖的 primitive/synthesis）
- `decision-criteria.md`（可选，声明决策标准）

## 输出

- `sources/source-pack.md`
- `sources/evidence-map.md`
- `draft.md`（包含场景定义、候选方案评估、决策分析、Verdict Draft）
- `review.md`

## 推荐 child change 拆分方式

- decision change 依赖其引用的所有 primitive 和 synthesis changes
- 如依赖的 primitive/synthesis 不存在，先创建对应 changes
- decision 独立一个 change

## draft.md 写作重点

- **场景定义**：明确约束条件、优先级、非功能需求
- **候选方案评估**：从依赖的 primitive/synthesis 提取能力评估和边界
- **决策分析**：按决策标准逐项判断
- **Verdict Draft**：条件性结论，明确适用场景和边界
- 不得脱离 primitive draft / synthesis draft 独立撰写候选方案评估
- 必须追溯到 `decision-criteria.md`（如声明）

## review 重点

- 场景定义是否清晰
- 候选方案评估是否基于可靠的依赖 artifacts
- 决策分析是否按标准执行
- Verdict Draft 是否有条件限制
- 是否避免了绝对化推荐

## Publish targets

```text
knowledge/decisions/<domain_id>/<topic_slug>/artifact.md
knowledge/decisions/<domain_id>/<topic_slug>/verdict.md
```

## 决策链路

```text
decision-criteria.md
  → draft.md#Decision Analysis / Verdict Draft
    → decision-verdict.md（template 生成的最终 verdict）
      → knowledge/decisions/**/verdict.md
```

## 禁止事项

- 不得脱离依赖 draft 独立撰写候选方案评估
- 不做绝对化推荐（必须是 bounded conclusions）
- 不生成 work-products/*.md
