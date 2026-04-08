# 05 Claude Command Refactor

## 目标

让 `.claude/commands/` 从“自己做完全部阶段”改成“根据 workflow + agent contracts 编排 active agents”。

## 命令分工

| 命令 | 角色 |
|------|------|
| `/spec-research` | 命令层入口 |
| `/spec-request` | request 阶段入口，主要消费 @research-author-agent contract |
| `/spec-plan` | plan 阶段入口，联动 @research-author-agent 与 @source-evidence-agent |
| `/spec-draft` | draft 阶段入口，联动 @research-author-agent 与 @diagram-agent |
| `/spec-artifact` | publish 阶段入口，消费 @publish-agent contract |

## 重构要求

- 不在命令里复制整份 workflow 规则
- 不在命令里重新定义 artifact contract
- 必须引用：
  - `harness/workflows/*.md`
  - `harness/agents/*.md`
  - 对应的 OpenSpec spec

## 所有命令的统一要求

每个 `.claude/commands/*.md` 都应显式说明：

1. 哪些准备动作可以并行
2. 哪些步骤必须串行
3. 命令级冰箱策略
4. 冰箱项最终写到哪里
5. 总结中如何报告被冻结的工作

## `/spec-research` 的新职责

1. 判断目标 change 与任务语义
2. 选择 active agents
3. 决定哪些阶段内窗口可并行
4. 维护冰箱清单
5. 在阶段间执行质量闸门
6. 汇总结果，不代替 author / reviewer 写各自产物

## fallback

若运行环境不支持真实 subagent：

- 仍按 active agents 的 contract 顺序执行
- 在总结中明确标注串行折叠执行

## 冰箱策略

命令层的冰箱策略不创造新正式文件类型，而是：

- 复用 `待确认问题`
- 复用 `证据缺口`
- 复用 `review/issues.md`
- 在最终总结中追加冰箱清单
