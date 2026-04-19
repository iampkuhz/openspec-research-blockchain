# 事实分析资产

这里存放长期维护的事实分析资产。

## 目录分层

```
knowledge/analysis/
├── _registry/
│   └── domains.yaml       # domain 注册表
├── primitives/            # 底层机制（按 domain 分组）
│   ├── account-abstraction/
│   │   ├── eip-4337/
│   │   └── eip-7702/
│   └── consensus/
│       ├── consensus-qbft/
│       └── consensus-tendermint/
└── synthesis/             # 演进/综合分析（扁平化）
    ├── bft-comparison/
    └── evolution-aa-eip/
```

## 对象类型

| 层级 | 职责 | 组织方式 | 交付物 |
|------|------|----------|--------|
| **primitives** | 单一对象的技术实现细节 | 按 `<domain_id>/<topic_slug>` 分组 | `artifact.md` |
| **synthesis** | 多个对象之间的关系和发展脉络 | 按 `<topic_slug>` 扁平化组织 | `artifact.md` |

## domain 分组

`domain` 是 taxonomy / 浏览分组概念，不是独立的 `object_type`。

- `primitives/` 下的子目录名即为 `domain_id`
- 所有合法的 `domain_id` 必须在 `_registry/domains.yaml` 中注册
- `domain` 不提供独立的 `artifact.md`

## 长期保留的文件

这里默认长期保留：

- `artifact.md`：所有类型的稳定分析结果

这里不放：

- `request.md`
- `plan.md`
- `draft.md`
- 其他只服务当前一轮研究纠偏的过程文件

这些过程文件应进入 `openspec/changes/<change-name>/`。

## 与其他目录的关系

| 目录 | 用途 | 与 analysis 的关系 |
|------|------|-------------------|
| `knowledge/decisions/` | 场景决策 | 消费 analysis 的分析结果 |
| `openspec/changes/` | 过程层 | analysis 的 inputs，通过后提升到 analysis |
