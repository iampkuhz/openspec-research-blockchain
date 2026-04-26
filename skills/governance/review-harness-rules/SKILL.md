---
name: review-harness-rules
description: 审查 harness/rules/ 与 harness/workflows/ 之间的一致性与引用完整性。
---

# 审查 Harness 规则

## 适用场景

- Harness workflow/rule 新增或修改后，需要检查引用链是否完整。
- 发现 workflow 引用的 rule 文件不存在或已移动。

## 输入

- `harness/workflows/` 目录。
- `harness/rules/` 目录。
- `harness/workflows/_index.yaml`。
- `harness/rules/_phase_index.yaml`。
- `harness/rules/_index.yaml`。

## 输出

- 一致性审查报告（死引用、缺失规则、阶段索引不同步）。
- 修复建议。

## 读取文件

- `harness/workflows/_index.yaml`。
- `harness/rules/_phase_index.yaml`。
- `harness/rules/_index.yaml`。
- 涉及的 workflow 与 rule 叶子文件。

## 写入文件

- 治理评审报告（由调用方决定写入位置）。

## 禁止事项

- 不得直接修改 harness 文件，只输出审查报告与修复建议。

## 自检

- 所有 workflow 引用的 rule 路径是否存在？
- 阶段索引文件是否与叶子文件同步？
