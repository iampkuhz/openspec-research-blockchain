---
name: review-openspec-contracts
description: 审查 openspec/schemas、openspec/specs、openspec/config.yaml 之间的一致性与引用完整性。
---

# 审查 OpenSpec 合约

## 适用场景

- schema 新增或修改字段、类型、模板后，需要检查引用链是否完整。
- 发现 profile、operation、artifact 模型之间存在不一致。

## 输入

- `openspec/schemas/` 目录。
- `openspec/specs/` 目录。
- `openspec/config.yaml`。

## 输出

- 治理问题清单（不一致的引用、缺失的模板、schema 冲突）。
- 修复建议。

## 读取文件

- `openspec/schemas/blockchain-research/schema.yaml`。
- `openspec/schemas/blockchain-research/profiles/*.schema.yaml`。
- `openspec/schemas/blockchain-research/operations/*.schema.yaml`。
- `openspec/schemas/blockchain-research/templates/*.md`。
- `openspec/config.yaml`。
- `openspec/specs/` 下的规约文件。

## 写入文件

- 治理评审报告（由调用方决定写入位置）。

## 禁止事项

- 不得直接修改 openspec 正文，只输出审查报告与修复建议。

## 自检

- 所有 schema 中的 template 路径是否都有对应文件？
- profile 与 operation 的引用是否形成闭环？
