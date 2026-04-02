# Knowledge Directory

`knowledge/` 目录包含仓库的核心知识资产。

## 结构

```
knowledge/
├── glossary/meta/        # 术语元数据（分类、层次、关系）
├── domains/              # 域知识组织
├── topics/               # 具体主题（primitive / synthesis）
├── indexes/              # 索引文件
└── templates/            # 知识模板
```

## 知识类型

### Topics (主题知识)

位于 `knowledge/topics/<domain>/<topic>/`

| 类型 | 描述 | 示例 |
|------|------|------|
| primitive | 单个协议/EIP/机制 | eip-4337, consensus-qbft |
| synthesis | 关系/演进/分类分析 | bft-comparison, aa-evolution |

### Domains (域知识)

位于 `knowledge/domains/<domain>/`

组织特定主题域的知识，如 `account-abstraction`。

### Decisions (决策知识)

位于 `knowledge/decisions/<domain>/<topic>/`

场景驱动的决策分析，如 `chain-comparison`。

## 原子化结构

每个 topic 包含：

```
<topic>/
├── overview.md           # 主题概述
├── atoms/                # 知识原子
│   ├── definition.md
│   ├── prerequisites.md
│   ├── core-mechanism.md
│   ├── module-evolution.md
│   ├── limits-and-assumptions.md
│   └── open-questions.md
├── claims/               # Claims
│   ├── facts.yaml
│   ├── inferences.yaml
│   └── estimates.yaml
├── comparisons/          # 比较分析
├── diagrams/             # 图表
├── sources/              # 来源
├── terms/                # 术语
└── changelog.md          # 变更日志
```

## 证据政策

所有知识主张必须有来源支持：

| 等级 | 来源 | 用途 |
|------|------|------|
| L1 | 官方规范/EIP/白皮书 | 核心技术主张 |
| L2 | 参考实现/官方文档 | 技术主张支持 |
| L3 | 官方博客/Release notes | 背景/动机 |
| L4 | 第三方分析/社区讨论 | 社区观点参考 |

详见：[harness/rules/general/evidence-policy.md](../../harness/rules/general/evidence-policy.md)

## 更新流程

**禁止**直接修改 `knowledge/` 下的主线知识。

**必须**通过 OpenSpec change 流程：

1. 在 `openspec/changes/` 创建 change
2. 完成研究并产出 draft
3. 通过 review 后 merge 到 knowledge

详见：[harness/workflows/merge-workflow.md](../../harness/workflows/merge-workflow.md)

## 模板

使用 `knowledge/templates/` 中的模板创建新知识：

- [topic-template/](./templates/topic-template/) - Topic 完整模板
- [principle-template.md](./templates/principle-template.md) - Principle 模板
- [comparison-template.md](./templates/comparison-template.md) - Comparison 模板

## 索引

- [Topic Index](./indexes/topic-index.md)
- [Concept Index](./indexes/concept-index.md)
- [Diagram Index](./indexes/diagram-index.md)
- [Comparison Index](./indexes/comparison-index.md)

## 术语

术语元数据位于 [glossary/meta/](./glossary/meta/)：

- [Concept Categories](./glossary/meta/concept-categories.yaml)
- [Layer Taxonomy](./glossary/meta/layer-taxonomy.yaml)
- [Relation Types](./glossary/meta/relation-types.yaml)
- [Evidence Status](./glossary/meta/evidence-status.yaml)

具体术语定义在各 topic 的 `terms/` 目录下。
