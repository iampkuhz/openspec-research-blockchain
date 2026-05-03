---
name: openspec-build-draft
description: 当当前 change 已有 request、plan 与证据材料，需要生成或修复唯一主候选产物 draft.md，并满足 draft gate 时使用。
---

# openspec-build-draft

## 何时使用

- `plan.md` 已通过 review，来源规划足以支撑第一轮正文。
- 需要把术语、分析、有限结论合并为一次集中 review 稿。
- draft gate 校验失败，需要修复 `draft.md`。

## 输入

- `openspec/changes/<id>/request.md`
- `openspec/changes/<id>/plan.md`
- `openspec/changes/<id>/sources/source-pack.md`
- `openspec/changes/<id>/sources/evidence-map.md`
- `openspec/changes/<id>/sources/excerpts/`（如有）

## 输出

- `openspec/changes/<id>/draft.md`
- 不生成新的 `openspec/changes/<id>/diagrams/<diagram-id>/`；如需正式 PlantUML 图，必须先由主会话调用 `diagram-agent` 完成。

## 必读文件

- `harness/workflows/research-step-execution.md` —— draft 阶段执行规约
- `harness/rules/diagrams/diagram-policy.md` —— 图表政策
- `openspec/schemas/blockchain-research/templates/draft.md` —— draft 模板

## 执行步骤

1. 读取 request.md、plan.md 与来源材料，确认前置条件已满足。
2. 对 mechanism-heavy 内容先写实体分类表（role / component / data / state / external）。
3. 写图表清单表，明确必需图、回答的问题、可省略的理由。
4. 先写术语表（表格形式），再写分析正文。
5. 如果 plan 要求正式 PlantUML 图但 `diagrams/<diagram-id>/validation.json` 缺失或未通过，停止并向主会话返回 `diagram-agent` handoff；不要在 draft skill 内直接调用 PlantUML skill。
6. 消费已完成的 diagram package，在 draft.md 中每个 PlantUML block 前添加 contract comment：`<!-- verified-diagram: package=./diagrams/<id>/validation.json puml=./diagrams/<id>/diagram.puml sha256=<sha256> -->`。
7. 只读取最终 `validation.json` 与 `diagram.puml` 做嵌入和 contract 判定；不要重跑 diagram validation 或再次调用 PlantUML skill。
8. 验证 draft.md 参考资料链接状态，更新 `[已验证]` / `[未验证]` 标记。

## 禁止事项

- 不直接写 `knowledge/**`。
- 不绕过 change.yaml 跳过类型判断。
- 不生成 `work-products/*.md`。
- 不手写 PlantUML block 后跳过 diagram contract 流程。
- 不在 validation.json 未显示 success 时声称图已完成。
- 不在 draft 阶段直接调用 `feipi-plantuml-generate-architecture-diagram` / `feipi-plantuml-generate-sequence-diagram`；正式图表缺失时返回 handoff。

## 自检

```bash
python3 scripts/research/validate_draft_diagram_contract.py openspec/changes/<id>/draft.md
python scripts/hooks/dispatch.py --change openspec/changes/<id> --gate post_draft --json
```
