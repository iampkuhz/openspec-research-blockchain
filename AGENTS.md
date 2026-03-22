# AGENTS.md

## 这个仓库是什么

这是一个基于 OpenSpec 的区块链技术调研工作台，用于长期维护多层级研究对象，而不是一次性输出单篇文章。

长期目录分离为：

- `knowledge/`：长期正式产出父目录
- `knowledge/analysis/`：长期事实分析资产
- `knowledge/decisions/`：长期场景决策资产
- `openspec/changes/`：当前研究改动包
- `openspec/specs/`：长期研究系统 specs

仓库内的研究对象只有四类：

- `domain`
- `primitive`
- `synthesis`
- `decision`

仓库内的主要研究路径只有三类：

- `deep-dive`
- `evolution`
- `scenario`

## 这个仓库不是什么

- 不是默认 `proposal/specs/design/tasks` 的软件研发仓库
- 不是营销内容仓库
- 不是“先给结论，再倒找材料”的观点仓库
- 不是把所有对象都做成同样深度的平铺笔记仓库

## 输出总原则

所有输出必须遵循以下优先顺序：

1. 先机制，后价值
2. 先事实，后判断
3. 先边界，后结论
4. 先说明为什么这样做，再说明为什么不是那样做
5. 结论必须受证据等级约束

禁止把 marketing copy、生态宣传语、空泛趋势判断直接写入结论。

## 语言要求

- 中文优先维护
- 英文术语优先保留
- 协议名、标准名、字段名、EIP/ERC/RIP 编号、专业名词优先保留英文
- 不要强行把关键技术术语全部中文化
- 正文解释与分析以中文为主
- 风格必须专业、克制、技术导向

## 证据政策

必须显式区分证据等级：

- `L1`: 官方 spec / EIP / whitepaper / protocol docs
- `L2`: 官方 docs / repo / SDK / API / 实现证据
- `L3`: 官方 blog / release / roadmap / ecosystem material
- `L4`: 第三方解读 / 媒体 / 评论材料

执行要求：

- 关键机制判断优先基于 `L1/L2`
- 若某结论仅由 `L3/L4` 支撑，必须降级表述
- 必须标注 `evidence gap`
- 必须标注 `unresolved ambiguity`
- 必须区分“文档写了什么”和“链上/实现实际上支持什么”

## 能力边界区分要求

所有研究必须区分：

- 原生协议能力
- 官方生态能力
- 第三方能力

并且必须区分：

- 已上线能力
- 规划中能力
- 宣传性表述

不要把钱包、SDK、基础设施服务商、第三方中间件的能力，直接写成协议原生能力。

## 研究层级与复用

技术分析主链：

- 底层：`primitive`
- 中层：`synthesis`
- 上层：`domain`

独立的场景应用层：

- `decision`

补充约束：

- `primitive` 和 `synthesis` 不要通过目录路径被锁死为某个 `domain` 的子节点
- 一个 `primitive` 或 `synthesis` 可以被多个 `domain` 复用
- 与哪些 `domain` 相关，应通过 `plan.md`、`dependencies.md`、正文链接来声明
- `synthesis` 是可选层，不是每个 domain 都必须有单独的 synthesis
- `request.md`、`plan.md` 这类过程 artifact 不应长期保留在 `knowledge/analysis/` 或 `knowledge/decisions/` 中

要求：

- 上层研究可以依赖下层研究
- 上层研究不得重写下层全文
- 上层研究必须在 `dependencies.md` 或 `plan.md` 中显式声明依赖
- 每个依赖都必须有 research budget：`deep` / `focused` / `light`
- 必须解释为什么只需要这个深度

## Glossary 层是核心内容

glossary 层不是附录，必须维护。

默认写法：

- 过程层并入 `draft.md` 的“关键术语”区
- 长期层并入 `artifact.md` 的“关键术语”区
- 术语展示必须使用列表，不使用按词分标题的卡片式结构

每条术语至少包含：

- 术语
- 一句话定义
- 在本题中的作用

如果一个术语在当前研究中承担关键区分作用，就必须入术语区。

## Artifact 级要求

### `request.md`

- 明确问题、目标、非目标、范围边界
- 避免在 request 中提前下结论
- 不要求此时已经写清完整机制
- 需要后续确认的机制问题，进入 `plan.md`

### `plan.md`

- 合并原来的计划层与来源规划层
- 明确对象类型、研究路径、相关 `domain`
- 明确预算、交付边界、完成标准
- 明确 `L1/L2/L3/L4` 来源规划
- 明确 `evidence gap` 与 `unresolved ambiguity`
- 对 `primitive`，把“为什么不直接改传统 transaction 路径”“关键角色分别位于哪一层”“哪些能力不是 protocol-native”这类问题写进“后续确认问题”
- 若是上层研究，必须定义抽取策略而不是全文复写策略

### `draft.md`

- 合并原来的 glossary、analysis、verdict
- 术语区必须是列表
- 先拆机制，再讨论价值
- 必须说明设计原因与替代方案
- 必须说明边界、失败条件、前提条件
- 必须区分 protocol-native、official ecosystem、third-party
- 必须区分 live、planned、promotional
- 有限结论必须写清前提与证据基础

### `artifact.md`

- 只用于 `knowledge/` 下的长期正式结果
- 不是工作中的推演稿，而是可复用的稳定产物
- 应提炼 mechanism、boundary、dependency impact，不保留过程痕迹
- 默认包含“关键术语”区

### `verdict.md`

- 只作为 `decision` 的长期条件性结论文件
- 必须说明结论适用前提
- 必须说明证据不足的地方
- 不得把未验证推断写成确定事实

### `dependencies.md`

- 列出依赖对象、依赖强度、依赖原因、抽取内容
- 强调“引用什么”，而不是“复制什么”

### `decision-criteria.md`

- 仅用于 `scenario` 等需要显式比较标准的研究
- 标准必须可解释、可比较、可复核

### `evidence-matrix.md`

- 把核心判断与证据等级绑定
- 重要判断若只有低等级证据，必须降格处理

## Canonical 目录规则

- `knowledge/analysis/` 和 `knowledge/decisions/` 只保留长期结果
- `request.md`、`plan.md`、一次性纠偏记录应进入 `openspec/changes/`
- `evidence-matrix.md` 默认属于过程性证据组织文件，应进入 `openspec/changes/`
- case 级 `README.md` 默认不进入长期目录
- `primitive / synthesis / domain` 的稳定内容应提炼为长期 `artifact.md`
- `decision` 的 `verdict.md` 可以作为长期文件保留
- 术语层默认并入 `artifact.md`，不单独长期保留 `glossary.md`
- `openspec/specs/` 用于沉淀跨 case 复用的研究系统规则

## 写作禁令

以下内容禁止直接进入正式结论：

- “生态很繁荣，所以前景更好”
- “社区很活跃，所以技术路线成立”
- “看起来更先进”
- “更适合未来”
- 没有边界条件的绝对化表述

若必须使用趋势性判断，必须说明：

- 判断对象
- 适用场景
- 证据等级
- 仍未解决的问题

## 新增或修改研究时的默认动作

1. 先看对象属于哪一层：`domain / primitive / synthesis / decision`
2. 再看路径属于哪一类：`deep-dive / evolution / scenario`
3. 先手工补 `request.md`
4. 再生成并 review `plan.md`
5. 若是上层研究，补 `dependencies.md`
6. 若是场景对比，补 `decision-criteria.md`
7. 若结论涉及争议或证据不足，补 `evidence-matrix.md`
8. 最后生成并 review `draft.md`
9. 稳定后提炼到 `knowledge/`

## 默认审稿标准

在 review 或自检时，优先检查：

- 机制是否讲清楚
- 设计原因是否讲清楚
- 边界是否写出来
- 证据等级是否够高
- 是否错误混用了原生能力、官方生态能力、第三方能力
- 是否错误混用了已上线、规划中、宣传性表述
- 上层研究是否复写了下层全文
- 关键术语是否覆盖
