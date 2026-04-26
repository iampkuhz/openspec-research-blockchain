---
name: route-research-change
description: 用于判断研究需求属于 primitive / synthesis / decision 中的哪一种，并路由到对应的 profile 与 change 初始化流程。
---

# 路由研究需求

## 适用场景

- 用户给出自然语言研究需求，需要判断属于哪种研究类型。
- 需要为 change 选择正确的 profile（`primitive` / `synthesis` / `decision`）。
- 复杂需求需要拆成多个 child changes 时，确定拆分策略。

## 输入

- 用户研究需求的自然语言描述。

## 输出

- 确定的 `research_type`（`primitive` / `synthesis` / `decision`）。
- 对应的 `change.yaml` 中的 `profile` 与 `operation` 值。
- 如需拆分，给出 change graph 建议。

## 读取文件

- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/schemas/blockchain-research/profiles/*.schema.yaml`
- 已有的 `openspec/changes/` 目录，避免重复创建。

## 写入文件

不直接写入文件，仅输出路由判断结果。由 `init-change` skill 负责写入。

## 禁止事项

- 不得跳过类型判断直接创建 change。
- 不得将单一复杂需求硬塞进一个 change。
- 不得引用 `work-products/*.md`。

## 自检

- 研究类型是否与 `schema.yaml` 中定义的 profile 一致？
- 如果拆分为多个 changes，每个 change 是否对应一个独立 publish target？
