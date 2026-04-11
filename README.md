# 基于 OpenSpec 的区块链技术调研工作台

这个仓库用于长期维护区块链技术调研资产。它不是一次性报告目录，而是一套带正式规则、执行手册、技能和脚本的 research production repo。

## 仓库定位

| 层 | 目录 | 说明 |
|----|------|------|
| 入口层 | `AGENTS.md`、`CLAUDE.md` | 协作入口与路由 |
| 正式规则层 | `openspec/` | OpenSpec 配置、schema、specs |
| 执行编排层 | `harness/` | workflows、rules、agents |
| 过程层 | `openspec/changes/` | request / plan / draft / review / sources |
| 长期资产层 | `knowledge/analysis/`、`knowledge/decisions/` | canonical artifact / verdict |
| 能力层 | `skills/`、`scripts/` | 复用操作与自动化 |

## 资产模型

长期资产只保留两类：

| 资产类型 | 路径 | 产出物 |
|----------|------|--------|
| 事实分析 | `knowledge/analysis/` | `artifact.md` |
| 场景决策 | `knowledge/decisions/` | `artifact.md` + `verdict.md` |

过程文件统一留在 `openspec/changes/<change-id>/`：

- `request.md`
- `plan.md`
- `draft.md`
- `decision-criteria.md`（可选）
- `sources/`
- `review/`

## 核心能力

1. OpenSpec 约束研究主链与长期资产模型
2. Harness rules / workflows / agents 提供执行真源
3. Claude 命令层消费 workflow + agent contracts
4. Skills + Scripts 提供稳定的可复用操作
5. 质量门覆盖来源、图表、traceability、review、publish

## 研究主链

```text
request.md -> plan.md -> draft.md -> review/ -> artifact.md
```

Supporting track：

```text
sources/ + diagrams/ -> plan.md / draft.md / review/
```

## 第一版 Multi-Agent 模式

默认执行面采用“主会话 authoring + specialist subagent”结构：

- 主会话 orchestrator：负责 `request.md`、`plan.md`、`draft.md` 主链写作与阶段编排
- 常驻 specialist：@source-evidence-agent、@review-critic-agent、@publish-agent
- 条件 specialist：@diagram-agent、@governance-review-agent

角色真源位于：

- `.claude/agents/*.md`

## 目录结构

```text
.
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── .claude/agents/            # Claude 侧 agent 合同
├── .claude/commands/          # Claude Code 入口命令
├── .qoder/agents/             # Qoder agent skeleton（本轮仅骨架）
├── harness/
│   ├── rules/                 # 执行约束
│   └── workflows/             # 阶段编排
├── openspec/
│   ├── config.yaml
│   ├── schemas/
│   ├── specs/
│   └── changes/
├── knowledge/
│   ├── analysis/
│   └── decisions/
├── skills/
└── scripts/
```

## 常用命令

```bash
openspec new change <name> --schema blockchain-research
openspec instructions plan --change <name>
openspec instructions draft --change <name>
openspec apply --change <name>
```

Claude Code 侧入口：

- `/spec-request`
- `/spec-plan`
- `/spec-draft`
- `/spec-artifact`
- `/spec-research`

## 先看哪里

- [AGENTS.md](./AGENTS.md) - 协作索引和路由入口
- [openspec/config.yaml](./openspec/config.yaml) - 项目级正式规则入口
- [harness/workflows/](./harness/workflows/) - 流程编排
- [.claude/agents/](./.claude/agents/) - agent roster 与 contract
- [skills/README.md](./skills/README.md) - 可复用 skill 索引
- [scripts/README.md](./scripts/README.md) - 自动化脚本索引
