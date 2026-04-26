---
name: write-source-reading-draft
description: 基于来源精读笔记，编写以来源为主线的第一版 draft 内容。
---

# 编写来源阅读型草稿

## 适用场景

- 研究以文献/规范阅读为主，需要按来源组织分析。
- 适用 `source_reading` 研究路径。

## 输入

- `sources/notes/*.md` 来源笔记。
- `sources/claims/*.md` 提取的 claims。
- `request.md` / `plan.md`。

## 输出

- `draft.md`（写入当前 change 目录下）。

## 读取文件

- `request.md`、`plan.md`。
- `sources/notes/*.md`、`sources/claims/*.md`。

## 写入文件

- `openspec/changes/<change-id>/draft.md`

## 禁止事项

- 不得跳过来源笔记直接写 draft。
- 不得生成 `work-products/*.md`。

## 自检

- draft 中的每个论点是否对应至少一个来源笔记？
- 术语是否与既有 glossary 一致？
