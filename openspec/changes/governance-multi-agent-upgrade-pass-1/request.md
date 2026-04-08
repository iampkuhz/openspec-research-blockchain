## 研究对象

- 对象类型：domain
- 研究路径：domain overview
- 相关 domains：repository-governance, research-execution, agent-orchestration

## 当前要回答的问题

1. 当前仓库从单 agent 阶段命令升级到 multi-agent 编排时，哪些职责必须独立，哪些职责应合并，才能在不显著增加复杂度的前提下提高分析质量？
2. OpenSpec、Harness、Claude Code 命令层在这次升级中的职责边界应该如何划分，才能避免把执行层约定误写进正式规则层？
3. 第一版 agent roster、交接物、质量闸门和降级策略应如何设计，才能兼容现有 `request -> plan -> draft -> artifact` 主链？
4. 哪些现有入口文件、workflow、rules、skills、commands 存在语义漂移，会直接影响后续 subagent 编排质量，需要在本轮一并修正？
5. 在不同时全面改造 Qoder 侧命令的前提下，如何为未来的多 agent 执行预留可复用骨架？

## 为什么现在要研究

当前仓库已经形成较清晰的 OpenSpec + Harness + Commands 分层，但执行层仍以单 agent 串行工作为主。现有 `.claude/commands/spec-*.md` 可以覆盖主要阶段，却缺少：

- agent roster 与激活规则
- 明确的 handoff artifact
- 独立 reviewer / auditor 视角
- diagram / governance 这类条件能力的按需启用机制
- 对旧入口语义漂移的统一收口

如果继续在现状上叠加 prompt，仓库分析质量会受到上下文污染、职责混用和自审偏差影响。

## 范围

### 覆盖对象

- `AGENTS.md`
- `README.md`
- `harness/workflows/`
- `harness/rules/general/`
- `harness/agents/`（新增）
- `.claude/commands/spec-*.md`
- `.qoder/agents/`（新增基础骨架）
- 与 apply / update / traceability 强相关的 maintenance skills

### 覆盖链/协议

- 不适用；本轮为仓库治理与执行架构改造

### 时间窗口

- 2026-04 第一版 multi-agent 升级

## 非目标

- 不在本轮同时完成 Claude Code 与 Qoder 两侧的完整命令级等价实现
- 不在本轮重写全部 research rules 或所有历史技能
- 不把 multi-agent 执行细节上移到 OpenSpec 正式规则层
- 不试图一次性清空仓库中所有历史术语与路径残留

## 已知输入

- `openspec/config.yaml`
- `openspec/schemas/blockchain-research/schema.yaml`
- `docs/governance/openspec-harness-boundary.md`
- `harness/workflows/research-pipeline.md`
- `harness/workflows/review-workflow.md`
- `harness/workflows/governance-review-workflow.md`
- `.claude/commands/spec-research.md` 及分步命令
- `skills/README.md` 与 maintenance skills
- 当前 `.qoder/agents/` 为空

## 预期输出

- `openspec/changes/governance-multi-agent-upgrade-pass-1/guides/*.md`
- `harness/agents/_index.yaml` 与各 agent contract
- 多 agent 感知的 workflow / command 更新
- 一批关键入口漂移修正，使第一版编排具备稳定基线
