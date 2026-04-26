# Plan Rules

## 适用文件

`openspec/changes/<id>/plan.md`

## 必须包含

- 研究深度声明（deep / focused / light）
- 来源分层规划（L1/L2/L3/L4）
- 图表规划（每张图的必要性：必须/可选/推荐）
- 证据缺口
- 完成标准
- 待确认问题
- 依赖声明（synthesis/decision 类型必需）

## 不应包含

- 分析正文
- 正式结论
- 图表正文

## 质量标准

- 来源必须按 L1/L2/L3/L4 分层
- 每条来源附可点击链接或 `[待补链接：原因]`
- synthesis/decision 类型必须对每个依赖 primitive 声明所需深度
- 来源规划表包含"验证状态"列

## Traceability 要求

- 依赖的现有 primitive/synthesis 必须记录路径
- 缺失的依赖必须在 plan 中规划补充

## 推荐 Validator

- `required_files`（base）：检查 plan.md 存在
- `markdown_sections`（base）：检查必要章节

## 失败处理

- 阻塞进入 sources / draft 阶段
- 返回缺失章节和依赖缺口清单
