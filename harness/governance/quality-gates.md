# 质量门禁定义

**本文件位置**：`harness/governance/quality-gates.md`
**用途**：定义研究流程中各阶段的质量门禁（gate），每个 gate 说明输入文件、检查项、推荐 validator、失败处理。

---

## Gate 总览

```
request.md → post-request gate
  → plan.md → post-plan gate
    → sources/ + notes/ + claims/ → post-research gate
      → draft.md → post-draft gate
        → review.md → post-review gate
          → publish.md → pre-publish gate
            → knowledge/** → post-publish gate
```

---

## post-request gate

**输入文件**：`openspec/changes/<id>/request.md`、`openspec/changes/<id>/change.yaml`

**检查项**：
1. request.md 包含必要章节（研究对象类型、研究路径、核心问题、范围边界、预期输出、触发原因）
2. change.yaml 已声明 task_type（source_reading / primitive / synthesis / decision）
3. change.yaml 已声明 change_operation
4. target knowledge path 草案已定义

**推荐 validator**：
- `required_files`（base）：检查 request.md 存在
- `markdown_sections`（base）：检查必要章节
- `process_file`（pre_commit）：检查最小字段

**失败处理**：
- 阻塞进入 plan 阶段
- 返回缺失章节清单
- 不生成 plan.md

---

## post-plan gate

**输入文件**：`openspec/changes/<id>/plan.md`、`openspec/changes/<id>/change.yaml`

**检查项**：
1. plan.md 包含必要章节（研究深度、来源规划、图表规划、证据缺口、完成标准）
2. child changes 已声明（如适用）
3. source strategy 已定义（来源分层计划）
4. draft target path 已定义

**推荐 validator**：
- `required_files`（base）：检查 plan.md 存在
- `markdown_sections`（base）：检查必要章节

**失败处理**：
- 阻塞进入 sources / draft 阶段
- 返回缺失章节清单
- 不生成 sources/ 或 draft.md

---

## post-research gate

**输入文件**：`openspec/changes/<id>/sources/source-pack.md`、`openspec/changes/<id>/sources/evidence-map.md`、`notes/*.md`、`claims/*.md`

**检查项**：
1. source-pack.md 存在且包含来源清单
2. evidence-map.md 存在且包含来源→主张的映射
3. plan 中声明的每个来源至少有 L1/L2 覆盖
4. notes/*.md 已消化 plan 中声明的核心来源
5. claims/*.md 已提取关键主张（如 plan 要求）

**推荐 validator**：
- `source_pack`（profile）：检查来源元信息
- `evidence_map`（profile）：检查证据映射

**失败处理**：
- 阻塞进入 draft 阶段
- 返回证据缺口清单
- 不生成 draft.md

---

## post-draft gate

**输入文件**：`openspec/changes/<id>/draft.md`

**检查项**：
1. draft.md 存在且包含必要章节（概述、术语表、分析正文、能力边界、参考资料）
2. traceability：每个核心 claim 可追溯到 source
3. target knowledge path 已定义
4. candidate type 已声明（source_note / primitive / synthesis / decision）
5. decision 类型必须包含 Decision Analysis 与 Verdict Draft
6. 图表 contract 已验证（如包含 PlantUML）

**推荐 validator**：
- `markdown_sections`（base）：检查必要章节
- `draft_diagram_contract`（post_tool_use）：检查 diagram contract
- `document_structure`（post_tool_use）：检查 Markdown 结构
- `traceability`（manual）：检查可追溯性

**失败处理**：
- 阻塞进入 review 阶段
- 返回缺失章节和 traceability gap
- 不生成 review.md

---

## post-review gate

**输入文件**：`openspec/changes/<id>/draft.md`、`openspec/changes/<id>/review.md`

**检查项**：
1. review.md 存在且包含评审结论
2. high severity 问题已清零
3. 评审结论明确（approved / approved with minor fixes / needs revision）
4. 如 needs revision，返回 draft 修复

**推荐 validator**：
- `markdown_sections`（base）：检查 review.md 结构
- `document_structure`（post_tool_use）：检查结构

**失败处理**：
- 如 needs revision：返回 draft 修复，不进入 publish
- 如 approved with minor fixes：确认修复后进入 publish
- 如 approved：进入 pre-publish gate

---

## pre-publish gate

**输入文件**：`openspec/changes/<id>/publish.md`、`openspec/changes/<id>/draft.md`、`openspec/changes/<id>/review.md`、`openspec/changes/<id>/change.yaml`

**检查项**：
1. publish.md 已定义 draft.md → knowledge/** 的 from/to 映射
2. publish_targets 声明合法（from 文件存在、to 路径合法、type 正确）
3. traceability 保留（draft 中的 source 引用在 artifact 中保留）
4. decision verdict 已映射：draft.md#Verdict Draft → knowledge/decisions/**/verdict.md
5. review 已通过（未绕过）

**推荐 validator**：
- `publish_targets`（operation）：检查发布目标合法性
- `traceability`（pre_publish）：检查可追溯性保留

**失败处理**：
- 阻塞写入 knowledge/**
- 返回不合法的 publish target
- 不生成 publish.md 或 knowledge artifact

---

## post-publish gate

**输入文件**：`knowledge/**/artifact.md`、`knowledge/decisions/**/verdict.md`（如适用）

**检查项**：
1. knowledge 文件已创建在正确路径
2. artifact.md 满足 knowledge artifact contract
3. TOC 覆盖所有一二级标题
4. traceability 从 draft 保留到 artifact
5. knowledge tree 结构满足约束（如 registry 需要更新）

**推荐 validator**：
- `knowledge_artifact`（post_tool_use）：检查 artifact contract
- `knowledge_artifact_toc`（post_tool_use）：检查 TOC 覆盖
- `frontmatter`（pre_commit）：检查 frontmatter（按需开启）
- `knowledge_tree`（pre_commit）：检查目录结构（按需开启）

**失败处理**：
- 阻止 commit（如 pre_commit hook）
- 返回不合法的知识资产
- 需要修复后重新 publish
