# 04 Harness Refactor

## 改造目标

把 `Harness` 升级成 multi-agent 编排真源。

## 必做项

1. 新增 `harness/agents/_index.yaml`
2. 为每个 agent 建立 contract 文档
3. 在 `research-pipeline` 中加入：
   - 默认 active roster
   - agent 激活条件
   - handoff artifact
   - fallback
4. 在 `review`、`source`、`merge`、`governance-review` workflow 中声明默认执行角色

## 约束

- workflow 不应重复整份 agent contract
- agent contract 不应重写 OpenSpec artifact contract
- workflow 负责阶段编排，agent contract 负责角色边界

## 推荐文件布局

```text
harness/
├── agents/
│   ├── _index.yaml
│   ├── research-author-agent.md
│   ├── source-evidence-agent.md
│   ├── review-critic-agent.md
│   ├── publish-agent.md
│   ├── diagram-agent.md
│   └── governance-review-agent.md
└── workflows/
    └── research-pipeline.md
```

## 验收

- `AGENTS.md` 能把人和 agent 一路路由到 `harness/agents/`
- workflow 能回答“谁应该做这一步”
- command 能回答“应激活哪些角色”
