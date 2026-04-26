---
name: write-source-note
description: 对单个来源做 source digestion，生成 notes/<source-slug>.md 阅读笔记。
---

# 生成来源笔记

## 适用场景

- 已完成来源收集，需要对特定文档/论文/规范做精读笔记。
- 需要从来源中提取与研究问题直接相关的要点。

## 输入

- 单个来源的 URL、文件或摘录内容。
- 当前 change 的研究问题（来自 `request.md` / `plan.md`）。

## 输出

- `sources/notes/<source-slug>.md`（写入当前 change 目录下）。

## 读取文件

- 来源原文（URL、本地文件或 `sources/excerpts/`）。
- `plan.md`（研究范围）。

## 写入文件

- `openspec/changes/<change-id>/sources/notes/<source-slug>.md`

## 禁止事项

- 不得脱离研究问题写泛泛摘要。
- 不得伪造来源中不存在的内容。

## 自检

- 笔记是否明确标注了哪些内容直接支撑研究问题？
- 引用的页码/章节/段落是否可追溯？
