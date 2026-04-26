---
name: review-research-system
description: 审查 OpenSpec 合约、command 路由与 Harness 规则的一致性，输出治理报告与修复建议。
---

# 审查研究系统一致性

## 适用场景

- schema 新增或修改字段、类型、模板后，需要检查引用链是否完整
- 新增、删除或重命名 command 后，需要检查引用链是否完整
- Harness workflow/rule 新增或修改后，需要检查引用链是否完整
- 发现 profile、operation、artifact 模型之间存在不一致

## 输入

- `openspec/schemas/`、`openspec/specs/`、`openspec/config.yaml`
- `.claude/commands/` 目录
- `harness/workflows/` 与 `harness/rules/` 目录
- `harness/workflows/_index.yaml`、`harness/rules/_phase_index.yaml`

## 输出

- 治理问题清单（不一致的引用、缺失的模板、schema 冲突、死引用、缺失 skill、command 与 workflow 不一致）
- 修复建议

## 读取文件

- `openspec/schemas/blockchain-research/schema.yaml` 及 profiles/operations/templates
- `openspec/config.yaml` 与 `openspec/specs/` 下的规约文件
- `.claude/commands/*.md` 与 `skills/*/SKILL.md`
- `harness/workflows/_index.yaml`、`harness/rules/_phase_index.yaml`、`harness/rules/_index.yaml`
- 涉及的 workflow 与 rule 叶子文件

## 写入文件

- 治理评审报告（由调用方决定写入位置）

## 禁止事项

- 不得直接修改 openspec / harness 正文，只输出审查报告与修复建议
- 不得直接删除 command 文件，只输出审查报告与修复建议

## 自检

- 所有 schema 中的 template 路径是否都有对应文件？
- 每个 command 引用的 skill 路径是否可解析？
- 所有 workflow 引用的 rule 路径是否存在？
- profile 与 operation 的引用是否形成闭环？
