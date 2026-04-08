# 03 Collaboration Protocol

## 编排原则

1. `orchestrator` 负责决定“激活谁”，不负责写主正文。
2. 各 agent 只写自己拥有的文件面，不交叉覆盖。
3. review 必须保持独立，不与 author 合并。
4. 子任务缺少清晰 handoff artifact 时，优先合并角色而不是强行拆分。

## 标准 handoff artifact

| From | To | Handoff |
|------|----|---------|
| orchestrator | research-author-agent | change 路径、对象类型、激活约束、目标交付物 |
| research-author-agent | source-evidence-agent | 研究问题、来源优先级、待验证列表 |
| source-evidence-agent | research-author-agent | `sources/`、核心 excerpts、source-review、evidence gaps |
| research-author-agent | diagram-agent | 实体分类、图表清单、diagram brief |
| research-author-agent | review-critic-agent | `draft.md`、`plan.md`、`sources/`、自评未决问题 |
| review-critic-agent | publish-agent | approved / blocked 结论、必须修复项 |

## 并行规则

### 可以并行

- `research-author-agent` 写 `plan.md` 与 `source-evidence-agent` 收集来源
- `research-author-agent` 写正文时，`diagram-agent` 可并行准备 diagram package

### 不应并行

- `research-author-agent` 与 `review-critic-agent` 不能同时改 `draft.md`
- `publish-agent` 不能在 review 结论未明确前写长期资产

## 冲突处理

- 文件归属冲突时，以 agent contract 的 write scope 为准
- 事实冲突时，以 L1/L2 与 `review-critic-agent` 的结论为准
- 治理边界冲突时，以 `docs/governance/openspec-harness-boundary.md` 为准

## 降级策略

当 subagent 能力不可用、任务很小或上下文过于耦合时：

- 仍按同一套 contract 顺序执行
- 由主 agent 串行模拟 active agents
- 但必须在总结中说明哪些角色被串行折叠执行
