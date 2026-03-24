# 事实分析资产

这里存放长期维护的事实分析资产。

## 目录分层

```
knowledge/analysis/
├── primitives/          # 底层机制研究（按领域分组）
│   ├── account-abstraction/
│   │   ├── eip-4337/
│   │   ├── eip-7560/
│   │   └── eip-7702/
│   ├── cross-chain/     # 未来扩展
│   └── scaling/         # 未来扩展
├── synthesis/           # 演进/综合分析（按主题组织）
│   ├── aa-eip-evolution/
│   └── cross-chain-evolution/  # 未来扩展
└── domains/             # 主题域定义（按问题空间组织）
    ├── account-abstraction/
    └── cross-chain-interoperability/  # 未来扩展
```

## 研究层级

它们共同构成技术分析主链：

```
primitive（底层机制） → synthesis（演进关系） → domain（问题域）
```

## 各层职责

### primitives（底层机制）

- **职责**：单一对象的技术实现细节
- **组织方式**：按**技术领域**分组（如 `account-abstraction/`、`cross-chain/`）
- **交付物**：`artifact.md`
- **查看**：[primitives/README.md](primitives/README.md)

### synthesis（演进/综合分析）

- **职责**：多个对象之间的关系和发展脉络
- **组织方式**：按**研究主题**组织（如 `aa-eip-evolution`）
- **交付物**：`artifact.md` + 演进图
- **查看**：[synthesis/README.md](synthesis/README.md)

### domains（主题域）

- **职责**：问题空间的划分和边界
- **组织方式**：按**问题空间**组织（如 `account-abstraction`）
- **交付物**：`artifact.md`（域定义）
- **查看**：[domains/README.md](domains/README.md)

## 长期保留的文件

这里默认长期保留：

- `artifact.md`：所有类型的稳定分析结果
- `dependencies.md`（仅 `synthesis / domain` 需要时保留）

这里不放：

- `request.md`
- `plan.md`
- `evidence-matrix.md`
- case 级 `README.md`
- 其他只服务当前一轮研究纠偏的过程文件

这些过程文件应进入 `openspec/changes/<change-name>/`。

术语层默认并入 `artifact.md` 的"关键术语"区。
