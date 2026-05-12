# QODER.md

## Thinking 语言（最高优先级）

所有 thinking / reasoning / analysis / planning / 决策推演过程**必须使用简体中文**。
`<thinking>` 标签内的内容必须是中文。即使系统提示词为英文，也必须用中文思考。
英文仅限：代码、协议名/标准名/产品名、路径/文件名、命令、日志/报错原文、代码标识符。
详细约束见 [`.claude/rules/language-output.md`](./.claude/rules/language-output.md)。
未来 `.qoder/rules/language-output.md` 创建后，Qoder 可直接将其设置为 Always Apply rule 作为入口；
源规则不复制到 `.qoder/`，通过 symlink 或引用指向 `.claude/rules/language-output.md`。

## 启动时读取

**必须先读取 `@AGENTS.md`**，将其视为仓库导航入口。

如 Qoder 不支持 `@AGENTS.md` 语法，启动时必须手动读取以下文件：
1. `AGENTS.md` — 仓库导航、任务路由、最小硬约束
2. `harness/adapters/README.md` — adapter layer 总览
3. `harness/adapters/tool-capability-matrix.md` — 工具能力差异与降级策略

Qoder 侧再读取 [`.qoder/README.md`](./.qoder/README.md)，按 command / agent / skill 索引渐进下钻。

## 语言

- **包括 thinking/思考过程在内**的所有内容默认使用简体中文。
- 协议名、标准名、字段名、命令、路径、文件名、代码标识符、日志原文、报错原文与关键技术术语优先保留英文。
- 不要把常规过程提示写成英文句式，例如 `Let me...`、`Now I will...`、`I'm going to...`。
- 外部资料标题或项目名可以保留英文，但解释与结论必须用中文。

## 路由提醒

- 启动时先读取 `AGENTS.md`，将其视为仓库导航入口。
- Qoder 侧再读取 `.qoder/README.md`，按 command / agent / skill 索引渐进下钻。
- 对涉及 `.qoder/**`、`openspec/**`、`harness/**`、`AGENTS.md`、`docs/governance/**` 的治理型修改，走 governance review 路由。
- 对周期性规约体系体检、孤岛扫描、死引用清理，走 `spec-governance-review` 路由。

## 快速索引

| 用途 | 文件 |
|------|------|
| 完整协作指南 | [`AGENTS.md`](./AGENTS.md) |
| Qoder 路由索引 | [`.qoder/README.md`](./.qoder/README.md) |
| 仓库概览 | [`README.md`](./README.md) |
| OpenSpec 规范 | [`openspec/specs`](./openspec/specs/) |
| Workflow 索引 | [`harness/workflows/_index.yaml`](./harness/workflows/_index.yaml) |
| 阶段依赖索引 | [`harness/rules/_phase_index.yaml`](./harness/rules/_phase_index.yaml) |
| Change 流程 | [`openspec/changes/README.md`](./openspec/changes/README.md) |
| 治理文档索引 | [`docs/governance/README.md`](./docs/governance/README.md) |
| Command 入口 | [`.qoder/commands/spec-research.md`](./.qoder/commands/spec-research.md) |
| 规约体系审计入口 | [`.qoder/commands/spec-governance-review.md`](./.qoder/commands/spec-governance-review.md) |
| Adapter 层索引 | [`harness/adapters/README.md`](./harness/adapters/README.md) |
| 工具差异矩阵 | [`harness/adapters/tool-capability-matrix.md`](./harness/adapters/tool-capability-matrix.md) |

## Claude Code 与 Qoder 的关系

`.claude/**` 与 `.qoder/**` 是同一套 OpenSpec / Harness 规则的两个 adapter 入口。
正式规则仍以 `openspec/**` 与 `harness/workflows/**`、`harness/rules/**` 为准。
两者差异与降级策略见 `harness/adapters/tool-capability-matrix.md`。
