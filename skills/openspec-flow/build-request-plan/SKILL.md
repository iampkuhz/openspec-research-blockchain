---
name: openspec-build-request-plan
description: 当 change 目录已创建或即将创建，需要生成 request.md 定义研究目标与范围边界，并基于已确认的 request 生成 plan.md 执行计划时使用。
---

# 生成研究请求与计划

## 规则来源

本 skill 执行 request 与 plan 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml` —— change 整体结构
- `openspec/schemas/blockchain-research/templates/request.md` —— request 模板
- `openspec/schemas/blockchain-research/templates/plan.md` —— plan 模板
- `harness/workflows/request-phase.md` —— request 阶段规范
- `harness/workflows/plan-phase.md` —— plan 阶段规范
- 相关上位规范（见上述阶段规范中"与上位规范的关系"）

本 skill 不复制上位规范正文，仅负责触发入口、使用时机与输入输出。

若阶段规范与其引用的上位规范存在差异，以上位规范为准。

## 何时使用

- 研究意图已萌芽，需要明确研究目标与范围边界
- change 目录已创建或即将创建，需要生成 `request.md` 作为研究起点
- `request.md` 已经写好，需要把问题收紧为可执行计划
- 需要一次性生成研究请求、预算、来源规划、证据缺口与完成标准

## 输入输出

**输入：**
- 目标 change 目录路径
- 用户提供的研究背景、触发原因、初步想法（如 request 尚未存在）

**输出：**
- `request.md`（如不存在或需更新）
- `plan.md`（如不存在或需更新）
- 如确有必要，补 `decision-criteria.md`（仅 decision 类型）

## 上下文不足时的补问规则

如用户未提供足够上下文，按 `request-phase.md` 补齐 request 所需关键信息：

- 研究对象类型
- 研究路径
- 核心问题
- 触发原因
- 范围边界
- 已知输入

request 完成后应能直接支撑后续 plan 生成。

## 执行顺序

1. 如 `request.md` 不存在或不完整，先生成/修订 request
2. 如 `plan.md` 不存在或不完整，基于已确认的 request 生成 plan
3. 如研究类型为 decision 类型，生成 `decision-criteria.md`

## 禁止事项

- 不得跳过 request 直接写 plan
- 不得在没有明确研究问题时生成 plan
- 不得引用 `work-products/*.md`
- 不得跳过类型判断直接创建 change

## 自检

- request 是否包含对象类型、研究路径、核心问题、触发原因、范围边界？
- plan 是否包含问题拆解、待确认问题、交付范围、来源规划、证据缺口、完成标准？
- 研究类型是否与 `schema.yaml` 中定义的 profile 一致？
