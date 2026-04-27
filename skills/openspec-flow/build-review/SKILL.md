---
name: openspec-build-review
description: 当 draft.md 已完成且需要进入评审阶段，对 draft 的 claim traceability、术语一致性与结论边界进行独立评审，生成 review.md 时使用。
---

# 生成研究评审

## 适用场景

- `draft.md` 已完成，需要进入 review 阶段。
- 需要对 draft 的 claim traceability、术语一致性、结论边界进行独立评审。

## 输入

- 当前 change 目录路径。
- `draft.md` 内容。
- `sources/` 目录下的来源证据。

## 输出

- `review.md`（写入当前 change 目录下）。

## 读取文件

- 当前 change 的 `change.yaml`。
- `draft.md`。
- `sources/source-pack.md`、`sources/evidence-map.md`、`sources/excerpts/`。
- `openspec/schemas/blockchain-research/templates/review.md`（如存在）。

## 写入文件

- `openspec/changes/<change-id>/review.md`

## 禁止事项

- 不得修改 `draft.md` 正文，评审意见只写入 `review.md`。
- 不得跳过 draft 直接生成 review。
- 不得直接写 `knowledge/**`。

## 自检

- review 是否覆盖了所有 draft 中的核心 claims？
- 每个 claim 是否可追溯到 source？
