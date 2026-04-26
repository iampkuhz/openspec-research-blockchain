# Request Rules

## 适用文件

`openspec/changes/<id>/request.md`

## 必须包含

- 研究对象类型（primitive / synthesis / decision）
- 研究路径（deep-dive / evolution / scenario）
- 3-5 个开放性核心问题
- 范围边界（覆盖对象、协议、时间窗口）
- 非目标
- 已知输入
- 预期输出
- 触发原因

## 不应包含

- 分析正文
- 结论
- 来源详细规划（属于 plan.md）
- 图表内容

## 质量标准

- 核心问题必须是开放性问题，不是 Yes/No 问题
- primitive 类型必须覆盖定义层和范围/边界层问题
- 问题层次与对象类型匹配

## Traceability 要求

- 已知输入中如有现有 knowledge 依赖，必须记录路径

## 推荐 Validator

- `required_files`（base）：检查 request.md 存在
- `markdown_sections`（base）：检查必要章节
- `process_file`（pre_commit）：检查最小字段

## 失败处理

- 阻塞进入 plan 阶段
- 返回缺失章节清单
