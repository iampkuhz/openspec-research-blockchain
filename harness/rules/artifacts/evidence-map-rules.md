# Evidence Map Rules

## 适用文件

`openspec/changes/<id>/sources/evidence-map.md`

## 必须包含

- 来源 → 主张（claim）的映射表
- 证据等级（L1/L2/L3/L4）
- 覆盖度分析

## 不应包含

- 分析正文
- 独立的新主张（必须有来源支撑）

## 质量标准

- 每个核心 claim 至少有一个 L1 或 L2 来源支撑
- 只有 L3/L4 支撑的 claim 必须标注低置信度
- 覆盖度分析覆盖 plan 中声明的所有核心问题

## Traceability 要求

- 每条映射保留来源 ID 和主张摘要

## 推荐 Validator

- `evidence_map`（profile）：检查证据映射完整性

## 失败处理

- 阻塞进入 draft 阶段
- 返回未覆盖的 claim 清单
