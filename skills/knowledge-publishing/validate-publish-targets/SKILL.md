---
name: publish-validate-targets
description: 当 publish.md 已生成，需要校验 publish_targets 的路径与 schema.yaml 的 artifact 模型一致且 decision 类型包含 verdict.md target 时使用。
---

# 校验发布目标

## 适用场景

- `publish.md` 已生成，需要在实际写入 `knowledge/**` 前校验目标合法性。
- 需要确认 publish_targets 的路径与类型映射正确。

## 输入

- 当前 change 的 `publish.md`。
- `change.yaml`。

## 输出

- 校验通过/失败报告，含具体不合规项。

## 读取文件

- `publish.md`、`change.yaml`、`draft.md`。
- `openspec/schemas/blockchain-research/schema.yaml`。
- `openspec/config.yaml`（apply 规则）。

## 写入文件

不直接写入文件，输出校验报告供 `/spec-research-publish` 使用。

## 禁止事项

- 不得在校验未通过时允许写入 `knowledge/**`。
- 不得跳过 publish.md 直接校验。

## 自检

- 每个 publish_target 的路径是否与 schema 定义的类型一致？
- decision 类型是否包含 `verdict.md` target？
