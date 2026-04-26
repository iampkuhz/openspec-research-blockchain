---
name: render-diagram-contract
description: 为 change 生成 diagram supporting artifacts（brief、PlantUML 源码、验证报告），不直接修改 knowledge/**。
---

# 渲染图表合约

## 适用场景

- 需要为 draft.md 中的 PlantUML 图生成 diagram package。
- 需要确保图表产出符合 diagram contract（brief → puml → validation）。

## 输入

- 图表 brief 描述。
- 当前 change 目录路径。

## 输出

- `diagrams/<diagram-id>/brief.yaml`
- `diagrams/<diagram-id>/diagram.puml`
- `diagrams/<diagram-id>/validation.json`

## 读取文件

- `draft.md`（如需基于现有内容生成图）。
- `openspec/schemas/blockchain-research/templates/`（如图表模板存在）。

## 写入文件

- `openspec/changes/<change-id>/diagrams/<diagram-id>/`

## 禁止事项

- 不得直接修改 `knowledge/**`。
- 不得手写 PlantUML 后跳过验证流程。
- 不得伪造 validation.json 状态。

## 自检

- diagram package 是否包含 brief、puml、validation.json？
- validation.json 的 final_status 是否为 success？
