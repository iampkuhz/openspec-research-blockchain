# 命令模型

## 结论先说

这个仓库的命令层分三层：

1. OpenSpec 原生命令
2. qoder slash command
3. 仓库本地 wrapper

推荐顺序也是这个顺序。

## 1. OpenSpec 原生命令

这个仓库的主入口应是：

- `openspec update`
- `openspec new change <change-name> --schema blockchain-research`
- `openspec status --change <change-name>`
- `openspec instructions request --change <change-name>`
- `openspec instructions plan --change <change-name>`
- `openspec instructions draft --change <change-name>`
- `openspec instructions dependencies --change <change-name>`
- `openspec instructions decision-criteria --change <change-name>`
- `openspec instructions evidence-matrix --change <change-name>`
- `openspec schema validate blockchain-research`

职责分别是：

- `openspec update`
  刷新客户端 AI 指令层。
- `openspec new change ... --schema blockchain-research`
  创建 `openspec/changes/<change-name>/`。
- `openspec status --change ...`
  根据 schema 依赖图显示哪些 artifact 已完成、哪些被阻塞。
- `openspec instructions <artifact> --change ...`
  生成“当前这个 artifact 该怎么写”的富化指令。
- `openspec schema validate blockchain-research`
  校验 schema 本身。

注意：

- 当前不要把 `openspec validate --changes` 当作 research change 的主校验命令
- 它仍然偏向 spec-driven 的 delta 校验，会期待 `specs/` 目录中的 requirement deltas
- 对本仓库，更可靠的检查方式是：
  - `openspec status --change <change-name>`
  - `support/docs/checklists/...`
  - 人工 review

## 2. `openspec instructions` 实际读什么、产出什么

以：

- `openspec instructions plan --change primitive-eip-4337-deep-dive-pass-1`

为例，它会读取：

- `openspec/config.yaml` 中的仓库级 context
- `openspec/schemas/blockchain-research/schema.yaml` 中 `plan` artifact 的 `instruction` 与 `requires`
- `openspec/schemas/blockchain-research/templates/plan.md`
- `openspec/changes/primitive-eip-4337-deep-dive-pass-1/` 中已经存在的上游 artifact

它不会直接替你把文件写好。它的输出是一段给 AI 或人工使用的“当前 plan.md 应如何生成”的指令。

所以在这个仓库里：

- schema 定义 artifact 图
- `instructions` 把 artifact 图翻译成当前一步的执行说明
- AI 或人工再据此写入目标文件

## 3. qoder command 到底是什么

qoder command 不是 schema 自动生成的能力，也不是 `openspec update` 自动帮你注册好的仓库命令。

它更像：

- 客户端侧的 slash command 别名
- 背后绑定仓库提供的 skill

这个仓库现在直接提供项目级自定义命令：

- `/build-plan`
- `/build-draft`
- `/promote-reference`

这三条命令的输入输出约定是：

| 命令 | 输入 | 输出 | 你主要 review 什么 |
| --- | --- | --- | --- |
| `/build-plan` | `request.md` | `plan.md` | 问题拆解、后续确认问题、来源分层、证据缺口 |
| `/build-draft` | `request.md`、`plan.md`、必要时可选文件 | `draft.md` | 术语区、机制、设计原因、边界、有限结论 |
| `/promote-reference` | 稳定版 `draft.md` | `knowledge/.../reference.md`，decision 额外保留 `verdict.md` | 是否还残留过程痕迹 |

## 4. `/opsx:propose` 为什么不是主入口

`/opsx:propose` 不是这个仓库 schema 自己定义的命令。它来自 OpenSpec 默认 spec-driven 指令层。

按默认语义，它更接近生成：

- `proposal.md`
- `specs/`
- `design.md`
- `tasks.md`

这和本仓库的研究主链：

- `request.md`
- `plan.md`
- `draft.md`

并不匹配，所以不要把它当主入口。

## 5. 为什么还保留本地 wrapper

保留 wrapper 只是为了少敲字：

- `./scripts/new_change.sh primitive eip-4337-pass-1`
- `make change-primitive NAME=eip-4337-pass-1`
- `make validate-schema`

它不是主语义，也不替代 OpenSpec。
