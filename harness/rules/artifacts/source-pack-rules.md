# Source Pack Rules

## 适用文件

`openspec/changes/<id>/sources/source-pack.md`

## 必须包含

- 来源清单（URL、类型、分层 L1-L4、验证状态）
- 来源质量评估
- 证据缺口

## 不应包含

- 分析正文
- 正式结论

## 质量标准

- 每个来源必须可访问或说明不可访问原因
- L1/L2 来源优先覆盖核心技术主张
- L3/L4 来源明确标注置信度

## Traceability 要求

- 每个来源记录 URL 和本地归档路径

## 推荐 Validator

- `source_pack`（profile）：检查来源元信息和清单

## 失败处理

- 阻塞进入 draft 阶段
- 返回证据缺口清单
