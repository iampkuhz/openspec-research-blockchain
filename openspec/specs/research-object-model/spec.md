# 研究对象模型

## 目的

定义本仓库中的研究对象层级与相互关系。

## 要求

- 研究对象必须显式区分为 `domain`、`primitive`、`synthesis`、`decision` 四类。
- 技术分析主链必须按 `primitive -> [optional synthesis] -> domain` 理解。
- `decision` 必须作为独立的场景应用层存在，而不是技术分析主链的下一层。
- `synthesis` 是可选层，不得强制要求每个 `domain` 都拥有独立 `synthesis`。
- `primitive` 与 `synthesis` 不得通过路径被锁死为某个 `domain` 的子节点。
- 上层研究必须显式声明依赖对象、budget 与抽取边界。
