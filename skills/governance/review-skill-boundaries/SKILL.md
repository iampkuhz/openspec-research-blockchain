---
name: review-skill-boundaries
description: 审查 skills/ 目录中各 skill 的职责边界是否清晰，是否存在职责重叠或分类错误。
---

# 审查 Skill 边界

## 适用场景

- 新增或重构 skill 后，需要确认分类是否合理。
- 发现多个 skill 职责重叠、分类不清。

## 输入

- `skills/` 目录。
- 每个 skill 的 `SKILL.md`。

## 输出

- 边界问题清单（重叠 skill、错分类别、命名不一致）。
- 重构建议。

## 读取文件

- `skills/*/SKILL.md`。
- `skills/README.md`。

## 写入文件

- 治理评审报告（由调用方决定写入位置）。

## 禁止事项

- 不得直接重构 skill 文件，只输出审查报告与重构建议。

## 自检

- 每个 skill 的 description 是否与其他 skill 有实质性重叠？
- skill 的分类目录是否与 description 中的使用场景一致？
