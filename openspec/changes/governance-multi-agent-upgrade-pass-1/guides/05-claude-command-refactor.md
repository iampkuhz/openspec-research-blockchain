# 05 Claude Command Refactor

## 目标

让 `.claude/commands/` 从“自己做完全部阶段”改成“根据 workflow + agent contracts 编排 active agents”。

## 命令分工

| 命令 | 角色 |
|------|------|
| `/spec-research` | orchestrator 入口 |
| `/spec-request` | request 阶段入口，主要消费 `research-author-agent` contract |
| `/spec-plan` | plan 阶段入口，联动 `research-author-agent` 与 `source-evidence-agent` |
| `/spec-draft` | draft 阶段入口，联动 `research-author-agent` 与 `diagram-agent` |
| `/spec-artifact` | publish 阶段入口，消费 `publish-agent` contract |

## 重构要求

- 不在命令里复制整份 workflow 规则
- 不在命令里重新定义 artifact contract
- 必须引用：
  - `harness/workflows/*.md`
  - `harness/agents/*.md`
  - 对应的 OpenSpec spec

## `/spec-research` 的新职责

1. 判断目标 change 与任务语义
2. 选择 active agents
3. 决定哪些步骤可并行
4. 在阶段间执行质量闸门
5. 汇总结果，不代替 author / reviewer 写各自产物

## fallback

若运行环境不支持真实 subagent：

- 仍按 active agents 的 contract 顺序执行
- 在总结中明确标注串行折叠执行
