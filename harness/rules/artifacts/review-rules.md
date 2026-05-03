# Review Rules

## 适用文件

`openspec/changes/<id>/review.md`

## 必须包含

- 评审结论（approved / approved with minor fixes / needs revision）
- high severity 问题清单
- 修复建议或必须修复项

## 不应包含

- 重写 draft.md 正文（除非任务明确要求修复）
- 新的分析内容

## 质量标准

- 评审独立于 draft 作者
- high severity 问题必须可定位到 draft.md 的具体位置
- 评审结论与问题清单一致
- 如无 high severity 问题，结论不得是 needs revision
- plan 要求的正式图表缺失、`diagrams/` package 为空、diagram contract 校验失败或 draft 仍含图表 TODO 时，必须列为 high severity / blocking issue
- 存在 blocking diagram issue 时，评审结论不得为 approved 或 approved with minor fixes

## Traceability 要求

- 每个评审问题可追溯到 draft.md 的位置

## 推荐 Validator

- `markdown_sections`（base）：检查必要章节
- `document_structure`（post_tool_use）：检查结构

## 失败处理

- 如 needs revision：返回 draft 修复，不进入 publish
- 如缺少评审结论：阻塞进入 publish
- 如存在 blocking diagram issue：返回 diagram / draft 修复，不进入 publish
