# 事实分析资产

这里存放长期维护的事实分析资产。

## 目录分层

```
knowledge/analysis/
├── primitives/          # 底层机制（按领域分组）
│   ├── account-abstraction/
│   │   ├── eip-4337/
│   │   └── eip-7702/
│   └── scaling/
├── synthesis/           # 演进/综合分析
│   ├── aa-eip-evolution/
│   └── bft-comparison/
└── domains/             # 主题域定义
    └── account-abstraction/
```

## 研究层级

```
primitive（底层机制） → synthesis（演进关系） → domain（问题域）
```

## 各层职责

| 层级 | 职责 | 组织方式 | 交付物 |
|------|------|----------|--------|
| **primitives** | 单一对象的技术实现细节 | 按技术领域分组 | `artifact.md` |
| **synthesis** | 多个对象之间的关系和发展脉络 | 按研究主题组织 | `artifact.md` |
| **domains** | 问题空间的划分和边界 | 按问题空间组织 | `artifact.md` |

## 长期保留的文件

这里默认长期保留：

- `artifact.md`：所有类型的稳定分析结果
- `dependencies.md`（仅 synthesis/domain 需要时保留）

这里不放：

- `request.md`
- `plan.md`
- `evidence-matrix.md`
- 其他只服务当前一轮研究纠偏的过程文件

这些过程文件应进入 `openspec/changes/<change-name>/`。

术语层默认并入 `artifact.md` 的"关键术语"区。

## 与其他目录的关系

| 目录 | 用途 | 与 analysis 的关系 |
|------|------|-------------------|
| `knowledge/decisions/` | 场景决策 | 消费 analysis 的分析结果 |
| `openspec/changes/` | 过程层 | analysis 的 inputs，通过后提升到 analysis |
