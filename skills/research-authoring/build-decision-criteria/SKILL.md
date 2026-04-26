---
name: build-decision-criteria
description: 为 decision 类型研究生成 decision-criteria.md，定义评估维度与判断标准。
---

# 生成决策标准

## 适用场景

- 研究类型为 `decision`，需要在方案对比前明确评估维度。
- 适用 `decision` profile。

## 输入

- `request.md`（研究问题与范围）。
- `plan.md`（研究路径）。
- 候选方案列表。

## 输出

- `decision-criteria.md`（写入当前 change 目录下）。

## 读取文件

- `request.md`、`plan.md`。
- `sources/source-pack.md`（如有）。

## 写入文件

- `openspec/changes/<change-id>/decision-criteria.md`

## 禁止事项

- 不得在方案对比之后再补充标准。
- 决策标准必须与研究问题直接相关。

## 自检

- 每个评估维度是否与研究问题直接相关？
- 标准是否足够具体，能支撑后续 verdict 判断？
