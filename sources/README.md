# sources/ — 原始资料库

本目录存放长期保留、不可变、只读的原始研究资料（raw sources）。

**与 change sources 的区别**：

| 目录 | 定位 | 生命周期 |
|------|------|----------|
| `sources/`（本目录） | 长期原始资料库，作为知识编译的 source of truth | 永久保留，不随 change 归档而删除 |
| `openspec/changes/<id>/sources/` | 特定研究任务的临时来源包 | 随 change 归档而移至 `openspec/archive/` |

**关系**：
- `sources/` 中的文件是原始资料，不可修改
- `knowledge/` 中的内容是编译产物，随研究演进
- `openspec/changes/` 中的来源包是特定任务的快照

---

## 现有资料

| 文件 | 类型 | 说明 |
|------|------|------|
| `tendermint-paper.pdf` | PDF | Tendermint 共识算法论文 |

## 如何新增资料

1. 将原始文件放入 `sources/` 或其子目录
2. 在本 README 的"现有资料"表中登记
3. 文件一旦放入即视为不可变（immutable）
