---
name: review-hook-coverage
description: 审查 scripts/hooks/ 中的 hook 脚本是否覆盖了 openspec change 的关键生命周期。
---

# 审查 Hook 覆盖

## 适用场景

- 新增 change profile、operation 或 artifact 类型后，需要确认 hook 覆盖是否完整。
- 需要检查 hook validator 是否对所有合法 change 结构生效。

## 输入

- `scripts/hooks/` 目录。
- `openspec/schemas/blockchain-research/` schema 文件。

## 输出

- Hook 覆盖分析报告（已覆盖/未覆盖的生命阶段、缺失的 validator）。
- 修复建议。

## 读取文件

- `scripts/hooks/` 下的所有脚本。
- `openspec/schemas/blockchain-research/schema.yaml`。
- `openspec/schemas/blockchain-research/profiles/*.schema.yaml`。
- `openspec/schemas/blockchain-research/operations/*.schema.yaml`。

## 写入文件

- 治理评审报告（由调用方决定写入位置）。

## 禁止事项

- 不得直接修改 hook 脚本，只输出审查报告与修复建议。

## 自检

- 每个 profile 是否有对应的 hook validator？
- 新增的 artifact 类型是否被现有 hook 覆盖？
