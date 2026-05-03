# Publish Rules

## 适用文件

`openspec/changes/<id>/publish.md`

## 必须包含

- draft.md → knowledge/** 的 from/to 映射
- 每个目标文件的 type（artifact / verdict）
- traceability 保留说明
- decision verdict 必须定义 draft.md#Verdict Draft → knowledge/decisions/**/verdict.md

## 不应包含

- 绕过 review 的发布
- 未在 change.yaml 中声明的 publish_targets

## 质量标准

- publish.md 是唯一发布边界
- draft.md 不能被直接复制为 final artifact，必须经过提炼
- decision verdict 必须追溯到 decision-criteria.md 和 draft.md 的 Verdict Draft
- 不得绕过 review
- 不得发布含图表 TODO、缺少必需正式图表 package 或 review 中仍有 blocking diagram issue 的 draft
- traceability 从 draft 保留到 artifact

## Traceability 要求

- 每个 publish target 可追溯到 draft.md 的对应章节
- artifact 保留来源引用（简化格式）

## 推荐 Validator

- `publish_targets`（operation）：检查发布目标合法性
- `traceability`（pre_publish）：检查可追溯性保留

## 失败处理

- 阻塞写入 knowledge/**
- 返回不合法的 publish target
- 要求补全 traceability
- 要求先补齐 diagram gate 或显式记录合法 fallback 降级
