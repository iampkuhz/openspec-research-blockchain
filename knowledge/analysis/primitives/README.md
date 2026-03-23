# Primitives（原语）

这里存放底层机制研究的长期 artifact。

## 目录结构

```
primitives/
├── account-abstraction/
│   ├── eip-4337/
│   ├── eip-7560/
│   └── eip-7702/
├── cross-chain/          # 未来扩展
└── scaling/              # 未来扩展
```

## 按领域分组

Primitive 按**技术领域**分组，每个领域下包含多个相关的 primitive：

- **account-abstraction/**：账户抽象相关（EIP-4337、EIP-7560、EIP-7702）
- **cross-chain/**：跨链相关（未来扩展，如 Avalanche ICM、Cosmos IBC）
- **scaling/**：扩容方案相关（未来扩展，如 Optimistic Rollup、ZK Rollup）

## 交付物

每个 primitive 默认只保留：
- `artifact.md`：机制分析文档

## 研究深度

Primitive artifact 必须在文档开头标注研究深度：
- `deep`：全面深挖，产出可复用的 reference
- `focused`：针对特定问题深入，不追求全面
- `light`：快速了解，确认基本事实

## 与上层研究的关系

- 一个 primitive 可以被多个 synthesis 复用
- 一个 primitive 可以被多个 domain 复用
- 与哪些 synthesis/domain 相关，应通过 `plan.md`、正文链接来声明
- Primitive 不通过目录路径被锁死为某个 domain 的子节点

## 新增 primitive 的流程

1. 创建 change packet：`./scripts/new_change.sh primitive <name>-deep-dive-pass-1`
2. 编写 `request.md` → 生成 `plan.md` → 生成 `draft.md` → 提炼 `artifact.md`
3. 根据 primitive 的技术领域，放入对应的分组目录
