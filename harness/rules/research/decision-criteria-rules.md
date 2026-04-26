# Decision Criteria Rules

## 适用文件

`openspec/changes/<id>/decision-criteria.md`（可选）

## 用途

定义决策分析的标准维度，作为 decision workflow 的输入。

## 必须包含

- 决策维度列表
- 每个维度的权重或优先级
- 评判标准（什么算好、什么算差）

## 与 draft 的关系

- `decision-criteria.md` → `draft.md#Decision Analysis / Verdict Draft` → `decision-verdict.md` → `knowledge/decisions/**/verdict.md`
- 决策分析必须按 criteria 中声明的维度逐项判断
- 不得在分析过程中临时增加未在 criteria 中声明的维度

## 可选性

- decision-criteria.md 是可选文件
- 如未声明，draft.md 中必须内联定义决策标准
- 如已声明，决策分析必须引用 criteria 文件的维度
