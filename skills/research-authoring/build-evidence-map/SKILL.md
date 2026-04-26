---
name: build-evidence-map
description: 为当前 change 生成 sources/evidence-map.md，梳理证据缺口与来源覆盖情况。
---

# 生成证据地图

## 适用场景

- `sources/source-pack.md` 已完成，需要系统化梳理来源覆盖的证据面。
- 需要识别哪些 claims 缺少足够的来源支撑。

## 输入

- 当前 change 目录路径。
- `sources/source-pack.md`。
- `plan.md` 中的研究范围。

## 输出

- `sources/evidence-map.md`（写入当前 change 目录下）。

## 读取文件

- `plan.md`。
- `sources/source-pack.md`。
- `sources/excerpts/`（如有）。

## 写入文件

- `openspec/changes/<change-id>/sources/evidence-map.md`

## 禁止事项

- 不得伪造不存在的来源证据。
- 不得跳过 source-pack 直接生成 evidence-map。

## 自检

- 证据地图是否覆盖了 plan 中列出的所有关键问题？
- 每个证据项是否标注了来源类型与可信度？
