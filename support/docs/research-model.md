# 研究模型

## 总体结构

这个仓库里的四类研究对象，更适合被理解成“两部分结构”：

- 技术分析主链：`primitive -> [optional synthesis] -> domain`
- 场景应用层：`decision`

也就是说：

- `primitive`、`synthesis`、`domain` 共同构成技术分析体系
- `decision` 不属于纯技术分析主链，而是消费前述知识资产来支持具体场景判断

## `primitive`

`primitive` 是最基础的研究单元，通常是：

- 单个 EIP
- 单个协议机制
- 单个链能力点
- 单个接口或执行模型

它负责提供最底层、最可复用的机制事实。

## `synthesis`

`synthesis` 处理多个对象之间的关系，例如：

- 演进顺序
- 分层关系
- 互补 / 替代关系
- 能力边界与职责分工

但要注意：

- `synthesis` 是可选层，不是强制层
- 只有当“对象之间的关系本身”值得长期维护时，才单独抽出一个 synthesis
- 如果关系层还不够稳定或不够复杂，`domain` 可以直接聚合多个 `primitive`

## `domain`

`domain` 是长期主题域，不追求一次写完，而是持续维护：

- 主题边界
- 核心问题簇
- 研究优先级
- 已覆盖对象
- 未覆盖对象

`domain` 是技术分析主链里的知识组织层，但它不应该通过目录结构强行成为 `primitive` 或 `synthesis` 的父节点。一个对象可以同时服务多个 domain，所以 domain 关系应通过链接和元数据表达，而不是通过硬编码路径表达。

例子：

- `account-abstraction`
- `agentic-payment`
- `privacy`

## `decision`

`decision` 面向具体场景做比较与判断，例如：

- 某个业务场景应该优先评估哪些链
- 某种支付形态需要哪类能力
- 某类基础设施应该按什么顺序试验

`decision` 的特点是：

- 它消费技术分析主链里的资产
- 它结合具体场景、需求、约束做判断
- 它不是技术分析主链上的下一层技术对象

## 技术分析主链

```text
domain
   ^
synthesis
   ^
primitive
```

这条链应从下往上读：

- `primitive` 提供机制级事实基础
- `synthesis` 组织关系与演进框架
- `domain` 负责长期主题组织、研究边界和知识聚合

但这不是一条强制每次都经过全部节点的流水线。

## 场景应用层

`decision` 是独立的场景应用层：

- 它消费 `primitive / synthesis / domain`
- 它结合具体场景、需求、约束做判断
- 它的输出不是“更高一层技术对象”，而是“带条件的场景结论”

## 非对称依赖

上层研究依赖下层研究，但不是对称依赖：

- `synthesis` 依赖多个 `primitive`
- `domain` 依赖多个 `primitive`，也可能依赖 `synthesis`
- `decision` 依赖 `primitive / synthesis / domain`
- `primitive` 一般不依赖上层结论

更重要的是，依赖深度也不对称：

- 一个 `decision` 可能对某个候选链要求 `deep`，对另一个候选链只要求 `light`
- 一个 `domain` 可能对某个关键 primitive 要求 `deep`，对其他对象只要求 `focused`

## 依赖声明机制

上层研究必须显式声明：

- 依赖对象
- 依赖层级
- 预算强度
- 依赖原因
- 抽取内容

推荐写在：

- `brief.md`
- `dependencies.md`
- canonical 目录中的 `dependencies.md`

## 为什么需要 `domain`

如果没有 `domain`，研究容易退化成平铺的题目清单。`domain` 的作用是：

- 把同类问题挂到同一主题下
- 帮助决定哪些 `primitive` 值得深挖
- 帮助决定哪些 `synthesis` 应该优先做
- 给 `decision` 提供稳定入口和背景边界

更直接地说：

- `domain` 是技术分析主链里的长期知识组织层
- `decision` 是独立的场景应用层

## 为什么需要 `glossary`

区块链研究经常失败在术语层，而不是资料层。

典型问题：

- 同一个词在不同协议中含义不同
- 同一个能力被不同生态使用不同命名
- 一个词既可能指协议原语，也可能指钱包实现

因此 glossary 必须进入核心 artifact，而不是附录。
