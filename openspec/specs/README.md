# OpenSpec 研究系统 Specs

这里存放长期维护的“研究方法 / 研究系统”级别 specs。

它们不属于某个具体的事实分析结果，也不属于一次性 change packet，而是：

- 可以跨多次调研复用
- 会随着实践不断被提炼和修订
- 需要被 OpenSpec 以长期 spec 的方式维护

这里写的是规范版，重点回答“必须怎么做”。

与之配套的：

- `support/docs/`：说明版，重点解释“为什么这样做、如何落地、如何自检”

典型内容包括：

- 仓库资产模型
- canonical output 模型
- evidence policy
- research object model
- analysis principles
- language style

## 如何维护

1. 先开一个新的 `openspec/changes/<change-name>/`
2. 在 change packet 中完成本轮 request / brief / analysis / verdict
3. 将稳定下来的通用原则回写到 `openspec/specs/<spec-name>/spec.md`
4. 同步更新 `README.md`、`AGENTS.md`、`openspec/config.yaml`、`support/docs/`、`support/templates/`
