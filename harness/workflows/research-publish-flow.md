# Research Publish Flow — `/spec-research-publish` 执行规约

**对应 Command**：`/spec-research-publish`
**输出**：`publish.md`、`knowledge/**/artifact.md`、`knowledge/decisions/**/verdict.md`

---

## 执行逻辑

### 步骤 1：检查 draft.md

确认 `draft.md` 存在且包含必要章节：
- 概述、术语表、分析正文、能力边界、参考资料
- candidate type 已声明
- target knowledge path 已声明

### 步骤 2：检查 review.md

确认 `review.md` 存在且评审结论为 approved 或 approved with minor fixes。
如 review 未通过，拒绝 publish。

### 步骤 3：生成或检查 publish.md

publish.md 必须定义：
- draft.md → knowledge/** 的 from/to 映射
- 每个目标文件的 type（artifact / verdict）
- traceability 保留说明

### 步骤 4：校验 publish_targets

检查 `change.yaml` 中声明的 publish_targets：
- from 文件存在
- to 路径合法
- type 正确（artifact / verdict）

### 步骤 5：生成 knowledge artifact

使用 `knowledge-artifact.md` 模板（或 `openspec/schemas/blockchain-research/templates/knowledge-artifact.md`）生成：
- 提炼 durable 内容，移除过程性痕迹
- 保留核心术语、分析正文、设计取舍、能力边界
- 保留 traceability 引用
- 参考资料简化为两列（来源 | 说明）

### 步骤 6：生成 decision verdict（如适用）

使用 `decision-verdict.md` 模板生成 `verdict.md`：
- 追溯到 `decision-criteria.md`
- 追溯到 `draft.md#Decision Analysis / Verdict Draft`
- 输出条件性结论

### 步骤 7：写入 knowledge/**

写入路径：

| task_type | 路径 |
|---|---|
| source_reading | `knowledge/analysis/source-notes/**/artifact.md` |
| primitive | `knowledge/analysis/primitives/**/artifact.md` |
| synthesis | `knowledge/analysis/synthesis/**/artifact.md` |
| decision | `knowledge/decisions/**/artifact.md` + `knowledge/decisions/**/verdict.md` |

---

## 核心约束

1. **publish.md 是唯一发布边界**：只有通过 publish.md 声明的目标才能写入 knowledge/**
2. **draft.md 不能被直接复制为 final artifact**：必须经过提炼，移除过程性痕迹
3. **decision verdict 必须追溯**：`decision-criteria.md` → `draft.md#Decision Analysis / Verdict Draft` → `decision-verdict.md` → `verdict.md`
4. **不得绕过 review**：无 review.md 或 review 不通过时拒绝 publish
5. **traceability 保留**：draft 中的 source 引用必须在 artifact 中保留

---

## 完成后

- 知识资产已沉淀到 knowledge/**
- change 目录可归档到 `openspec/archive/`
- 如需更新已有 knowledge，走 update 场景的 impact scan
