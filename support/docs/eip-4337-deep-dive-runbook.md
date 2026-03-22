# EIP-4337 Deep-Dive 操作手册

## 适用范围

这份手册只用于跑通一次：

- 研究对象：`EIP-4337`
- 对象层级：`primitive`
- 研究路径：`deep-dive`

目标不是一次把研究写完，而是完整走通一轮 `request -> plan -> draft -> promote` 的 research-driven OpenSpec 流程。

## 本次固定参数

建议把本轮 change 名固定为：

```bash
export CHANGE=primitive-eip-4337-deep-dive-pass-1
```

本轮过程目录：

```text
openspec/changes/$CHANGE/
```

本轮希望得到的核心过程产物：

- `request.md`
- `plan.md`
- `draft.md`

本轮默认不强制创建：

- `dependencies.md`
- `decision-criteria.md`
- `evidence-matrix.md`

只有在出现明显争议主张、证据不足或需要额外约束时，才补 `evidence-matrix.md`。

本轮最终要提炼出的长期产物：

- `knowledge/analysis/primitives/eip-4337/reference.md`

## 总览

| 步骤 | 命令 | 主要输入 | 主要产物 |
| --- | --- | --- | --- |
| 0 | `openspec update` | 仓库 schema / config | 最新 OpenSpec 指令层 |
| 1 | `openspec new change ...` | `CHANGE` 名称 | `openspec/changes/$CHANGE/` |
| 2 | 手工写 `request.md` | 你的问题、范围、非目标 | `request.md` |
| 3 | `openspec instructions plan ...` 或 `/build-plan <change-path>` | `request.md` | `plan.md` |
| 4 | review `plan.md` | `plan.md` | 稳定版 `plan.md` |
| 5 | `openspec instructions draft ...` 或 `/build-draft <change-path>` | `request.md`、`plan.md` | `draft.md` |
| 6 | review `draft.md` | `draft.md` | 稳定版 `draft.md` |
| 7 | `/promote-reference <change-path>` | 稳定版 `draft.md` | `knowledge/.../reference.md` |

## Step 0：刷新指令层

执行：

```bash
openspec update
openspec schema validate blockchain-research
```

输入：

- `openspec/config.yaml`
- `openspec/schemas/blockchain-research/schema.yaml`

产物：

- 客户端最新 OpenSpec 指令层
- schema 校验结果

人工检查：

- schema 名确实是 `blockchain-research`
- artifact 主链已经是 `request -> plan -> draft`

参考：

- `support/docs/command-model.md`
- `support/docs/workflow.md`

## Step 1：创建 change

执行：

```bash
openspec new change "$CHANGE" --schema blockchain-research
```

输入：

- 环境变量 `CHANGE`
- schema 名 `blockchain-research`

产物：

- `openspec/changes/$CHANGE/`

人工检查：

- `CHANGE` 名稳定、可读、可复用
- 本次对象是 `primitive`
- 本次路径是 `deep-dive`

参考：

- `support/docs/research-model.md`

## Step 2：手工写 `request.md`

执行：

直接编辑：

```text
openspec/changes/$CHANGE/request.md
```

输入：

- 你当前真正想回答的问题
- 当前范围
- 当前非目标
- 已知输入

产物：

- `request.md`

人工应该写什么：

- 当前问题是 `EIP-4337` 的流程、角色、设计原因、边界
- 预期输出是单对象深挖，不是整个 AA 全景

人工不必现在写什么：

- 不必现在回答“为什么 4337 不直接改传统 transaction 路径”
- 不必现在确定 `bundler`、`EntryPoint`、`paymaster` 分别位于哪一层
- 不必现在完全区分哪些能力是 protocol-native，哪些只是 official ecosystem 或 third-party

这些都留到 `plan.md` 的“后续确认问题”。

参考：

- `openspec/schemas/blockchain-research/templates/request.md`
- `support/docs/language-style.md`

## Step 3：生成 `plan.md`

执行方式二选一：

```bash
openspec instructions plan --change "$CHANGE"
```

或在 Qoder 中执行：

```text
/build-plan openspec/changes/primitive-eip-4337-deep-dive-pass-1/
```

输入：

- `request.md`

产物：

- `plan.md`

人工重点检查：

- 对象类型是否写成 `primitive`
- 研究路径是否写成 `deep-dive`
- 预算是否默认 `deep`
- 来源是否按 `L1/L2/L3/L4` 分层
- 后续确认问题里是否真的列出了：
  - 为什么 4337 不直接改传统 transaction 路径
  - `bundler`、`EntryPoint`、`paymaster` 分别属于什么层
  - 哪些能力是 protocol-native，哪些只是 official ecosystem 或 third-party
- 是否显式标了 `evidence gap` 与 `unresolved ambiguity`

参考：

- `skills/build-plan/SKILL.md`
- `support/templates/plan.md`
- `support/prompts/build-plan.md`
- `support/docs/evidence-policy.md`

## Step 4：review `plan.md`

这一轮 review 只盯四件事：

1. 问题有没有被收紧
2. 来源分层是否合理
3. 后续确认问题是否够具体
4. 暂不处理的内容是否已经挡住研究滑坡

对 `EIP-4337` 来说，典型的“应该挡住”的内容包括：

- 不做完整 `account-abstraction` 主题地图
- 不做 `EIP-7702` / `EIP-3074` 全面对比
- 不做链选择或钱包选型

如果这一步没收紧，后面 `draft.md` 一定会发散。

## Step 5：生成 `draft.md`

执行方式二选一：

```bash
openspec instructions draft --change "$CHANGE"
```

或在 Qoder 中执行：

```text
/build-draft openspec/changes/primitive-eip-4337-deep-dive-pass-1/
```

输入：

- `request.md`
- `plan.md`
- 如有需要，再加 `evidence-matrix.md`

产物：

- `draft.md`

人工重点检查：

- “关键术语”是否是列表，而不是按词分标题
- 是否先写机制，再写价值
- 是否明确解释“为什么这样设计，而不是那样设计”
- 是否明确区分 protocol-native / official ecosystem / third-party
- 是否明确区分 live / planned / promotional
- “当前可确认结论”是否有限、受证据约束
- “当前不能确认的部分”是否真的写出了不确定性，而不是假装完成

参考：

- `skills/build-draft/SKILL.md`
- `support/templates/draft.md`
- `support/prompts/build-draft.md`
- `support/docs/checklists/general-research.md`
- `support/docs/checklists/deep-dive.md`

## Step 6：review `draft.md`

这一轮 review 的目标不是润色，而是做结构校验。

优先检查：

- 术语区是否真的帮助理解正文
- 流程是否连贯
- 设计原因有没有回答到
- 边界有没有写出来
- 结论有没有越过证据

如果这一轮发现关键主张只有 `L3/L4` 支撑，再回去补：

- `plan.md`
- 必要时 `evidence-matrix.md`

不要直接硬改结论句型来掩盖证据不足。

## Step 7：提炼长期 `reference.md`

执行：

在 Qoder 中执行：

```text
/promote-reference openspec/changes/primitive-eip-4337-deep-dive-pass-1/
```

或按 `skills/promote-canonical/` 的规范手工提炼。

输入：

- 稳定版 `draft.md`

产物：

- `knowledge/analysis/primitives/eip-4337/reference.md`

人工重点检查：

- 长期稿里不要保留过程口吻
- 不要把 `request.md`、`plan.md` 原样抄进长期目录
- 关键术语要并入 `reference.md`
- 结论部分默认并入 `reference.md`，不要额外拆一个 primitive 级 `verdict.md`

参考：

- `skills/promote-canonical/SKILL.md`
- `support/templates/primitive-deep-dive.md`
