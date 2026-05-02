# Research Step Execution — `/spec-research-step` 执行规约

**对应 Command**：`/spec-research-step`
**输出**：`sources/source-pack.md`、`sources/evidence-map.md`、`notes/*.md`、`claims/*.md`、`draft.md`、`review.md`、`publish.md`、`knowledge/**`

---

## 自动下一步判断

本 command 的核心职责是自动检测当前 change 缺少的产物，并按顺序补全。

```text
if missing sources/source-pack.md:
  → build source-pack

elif missing sources/evidence-map.md:
  → build evidence-map

elif plan requires source digestion and missing notes:
  → build notes/*.md

elif plan requires claims and missing claims:
  → build claims/*.md

elif missing draft.md:
  → build draft.md

elif missing review.md:
  → build review.md

elif review approved and missing publish.md:
  → build publish.md

elif review approved and publish targets not written:
  → publish to knowledge/**

else:
  → report completed
```

## 执行原则

1. **只有 publish 阶段写 knowledge/**：sources / draft / review 只产出 change 目录下的过程产物
2. **不生成 work-products/*.md**：统一使用 draft.md 作为主候选产物
3. **如果发现多个 final artifacts**：停止并建议拆 child changes
4. **按 plan 声明执行**：只做 plan.md 中声明的研究范围和图表规划
5. **publish 必须通过 review gate**：无 `review.md` 或 verdict 不通过时不得写 `knowledge/**`

## 各步产出说明

### build source-pack

产出：`sources/source-pack.md`
- 来源清单（URL、类型、分层、验证状态）
- 来源质量评估
- 证据缺口

### build evidence-map

产出：`sources/evidence-map.md`
- 来源 → 主张（claim）的映射表
- 证据等级（L1/L2/L3/L4）
- 覆盖度分析

### build notes

产出：`notes/*.md`（可多文件）
- 按来源消化核心内容
- 每个 note 对应一个来源或来源组
- 保留 source 引用标记

### build claims

产出：`claims/*.md`（可多文件，如 plan 要求）
- 提取关键主张
- 每个 claim 必须有 source 支撑

### build draft

产出：`draft.md`
- 唯一主候选产物
- 包含必要章节（概述、术语表、分析正文、能力边界、参考资料）
- 声明 candidate type（source_note / primitive / synthesis / decision）
- 声明 target knowledge path
- 包含 Evidence 与 Traceability
- decision 类型必须包含 Decision Analysis 与 Verdict Draft
- **不生成 work-products/*.md**

### build review

产出：`review.md`
- 评审结论（approved / approved with minor fixes / needs revision）
- high severity 问题清单
- 修复建议

### build publish

产出：`publish.md`
- draft → knowledge 的 from/to 映射
- publish target 类型（artifact / verdict）
- traceability 保留说明

### publish to knowledge

产出：
- `knowledge/**/artifact.md`
- `knowledge/decisions/**/verdict.md`（decision 类型）

要求：
- 必须存在 `publish.md`
- 必须符合 `openspec/config.yaml` 与 schema asset model
- 不得从 `request.md` 或 `plan.md` 直接发布

## 完成后进入

- 如 review 不通过 → 返回 draft 修复后重新 review
- 如 publish 完成 → 汇报写入路径
