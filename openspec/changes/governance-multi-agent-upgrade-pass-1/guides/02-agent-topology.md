# 02 Agent Topology

## 第一版 Agent Roster

### 常驻角色

| Agent | 主要职责 | 关键输出 |
|-------|----------|----------|
| @research-author-agent | 负责 `request / plan / draft` 主链写作与增量修订 | `request.md`、`plan.md`、`draft.md` |
| @source-evidence-agent | 负责来源收集、excerpts、source-review、证据缺口盘点 | `sources/`、`source-review.md` |
| @review-critic-agent | 独立技术评审、traceability audit、术语一致性检查 | `review/checklist.yaml`、`issues.md`、`review-summary.md` |
| @publish-agent | 提炼长期 artifact，执行 update impact scan 与 apply 前检查 | `artifact.md`、`verdict.md`、impact notes |

### 条件角色

| Agent | 激活条件 | 关键输出 |
|-------|----------|----------|
| @diagram-agent | primitive / mechanism-heavy / 明确需要图表 | `diagrams/` package、diagram checklist、contract validation |
| @governance-review-agent | 修改 `openspec/**`、`harness/**`、`AGENTS.md`、治理边界 | `review/governance-review.md` |

## 为什么这样合并

- @plan-architect-agent + @analysis-agent 合并为 @research-author-agent
  - 原因：`plan -> draft` 是强连续链，拆分会增加 handoff 成本
- @traceability-auditor 不并入 source producer，而并入 @review-critic-agent
  - 原因：证据生产者与证据审计者应保持独立
- @artifact-promoter-agent + @update-impact-agent 合并为 @publish-agent
  - 原因：都属于发布后处理链，输入高度重叠

## 激活矩阵

| Workflow | Always-on | Conditional |
|----------|-----------|-------------|
| `intake` / `request` | 命令层，@research-author-agent | @governance-review-agent（仅治理改造） |
| `source` | 命令层，@source-evidence-agent | 无 |
| `plan` | 命令层，@research-author-agent, @source-evidence-agent | 无 |
| `draft` | 命令层，@research-author-agent | @diagram-agent |
| `review` | 命令层，@review-critic-agent | @diagram-agent（如存在图） |
| `merge/apply` | 命令层，@publish-agent | @governance-review-agent（治理类变更不 apply 到 knowledge） |
