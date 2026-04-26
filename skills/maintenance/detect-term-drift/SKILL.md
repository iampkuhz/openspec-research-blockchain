---
name: detect-term-drift
description: 检测术语漂移：对比当前 change 中的术语用法与既有 glossary/taxonomy 的一致性。
---

# 检测术语漂移

## 适用场景

- 新 change 写入后，需要检查术语是否与既有 glossary 一致。
- 发现同一术语在不同文件中含义可能不一致。

## 输入

- 当前 change 的 `draft.md` 与笔记。
- 既有 glossary / taxonomy 文件。

## 输出

- 术语漂移报告（不一致的术语、可能的冲突、建议的标准化用法）。

## 读取文件

- `draft.md`、`sources/notes/*.md`。
- 仓库中已有的 glossary / taxonomy 文件。

## 写入文件

- 术语漂移报告（由调用方决定写入位置）。

## 禁止事项

- 不得直接修改术语用法，只输出报告与建议。

## 自检

- 报告是否覆盖了 draft 中的所有关键术语？
- 每个漂移项是否标注了冲突位置与建议？
