---
name: build-research-support
description: 为当前 change 生成研究支撑材料（来源包、证据地图、笔记、claims），作为 draft 的前置输入。
---

# 生成长期研究资产

## 规则来源

本 skill 执行端到端 research pipeline 规则，正式流程来自：

- `harness/workflows/research-pipeline.md` —— 端到端流程真源
- 各阶段 OpenSpec spec 与模板（见 research-pipeline.md 中"阶段定义"）

本 skill 不复制阶段正式规则正文，仅负责 Qoder 的触发入口、使用时机与输入输出。

若 pipeline 引用的规范存在差异，以相关上位规范为准。

## 何时使用（Qoder 特定）

- 需要端到端完成一个 research change
- 研究意图已萌芽，需要从 request 开始完整执行
- 已有部分阶段文件，需要增量补全至 artifact

## 输入输出（Qoder 特定）

**输入：**
- 目标 change 目录路径
- 用户提供的研究背景、触发原因、初步想法（如 request 尚未存在）

**输出：**
- `request.md`（如不存在或需增量更新）
- `plan.md`（如不存在或需增量更新）
- `draft.md`（如不存在或需增量更新）
- `review/`（如不存在或需增量补齐）
- `knowledge/analysis/.../artifact.md` 或 `knowledge/decisions/.../artifact.md`

## 执行模式

**默认模式：命令层驱动的连续执行**

- 按顺序执行 request / plan / draft / review / artifact
- 如某阶段文件已存在且内容完整，自动跳过该阶段
- 如某阶段文件存在但不完整，自动增量修订

**跳过规则**：
- request：已包含对象类型、研究路径、核心问题、触发原因、范围边界、已知输入、预期输出 → 跳过
- plan：已包含研究对象、问题拆解、待确认问题、交付范围、研究深度、来源规划、证据缺口、完成标准 → 跳过
- draft：已包含概述、术语表、组件架构、核心流程、设计取舍、能力边界、相关协议对比、结论、待确认问题、参考资料 → 跳过
- review：如 `review-summary.md` 不存在或结论过期，则补齐
- artifact：不跳过（必须执行，除非用户显式指定）

request 完成后应能直接支撑后续 plan 生成，plan 完成后应能直接支撑 draft 生成，以此类推。
