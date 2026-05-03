# Draft Rules

## 适用文件

`openspec/changes/<id>/draft.md`

## 必须包含

- 概述
- 术语表（表格形式：术语、定义、作用）
- 分析正文
- 能力边界
- 参考资料
- Target Knowledge path
- Evidence 与 Traceability
- Candidate type（source_note / primitive / synthesis / decision）

## 不应包含

- work-products/*.md 的任何内容
- 过程性注释和标记
- 原样复制的 request.md / plan.md

## 质量标准

- draft.md 是唯一主候选产物
- candidate type 必须与 change.yaml 中的 task_type 一致
- 每个核心 claim 可追溯到 source
- evidence 不足时必须明确写不确定性
- 结论只能是 bounded conclusions
- decision 类型必须包含 Decision Analysis 与 Verdict Draft
- 不得保留 `[TODO: diag-*]`、`TODO diagram`、`待补图` 等图表占位
- plan 声明的正式 PlantUML 图表必须已由 `diagrams/<diagram-id>/` package 支撑；fallback 图表必须在 draft 中完成并说明降级理由

## Traceability 要求

- 每个核心主张有来源引用
- 来源引用格式：`[L1: 来源名称]`
- 证据缺口明确列出

## 推荐 Validator

- `markdown_sections`（base）：检查必要章节
- `draft_diagram_contract`（post_tool_use）：检查 diagram contract
- `document_structure`（post_tool_use）：检查 Markdown 结构
- `traceability`（manual）：检查可追溯性

## 失败处理

- 阻塞进入 review 阶段
- 返回缺失章节和 traceability gap 清单
- 图表 TODO、缺少必需正式图表 package 或 diagram contract 校验失败时，阻塞进入 review / publish 阶段
