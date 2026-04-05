# Knowledge Directory

`knowledge/` 目录包含仓库的长期知识资产。

---

## 资产模型

**两套长期资产目录**：

| 目录 | 用途 | 产出物 |
|------|------|--------|
| `knowledge/analysis/` | 事实分析资产 | `artifact.md` |
| `knowledge/decisions/` | 场景决策资产 | `artifact.md` + `verdict.md` |

**过程产物不进入 knowledge/**：
- `request.md`、`plan.md`、`draft.md` 等保留在 `openspec/changes/<change-id>/`
- 只有稳定的分析结果提升到 knowledge/

**详情**：`openspec/schemas/blockchain-research/schema.yaml`

---

## 目录结构

```
knowledge/
├── analysis/               # 事实分析资产
│   ├── primitives/         # 底层机制（按领域分组）
│   │   ├── account-abstraction/
│   │   │   ├── eip-4337/
│   │   │   └── eip-7702/
│   │   └── scaling/
│   ├── synthesis/          # 演进/综合分析
│   │   └── aa-eip-evolution/
│   └── domains/            # 主题域定义
│       └── account-abstraction/
├── decisions/              # 场景决策资产
│   └── agentic-payment/
├── glossary/meta/          # 术语元数据
│   ├── concept-categories.yaml
│   ├── layer-taxonomy.yaml
│   └── relation-types.yaml
└── indexes/                # 索引文件
    └── topic-index.md
```

---

## 研究层级

```
primitive（底层机制） → synthesis（演进关系） → domain（问题域）
                                                    ↓
                                               decision（场景应用）
```

### 各层职责

| 层级 | 职责 | 组织方式 | 文件 |
|------|------|----------|------|
| **primitives** | 单一对象的技术实现细节 | 按技术领域分组 | `artifact.md` |
| **synthesis** | 多个对象之间的关系和发展脉络 | 按研究主题组织 | `artifact.md` |
| **domains** | 问题空间的划分和边界 | 按问题空间组织 | `artifact.md` |
| **decisions** | 场景驱动的比较和选型 | 按应用场景组织 | `artifact.md` + `verdict.md` |

---

## 证据政策

| 等级 | 来源 | 用途 |
|------|------|------|
| L1 | 官方规范/EIP/白皮书 | 核心技术主张 |
| L2 | 参考实现/官方文档 | 技术主张支持 |
| L3 | 官方博客/Release notes | 背景/动机 |
| L4 | 第三方分析/社区讨论 | 社区观点参考 |

**详情**：`openspec/specs/evidence-policy/spec.md`

---

## 更新流程

**禁止**直接修改 `knowledge/` 下的主线知识。

**必须**通过 OpenSpec change 流程：

1. 在 `openspec/changes/` 创建 change
2. 完成研究并产出 draft
3. 通过 review 后 apply 到 knowledge

**详情**：`openspec/changes/README.md`

---

## 索引

- [Topic Index](./indexes/topic-index.md)

---

## 术语

术语元数据位于 [glossary/meta/](./glossary/meta/)。

具体术语定义在各 case 的 `artifact.md` 术语区。
