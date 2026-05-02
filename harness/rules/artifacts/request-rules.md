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
- 切断来源验证的自我设限表述

## 质量标准

- 核心问题必须是开放性问题，不是 Yes/No 问题
- primitive 类型必须覆盖定义层和范围/边界层问题
- 问题层次与对象类型匹配

## 二次研究来源保护

当 `request.md` 引用既有 artifact、旧 change、旧分析或用户提供的二手总结时：

- 既有 artifact 只能作为参考基线，不得作为事实终点。
- "非目标"中不得出现"不扩展研究新来源"、"不引入新外部来源"、"基于既有分析已确认的事实"等切断来源搜索或回源验证的表述。
- request 必须说明仍需回源到原始项目仓库、官方文档、规范、release notes、commit history 或其他 L1 / L2 来源进行验证和补充。
- 如发现已有 request 包含此类自我设限表述，必须先修正 request，再进入 plan 或 sources 阶段。

## Traceability 要求

- 已知输入中如有现有 knowledge 依赖，必须记录路径

## 推荐 Validator

- `required_files`（base）：检查 request.md 存在
- `markdown_sections`（base）：检查必要章节
- `process_file`（pre_commit）：检查最小字段

## 失败处理

- 阻塞进入 plan 阶段
- 返回缺失章节清单
