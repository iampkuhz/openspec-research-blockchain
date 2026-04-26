# 发布计划

## 发布目标

| 来源 | 目标 | 类型 | Operation |
|---|---|---|---|
| draft.md | knowledge/.../artifact.md | knowledge_source_note / knowledge_primitive / knowledge_synthesis / knowledge_decision | create / update |

## Decision Verdict 映射

<!-- 仅 decision 需要生成 verdict.md 时填写。 -->

| 来源章节 | 目标 | 类型 | 模板 |
|---|---|---|---|
| draft.md#Verdict 草稿 | knowledge/decisions/.../verdict.md | knowledge_decision_verdict | decision-verdict.md |

## 最终模板

| 目标类型 | 模板 |
|---|---|
| knowledge/**/artifact.md | knowledge-artifact.md |
| knowledge/decisions/**/verdict.md | decision-verdict.md |

## 合并/替换策略

<!-- 说明是新增、覆盖、合并还是更新局部章节。 -->

## 前置条件

- [ ] review 已完成或明确豁免
- [ ] validation 已通过或问题已记录
- [ ] publish target 路径合法
- [ ] traceability 完整
- [ ] decision verdict 如存在，已关联 decision-criteria.md

## 发布后检查

- [ ] Knowledge 文件存在
- [ ] Knowledge registry 如需更新已更新
- [ ] 关联关系已记录
