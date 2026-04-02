# Knowledge Glossary Meta

本目录包含术语分类和关系的元数据定义。

## 文件说明

| 文件 | 用途 |
|------|------|
| [`concept-categories.yaml`](./concept-categories.yaml) | 概念分类定义 |
| [`layer-taxonomy.yaml`](./layer-taxonomy.yaml) | 层次分类定义 |
| [`relation-types.yaml`](./relation-types.yaml) | 关系类型定义 |
| [`evidence-status.yaml`](./evidence-status.yaml) | 证据状态定义 |

## 使用方法

这些元数据文件用于：

1. **术语注册** - 新术语必须声明 category 和 layer
2. **一致性检查** - 脚本验证术语使用是否符合 taxonomy
3. **知识索引** - 按 category/layer 组织术语

## 扩展

如需新增 category 或 relation type，修改对应 YAML 文件并提交 change。
