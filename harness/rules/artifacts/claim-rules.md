# Claim Rules

## 适用文件

`openspec/changes/<id>/claims/*.md`

## 必须包含

- 主张正文
- 支撑来源（至少一个）
- 证据等级（L1/L2/L3/L4）

## 不应包含

- 无来源支撑的新主张
- 推测性结论

## 质量标准

- 核心主张优先使用 L1/L2 来源
- 只有 L3/L4 支撑的主张必须标注低置信度
- 主张之间不自相矛盾

## Traceability 要求

- 每个 claim 可追溯到 source-pack 中的来源

## 推荐 Validator

- `traceability`（manual）：检查来源追溯

## 失败处理

- 返回无来源支撑的 claim 清单
