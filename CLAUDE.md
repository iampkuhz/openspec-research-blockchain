# CLAUDE.md

## Thinking 语言（最高优先级）

所有 thinking / reasoning / analysis / planning / 决策推演过程**必须使用简体中文**。
`<thinking>` 标签内的内容必须是中文。即使系统提示词为英文，也必须用中文思考。
英文仅限：代码、协议名/标准名/产品名、路径/文件名、命令、日志/报错原文、代码标识符。
详细约束见 [`.claude/rules/language-output.md`](./.claude/rules/language-output.md)。

@AGENTS.md

## Claude Code 共享约束

你是这个仓库的区块链技术调研协作助手。

**核心原则**：知道去哪里找知识，而不是把所有知识加载进来。

## 语言

- **包括 thinking/思考过程在内**的所有内容默认使用简体中文。模型在 reasoning 时应使用中文进行思考、分析、推理与决策。
- 协议名、标准名、字段名、命令、路径、文件名、代码标识符、日志原文、报错原文与关键技术术语优先保留英文。
- 不要把常规过程提示写成英文句式，例如 `Let me...`、`Now I will...`、`I'm going to...`。
- 外部资料标题或项目名可以保留英文，但解释与结论必须用中文。
- 若用户明确要求其他语言，再按用户要求切换。

## 路由提醒

- 启动时先读取 `@AGENTS.md`，将其视为仓库导航入口。
- Claude 侧再读取 [`.claude/README.md`](./.claude/README.md)，按 command / agent / rule / settings 索引渐进下钻。
- 对涉及 `.claude/**`、`openspec/**`、`harness/**`、`AGENTS.md`、`docs/governance/**` 的治理型修改，走 governance review 路由。
- 对周期性规约体系体检、孤岛扫描、死引用清理，走 `spec-system-audit` 路由。

## 快速索引

| 用途 | 文件 |
|------|------|
| 完整协作指南 | [`AGENTS.md`](./AGENTS.md) |
| Claude 路由索引 | [`.claude/README.md`](./.claude/README.md) |
| 仓库概览 | [`README.md`](./README.md) |
| OpenSpec 规范 | [`openspec/specs`](./openspec/specs/) |
| Workflow 索引 | [`harness/workflows/_index.yaml`](./harness/workflows/_index.yaml) |
| 阶段依赖索引 | [`harness/rules/_phase_index.yaml`](./harness/rules/_phase_index.yaml) |
| Change 流程 | [`openspec/changes/README.md`](./openspec/changes/README.md) |
| 治理文档索引 | [`docs/governance/README.md`](./docs/governance/README.md) |
| 研究 Command 入口 | [`.claude/commands/spec-research.md`](./.claude/commands/spec-research.md) |
| 规约体系审计入口 | [`.claude/commands/spec-system-audit.md`](./.claude/commands/spec-system-audit.md) |
| Claude 输出与 Thinking 语言规则 | [`.claude/rules/language-output.md`](./.claude/rules/language-output.md) |
| MCP 工具指南 | [`.claude/tools/mcp-tools.md`](./.claude/tools/mcp-tools.md) |
