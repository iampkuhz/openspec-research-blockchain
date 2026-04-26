---
name: build-publish-plan
description: 为当前 change 生成 publish.md，定义从 draft.md 到 knowledge/** 的映射规则。
---

# 生成发布计划

## 适用场景

- `draft.md` 已通过 review（或有明确豁免）。
- 需要将 draft 内容映射到 `knowledge/**` 长期目录。
- 需要定义 `publish_targets` 与校验规则。

## 输入

- 当前 change 目录路径。
- `draft.md`、`review.md`。
- `change.yaml`（含 research_type / profile）。

## 输出

- `publish.md`（写入当前 change 目录下），包含 `publish_targets` 列表。

## 读取文件

- `openspec/schemas/blockchain-research/schema.yaml`（artifact 模型）。
- `openspec/schemas/blockchain-research/templates/publish.md`（如存在）。
- `openspec/config.yaml`（apply 规则）。

## 写入文件

- `openspec/changes/<change-id>/publish.md`

## 禁止事项

- 不得跳过 publish.md 直接写入 `knowledge/**`。
- 不得从 request.md 或 plan.md 直接生成 publish.md。
- decision 类型必须包含 `verdict.md` 的 publish target。

## 自检

- publish_targets 是否覆盖所有需要沉淀的内容？
- 目标路径是否与 `schema.yaml` 的 artifact 模型一致？
