---
name: extract-claims
description: 从来源笔记与研究笔记中提取可追溯的 claims，生成 claims/<claim-slug>.md。
---

# 提取研究声明

## 适用场景

- 来源笔记已完成，需要提炼为结构化 claims。
- 每个 claim 需要可追溯到具体来源。

## 输入

- `sources/notes/*.md` 来源笔记。
- `sources/evidence-map.md`。

## 输出

- `sources/claims/<claim-slug>.md`（一个文件对应一个 claim）。

## 读取文件

- `sources/notes/*.md`。
- `sources/evidence-map.md`。

## 写入文件

- `openspec/changes/<change-id>/sources/claims/<claim-slug>.md`

## 禁止事项

- 每个 claim 必须有明确来源引用，不得凭空生成。
- 不得将多个独立 claims 合并为一个。

## 自检

- 每个 claim 是否指向至少一个具体来源？
- claim 的表述是否足够精确、可被独立验证或反驳？
