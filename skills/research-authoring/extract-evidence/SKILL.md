---
name: research-extract-evidence
description: 当 plan.md 中的来源规划已确定，需要实际获取来源内容、生成 source-pack.md、evidence-map.md、notes/ 与 claims/ 时使用。
---

# 提取来源与证据

## 适用场景

- change 已有 `plan.md` 中的来源规划，需要实际获取来源
- 来源收集完成后，需要对单个来源做精读笔记
- 来源笔记完成后，需要提炼为结构化 claims
- 需要系统化梳理来源覆盖的证据面与证据缺口

## 输入

- 原始来源的 URL、文件或摘录内容。
- 当前 change 的研究问题（来自 `request.md` / `plan.md`）。

## 输出

- `sources/source-pack.md`（来源包）
- `sources/evidence-map.md`（证据地图）
- `notes/<source-slug>.md`（精读笔记）
- `claims/<claim-slug>.md`（结构化 claims）

## 读取文件

- `plan.md`（研究范围与来源规划）。
- 来源原文（URL、本地文件或 `sources/excerpts/`）。

## 写入文件

- `openspec/changes/<change-id>/sources/` 下的上述输出文件。

## 执行步骤

1. **来源获取**
   - 按 `plan.md` 中的来源规划获取内容
   - 每个来源必须有 `source_id`
   - 标注证据等级（L1/L2/L3/L4）
   - 记录 `accessed_at` 日期
   - 不要把 L3/L4 来源作为技术主张的唯一证据

2. **来源精读（write-source-note）**
   - 对每个来源做精读笔记，提取与研究问题直接相关的要点
   - 明确标注哪些内容直接支撑研究问题
   - 引用的页码/章节/段落可追溯

3. **提取 claims（extract-claims）**
   - 从来源笔记中提取可独立验证的结构化 claims
   - 每个 claim 必须有明确来源引用，不得凭空生成
   - claim 的表述必须足够精确、可被独立验证或反驳
   - 不得将多个独立 claims 合并为一个

4. **生成证据地图（build-evidence-map）**
   - 覆盖 plan 中列出的所有关键问题
   - 标注来源类型与可信度
   - 识别哪些 claims 缺少足够的来源支撑
   - 不得伪造不存在的来源证据

## 禁止事项

- 不得仅保存 URL 而不获取内容
- 不得混用不同证据等级的来源
- 不得脱离研究问题写泛泛摘要
- 不得伪造来源中不存在的内容
- 不得生成 `work-products/*.md`

## 自检

- 所有来源是否已获取内容（不仅 URL）？
- 每个 claim 是否指向至少一个具体来源？
- 证据地图是否覆盖了 plan 中所有关键问题？
- 术语是否与既有 glossary 一致？
