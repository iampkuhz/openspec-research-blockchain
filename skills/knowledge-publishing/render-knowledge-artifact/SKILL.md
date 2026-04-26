---
name: render-knowledge-artifact
description: 用于把稳定的 draft.md 结果提炼进长期 artifact 目录，适合一轮研究完成后整理长期资产时使用。
---

# 生成长期 artifact

## 规则来源

本 skill 执行 artifact 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml` —— change 整体结构
- `harness/workflows/artifact-phase.md` —— artifact 阶段规范（入口）
- `openspec/specs/canonical-output-model/spec.md` —— 长期资产结构
- 相关上位规范（见 `artifact-phase.md` 中"与上位规范的关系"）

本 skill 不复制上位规范正文，仅负责 Qoder 的触发入口、使用时机与输入输出。

若 `artifact-phase.md` 与其引用的上位规范存在差异，以相关上位规范为准。

## 何时使用（Qoder 特定）

- change packet 已经完成本轮研究
- `draft.md` 已稳定且通过 review
- 需要把长期值得保留的内容提炼进 `knowledge/` 目录

## 输入输出（Qoder 特定）

**输入：**
- 目标 change 目录路径

**输出：**
- `knowledge/analysis/.../artifact.md`（primitive / synthesis 类型）
- `knowledge/decisions/.../artifact.md` + `verdict.md`（decision 类型）

## 适用的长期目录范围

- `knowledge/analysis/primitives/` —— primitive 类型
- `knowledge/analysis/synthesis/` —— synthesis 类型
- `knowledge/decisions/` —— decision 类型
