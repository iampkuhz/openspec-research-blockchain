# harness/ — 执行规约层 / 质量门禁层 / 边界治理层

**定位**：harness/ 是 OpenSpec 区块链研究的执行规约层。

## 与外层的关系

| 层 | 拥有者 | 职责 |
|---|---|---|
| OpenSpec | `openspec/` | artifact contracts、对象模型、产物路径、模板、apply 规则 |
| **Harness** | `harness/` | 执行步骤、质量门禁、artifact 规则、research 规则 |
| Command | `.claude/commands/` | 用户入口、任务路由 |
| Skill | `skills/`、`.claude/skills/` | 可复用执行能力 |
| Hook/Script | `scripts/hooks/` | 确定性校验 |
| Knowledge | `knowledge/` | 最终长期研究资产 |

详细边界见 [`harness/governance/openspec-harness-boundary.md`](./governance/openspec-harness-boundary.md)。

## Active Workflows

| Workflow | 对应 Command | 说明 |
|---|---|---|
| `research-pipeline.md` | `/spec-research` | 端到端研究编排与 agent capsule 调度 |
| `research-intake-routing.md` | `/spec-research` | 研究请求接入、task_type 判断、change 初始化、request/plan 生成 |
| `research-step-execution.md` | `/spec-research-step` | 自动下一步判断、sources/draft/review 生成 |
| `source-workflow.md` | — | 来源收集、链接验证与 evidence map 阶段流程 |
| `research-publish-flow.md` | `/spec-research-publish` | publish 校验、knowledge artifact 生成 |
| `source-reading-workflow.md` | — | task_type=source_reading 的执行流程 |
| `primitive-workflow.md` | — | task_type=primitive 的执行流程 |
| `synthesis-workflow.md` | — | task_type=synthesis 的执行流程 |
| `decision-workflow.md` | — | task_type=decision 的执行流程 |
| `governance-review-workflow.md` | `/spec-governance-review` | 规约体系评审 |
| `diagram-workflow.md` | — | 图表创建（PlantUML） |

完整索引见 [`harness/workflows/_index.yaml`](./workflows/_index.yaml)。

## Active Rule Categories

| 类别 | 说明 | 路径 |
|---|---|---|
| Artifact Rules | 每个 artifact 文件的质量要求 | `harness/rules/artifacts/` |
| Research Rules | 研究类型质量规则 | `harness/rules/research/` |
| Cross-cutting Rules | 写作风格、图表、通用规则 | `harness/rules/writing/`、`harness/rules/diagrams/`、`harness/rules/general/` |

完整索引见 [`harness/rules/_index.yaml`](./rules/_index.yaml)。

## Hook Governance

- Hook 注册表：[`harness/hooks/registry.yaml`](./hooks/registry.yaml)
- Schema 接线说明：[`harness/hooks/schema-wiring.md`](./hooks/schema-wiring.md)
- Hook 系统说明：[`harness/hooks/README.md`](./hooks/README.md)

## 禁止事项

- 不直接修改 `knowledge/` 主线，必须通过 change + publish 流程
- 不生成 `work-products/*.md`，统一使用 `draft.md`
- 不在 harness 中重新定义 OpenSpec 的 artifact graph
- 不保留 `principle-atom` / `atom-definition` 等旧命名，统一使用 `primitive`
