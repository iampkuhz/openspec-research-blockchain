# Command / Skill / Harness Workflow / Rule / Hook 边界

**本文件位置**：`harness/governance/command-skill-boundary.md`
**用途**：定义 Command / Skill / Harness Workflow / Harness Rule / Hook 的职责边界与映射关系。

---

## 职责定义

| 概念 | 职责 | 不做什么 |
|---|---|---|
| **Command** | 用户入口 / routing / 本次任务边界 | 不包含具体写作步骤、不定义质量规则 |
| **Skill** | 可复用执行能力 / 多步骤执行策略 / 脚本与模板组织 | 不定义 artifact 正式语义、不直接生成最终 knowledge |
| **Harness Workflow** | 执行规约，解释某类任务的步骤与输入输出 | 不直接触发、不替代 command 的路由职责 |
| **Harness Rule** | 质量规则，定义 artifact 或 task_type 的质量要求 | 不直接生成产物、不和 schema 冲突 |
| **Hook / Script** | 确定性校验，质量 gate 的自动化落地 | 不替代人类评审、不通过路径硬猜语义 |

## Active Commands 与 Primary Skills 映射

| Command | Primary Skills |
|---|---|
| `/spec-research` | `openspec-route-research-change`、`openspec-init-change`、`openspec-build-request-plan` |
| `/spec-research-step` | `openspec-build-research-support`、`research-extract-evidence`、`research-write-source-note`、`openspec-build-draft`、`openspec-build-review` |
| `/spec-research-publish` | `openspec-build-publish-plan`、`publish-validate-targets`、`publish-render-artifact`、`publish-render-verdict`、`publish-merge-knowledge` |
| `/spec-governance-review` | `governance-review-system`、`governance-review-boundaries`、`governance-cleanup-legacy` |

## Workflow 与 Command 的关系

- Workflow 文件描述**怎么做**，但不直接作为用户入口
- Command 文件决定**什么时候调用哪个 workflow**
- 一个 command 可对应多个 workflow（如 `/spec-research-step` 对应 `research_step_execution`）
- 一个 workflow 可被多个 command 间接引用（如 `source-reading-workflow.md` 被 intake 和 step 都引用）

## Rule 与 Workflow 的关系

- Workflow 文件引用 Rule 文件，但 Rule 不反向引用 Workflow
- Rule 文件只定义质量要求，不定义执行步骤
- 同一 Rule 可被多个 Workflow 引用

## Hook 与 Rule 的关系

- Hook 是 Rule 的自动化实现
- 不是所有 Rule 都有对应的 Hook（部分质量要求依赖人类评审）
- Hook registry（`harness/hooks/registry.yaml`）声明 validator id → script 映射
- Hook 脚本位于 `scripts/hooks/validators/`
