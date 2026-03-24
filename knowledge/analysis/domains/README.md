# Domains（主题域）

这里存放主题域定义的长期 artifact。

## 目录结构

```
domains/
├── account-abstraction/      # 账户抽象主题域
├── cross-chain-interoperability/  # 未来扩展：跨链互操作性
└── consensus-mechanisms/     # 未来扩展：共识机制
```

## 按问题空间组织

Domain 按**问题空间**组织，每个 domain 定义一个大的主题领域：

- **account-abstraction/**：账户抽象问题域
  - 问题簇：账户表达、交易入口、验证授权、gas 支付
  
- **cross-chain-interoperability/**（未来）：跨链互操作性问题域
  - 问题簇：资产互操作、消息传递、状态验证、安全性假设
  
- **consensus-mechanisms/**（未来）：共识机制问题域
  - 问题簇：最终性、验证者选择、分叉处理、激励机制

## 交付物

每个 domain 默认长期保留：
- `artifact.md`：域定义文档（原 `reference.md`）
- `dependencies.md`（如需要）：依赖声明

## Domain 的职责

Domain 关注**问题空间的划分和边界**：

1. **问题簇划分**：将大问题拆成多个子问题
2. **与相邻 domain 的关系**：定义上下游、平行 domain
3. **价值定位**：为什么这个 domain 值得长期维护

## 与下层研究的关系

- Domain 依赖下层的 primitive 和 synthesis 提供机制事实
- Domain 不得重写下层研究的全文，只能引用和综合
- 一个 domain 可以复用多个 primitive 和 synthesis

## 与上层 decision 的关系

- Domain 会被多个 decision 场景复用
- Decision 将 domain 的问题框架应用到具体场景

## 新增 domain 的流程

1. 创建 change packet：`./scripts/new_change.sh domain <topic>-overview-pass-1`
2. 编写 `request.md` → 生成 `plan.md` → 生成 `draft.md` → 提炼 `artifact.md`
3. 放入 `domains/` 目录

## 何时需要 Domain？

✅ 需要 domain 的场景：
- 同时涉及多个 primitive 和 synthesis
- 容易被混淆或误解（如"AA 到底是什么"）
- 需要长期维护问题框架
- 会被多个 decision 场景复用

❌ 不需要 domain 的场景：
- 只研究单一对象的技术细节 → **primitive**
- 只分析多个对象的演进关系 → **synthesis**
- 只做特定场景的选型决策 → **decision**
