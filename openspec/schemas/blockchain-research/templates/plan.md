# Plan

## 摘要

<!-- 摘要 request.md 中的目标和边界。 -->

## 计划

## 任务类型

- task_type:
- change_operation:
- execution_scope:

## Artifact 计划

| Artifact | 是否必填 | 路径 | 用途 |
|---|---:|---|---|
| request | 必填 | request.md | 需求说明 |
| plan | 必填 | plan.md | 执行计划 |
| source_pack | 必填 | sources/source-pack.md | 来源清单 |
| evidence_map | 可选 | sources/evidence-map.md | 证据映射 |
| note | 可选 | notes/*.md | source 级别摘要 |
| claim | 可选 | claims/*.md | 可验证主张 |
| draft | 必填 | draft.md | 唯一主候选产物 |
| review | 可选 | review.md | 语义审查 |
| publish | 可选 | publish.md | 发布映射 |

## Evidence 策略

<!-- 说明需要哪些 source，哪些 source 需要升级为 note。 -->

## Draft 目标

- Draft 路径: draft.md
- 目标 Knowledge 路径:

## 子 Change

<!-- 如果任务复杂，列出需要先完成的 child changes。当前 change 不得产出多个主候选产物。 -->

## 校验计划

<!-- 每个阶段需要哪些自动校验。 -->

## 执行顺序

```text
request.md -> plan.md -> source-pack.md -> evidence-map.md -> notes* -> claims* -> draft.md -> review.md -> publish.md -> knowledge/**
```
