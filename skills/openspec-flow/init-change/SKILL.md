---
name: openspec-init-change
description: 当用户提出新的研究目标需要创建 change 目录、change.yaml、request.md、plan.md 及完整子目录结构时使用。
---

# openspec-init-change

## 何时使用

- 用户以自然语言提出"创建一个新的研究"、"初始化 <topic> 的研究"等请求。
- 路由判断完成后，需要创建 `openspec/changes/<change-id>/` 目录。
- 二次研究需要新建独立 change（而非在既有 artifact 上直接修改）。

## 输入

- 用户研究需求的自然语言描述。
- 路由结果：`task_type`（primitive/synthesis/decision/source_reading）。
- `change_operation`：create / update（当前仅支持这两项）。

## 输出

- `openspec/changes/<change-id>/change.yaml`
- `openspec/changes/<change-id>/request.md`
- `openspec/changes/<change-id>/plan.md`
- `openspec/changes/<change-id>/sources/`、`notes/`、`claims/` 空目录

## 必读文件

- `openspec/schemas/blockchain-research/schema.yaml` —— change 结构
- `openspec/schemas/blockchain-research/templates/request.md`
- `openspec/schemas/blockchain-research/templates/plan.md`

## 执行步骤

1. 从路由结果确定 `task_type` 与 `change_operation`。
2. 生成 change-id：`<type>-<topic>-<path>-pass-1`。
3. 创建 change 目录与 `sources/`、`notes/`、`claims/` 子目录。
4. 生成 `change.yaml`，填入 `id`、`schema`、`task_type`、`change_operation`、`artifacts`、`validators`、`publish_targets`。
5. 生成 `request.md`，包含目标、范围边界、非目标、预期输出。
6. 生成 `plan.md`，包含问题拆解、来源规划、证据缺口、完成标准。
7. 如为 decision 类型，创建空 `decision-criteria.md`。

## 禁止事项

- 不直接在 `knowledge/` 下创建文件。
- 不跳过 request.md 直接写分析。
- 不绕过 change.yaml 声明 artifact。
- 不将单一复杂需求硬塞进一个 change。

## 自检

```bash
python scripts/hooks/dispatch.py --change openspec/changes/<change-id> --gate post_draft --json
```
