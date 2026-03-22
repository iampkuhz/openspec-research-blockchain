# 命令模型

## 结论先说

这个仓库的命令层分三层：

1. OpenSpec 原生命令
2. 客户端 slash command
3. 仓库本地 wrapper

推荐顺序也是这个顺序。

## 1. OpenSpec 原生命令

这个仓库的主入口应是：

- `openspec update`
- `openspec new change <change-name> --schema blockchain-research`
- `openspec status --change <change-name>`
- `openspec instructions request --change <change-name>`
- `openspec instructions brief --change <change-name>`
- `openspec instructions sources --change <change-name>`
- `openspec instructions dependencies --change <change-name>`
- `openspec instructions analysis --change <change-name>`
- `openspec instructions verdict --change <change-name>`
- `openspec validate --changes`
- `openspec schema validate blockchain-research`

它们的职责分别是：

- `openspec update`
  刷新客户端 AI 指令文件，让 slash command 与仓库配置保持一致。
- `openspec new change ... --schema blockchain-research`
  创建 `openspec/changes/<change-name>/`。
- `openspec status --change ...`
  根据 schema 依赖图显示哪些 artifact 已完成、哪些被阻塞。
- `openspec instructions <artifact> --change ...`
  生成“当前这个 artifact 该怎么写”的富化指令。
- `openspec validate --changes`
  校验当前 change。
- `openspec schema validate blockchain-research`
  校验 schema 本身。

## 2. `openspec instructions` 实际读什么、产出什么

以：

- `openspec instructions analysis --change eip-4337-pass-1`

为例，它会读取：

- `openspec/config.yaml` 中的仓库级 context
- `openspec/schemas/blockchain-research/schema.yaml` 中 `analysis` artifact 的 `instruction` 与 `requires`
- `openspec/schemas/blockchain-research/templates/analysis.md`
- `openspec/changes/eip-4337-pass-1/` 中已经存在的上游 artifact

它不会直接替你把文件写好。它的输出是一段给 AI 或人工使用的“当前分析文档应如何生成”的指令。

所以在这个仓库里：

- schema 定义 artifact 图
- `instructions` 把 artifact 图翻译成当前一步的执行说明
- AI 或人工再据此写入目标文件

## 3. `/opsx:propose` 到底是什么

`/opsx:propose` 不是这个仓库 schema 自己定义的命令。它来自 OpenSpec 写入客户端的 AI 指令层。

OpenSpec 官方 README 明确要求：

- 在项目目录里执行 `openspec update`

这样客户端才会拿到最新 slash command 对应的指令。

按官方默认 `core` profile，`/opsx:propose "your idea"` 走的是 spec-driven 语义，默认生成：

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/specs/`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`

这就是为什么本仓库不把它当主入口。它针对的是默认 spec-driven 流程，不是本仓库的 research-driven schema。

## 4. 这个仓库里 slash command 该怎么理解

在这个仓库里，更稳的思路是：

1. 先执行 `openspec update`
2. 用 `openspec new change <change-name> --schema blockchain-research` 开 change
3. 用 `openspec status --change <change-name>` 看当前依赖图
4. 用 `openspec instructions <artifact> --change <change-name>` 驱动具体 artifact

也就是说，slash command 只是外层入口；真正决定输入、依赖和目标文件的，仍然是：

- `openspec/config.yaml`
- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/schemas/blockchain-research/templates/...`
- 当前 `openspec/changes/<change-name>/` 中已存在的文件

## 5. 推荐的研究语义映射

如果你的客户端支持自定义 slash command，更适合映射成研究语义：

- `/opsx:request-brief` -> `skills/request-brief/`
- `/opsx:sources-evidence` -> `skills/sources-evidence/`
- `/opsx:analysis-writing` -> `skills/analysis-writing/`
- `/opsx:decision-verdict` -> `skills/decision-verdict/`
- `/opsx:promote-canonical` -> `skills/promote-canonical/`

这层属于客户端映射，不是仓库目录自动生成的能力。

## 6. 为什么还保留 `make`

保留 `make` 只是为了少敲字：

- `make change-primitive NAME=eip-4337-pass-1`
- `make validate-schema`

它不是主语义，也不替代 OpenSpec。
