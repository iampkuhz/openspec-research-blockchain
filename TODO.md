# TODO

## ~~openspec/specs 里面有一些应该放到 harness/~~ [已完成]

已完成迁移。`openspec/specs/` 现在只保留仓库级物理定律（5 个）：
- `repository-asset-model/` — 仓库拓扑
- `canonical-output-model/` — 产出模型
- `evidence-policy/` — 证据标准
- `analysis-principles/` — 分析哲学
- `research-object-model/` — 对象分类学

已迁移到 `harness/`：
- 流程阶段 → `harness/workflows/{request,plan,draft,artifact}-phase.md`
- 领域质量 → `harness/rules/research/{component-quality,consensus-depth}-rules.md`
- 图表质量 → `harness/rules/diagrams/{diagram-policy,architecture-quality,component-abstraction}-*.md`
- 语言风格 → `harness/rules/writing/language-rules.md`


## claw4ai 反爬虫命中

如何降低反爬虫命中概率？

| 属性 | 值 |
|------|------|
| **URL** | https://www.w3.org/TR/did-core/ |
| **验证状态** | ⚠️ 未验证 - Cloudflare 反爬虫拦截 |
| **替代来源** | https://github.com/w3c/did (GitHub 仓库，已验证) |




### Tendermint 共识算法

/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/openspec/changes/primitive-tendermint-consensus-deep-dive-pass-1/plan.md

1. 图标交付可能要区分：一个角色内部的组件分层；和不同角色之间的流程，可能是多个图
   2. 图1*n：每个角色一个图，每个角色内部的组件架构图
   3. 角色之间的流程图：每一个步骤，怎么在角色之间流转和处理
   4. 每个角色内部的状态机转换
2. 说明角色和组件的区分关系：组件是指他们的掌控方是同一个人，互相之间没有任何信任假设，无条件信任；角色不同之间有信任假设，基于信任假设才能互相通信

## 以 登链的 Tendermint 文章作为入口，分析仓库对于指定文章来源扩充知识库的能力效果

## 基于 karpathy wiki 优化

> https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f 
> # LLM Wiki
>
> 一种使用 LLM 构建个人知识库的模式。
>
> 这是一份 idea file，设计出来就是为了让你直接复制粘贴给你自己的 LLM Agent（例如 OpenAI Codex、Claude Code、OpenCode / Pi 等）。它的目标是传达这个想法的高层思路，而你的 agent 会在与你协作的过程中把具体实现细化出来。
>
> ## 核心想法
>
> 大多数人把 LLM 和文档结合起来使用时，形式看起来都像 RAG：你上传一批文件，LLM 在查询时检索相关片段，然后生成答案。这种方式能用，但 LLM 每次提问时都在从零重新发现知识。
> 如果你问了一个微妙的问题，而这个问题需要综合五份文档，LLM 每次都得重新找到并拼接相关碎片。没有任何积累。NotebookLM、ChatGPT 文件上传，以及大多数 RAG 系统，基本都是这样工作的。
>
> 这里的想法不一样。不是只在查询时从原始文档里检索，而是让 LLM 逐步构建并维护一个持久化的 wiki——它是位于你和原始资料之间的一组结构化、可互链的 markdown 文件。
> 当你加入一个新来源时，LLM 并不是只给它建立索引，等以后再检索。它会去读它，提取其中的关键信息，并把这些信息整合进已有 wiki 中——更新实体页面、修订主题摘要、记录哪里有新数据与旧观点相矛盾、强化或挑战当前不断演进的综合结论。知识被编译一次，然后持续保持最新，而不是每次提问时重新推导。
>
> 这才是关键差别：这个 wiki 是一个持久的、会不断复利的产物。交叉引用已经在那里。矛盾已经被标记出来。综合结论已经反映了你读过的全部内容。随着你加入更多来源、提出更多问题，这个 wiki 会越来越丰富。
>
> 你自己永远不需要（或几乎不需要）亲手去写这个 wiki——LLM 会负责写并维护全部内容。你负责的是来源收集、探索，以及提出正确的问题。LLM 负责所有脏活累活——摘要、交叉引用、归档、记账式维护，这些正是知识库长期真正有用所必需的工作。
> 在实践里，我通常一边开着 LLM agent，一边开着 Obsidian。LLM 会根据我们的对话直接修改内容，而我实时浏览结果——点链接、看 graph view、读更新后的页面。Obsidian 是 IDE；LLM 是程序员；wiki 是代码库。
>
> 这可以应用在很多场景中。几个例子：
>
> - **个人场景**：追踪你自己的目标、健康、心理状态、自我提升——把日记、文章、播客笔记归档进去，随着时间推移建立一幅关于你自己的结构化图景。
> - **研究场景**：围绕一个主题连续深入几周或几个月——阅读论文、文章、报告，并逐步构建一个带有演进中论点的综合 wiki。
> - **读一本书**：随着阅读进度把每一章归档进去，逐步建立人物、主题、情节线及其联系的页面。读完时你就拥有了一个丰富的伴读 wiki。想想 Tolkien Gateway 这类 fan wiki——成千上万个相互链接的页面，覆盖人物、地点、事件、语言，多年来由志愿者社区构建。你可以在个人阅读过程中构建类似的东西，只不过交叉引用和维护都由 LLM 来做。
> - **企业 / 团队场景**：由 LLM 维护的内部 wiki，输入来源可以是 Slack 线程、会议转录、项目文档、客户通话记录。也可以有人类在环审核更新。wiki 能保持最新，是因为维护这件没人愿意做的事由 LLM 承担了。
> - **竞品分析、尽调、旅行规划、课程笔记、兴趣深挖**——任何你会随着时间不断积累知识，并且希望这些知识是被组织起来而不是散落各处的场景。
>
> ## 架构
>
> 有三层：
>
> ### 原始来源（Raw sources）
>
> 这是你精心挑选的一组源文档。文章、论文、图片、数据文件。它们是不可变的——LLM 可以读取它们，但绝不会修改它们。这是你的事实来源。
>
> ### wiki
>
> 这是一个由 LLM 生成的 markdown 文件目录。包括摘要、实体页、概念页、对比页、总览页、综合页。
> 这一层完全由 LLM 拥有。它创建页面，在新来源到来时更新页面，维护交叉引用，并保持整体一致性。你来读；LLM 来写。
>
> ### schema
>
> 这是一个文档（例如给 Claude Code 用的 `CLAUDE.md`，或给 Codex 用的 `AGENTS.md`），它告诉 LLM：这个 wiki 是如何组织的、遵循什么约定、在导入来源、回答问题、维护 wiki 时要走哪些流程。
> 这是关键配置文件——它让 LLM 成为一个纪律严明的 wiki 维护者，而不是一个泛化聊天机器人。你和 LLM 会随着时间共同演化这个 schema，因为你们会逐步发现什么方式最适合你的领域。
>
> ## 操作
>
> ### Ingest（导入）
>
> 你把一个新来源放进原始资料集合里，然后告诉 LLM 去处理它。一个示例流程是：LLM 读取来源，和你讨论关键结论，往 wiki 里写一页摘要，更新索引，更新 wiki 中相关的实体页和概念页，并在日志中追加一条记录。
> 一个来源可能会触发 10 到 15 个 wiki 页面更新。
> 我个人更喜欢一次只导入一个来源，并且保持参与——我会阅读摘要、检查更新、引导 LLM 强调哪些内容。但你也可以一次批量导入很多来源，减少监督。这取决于你想形成什么样的工作流，并把它写进 schema 里，供未来会话复用。
>
> ### Query（查询）
>
> 你围绕 wiki 提问。LLM 会搜索相关页面，读取它们，并带引用地综合出答案。
> 答案的形式可以根据问题而变化——可能是一页 markdown、一个对比表、一份 slide deck（Marp）、一张图（matplotlib）、一个 canvas。
> 这里重要的洞见是：好的回答也可以再反向归档进 wiki，成为新的页面。你提出的一个对比、一次分析、一次新发现的联系——这些都是有价值的，不应该消失在聊天记录里。
> 这样，你的探索过程就会像导入来源一样，在知识库里不断复利。
>
> ### Lint（体检）
>
> 定期让 LLM 给 wiki 做一次健康检查。检查内容包括：
>
> - 页面之间是否有矛盾
> - 是否有已经被新来源覆盖、但仍然保留的陈旧说法
> - 是否存在没有入链的孤儿页
> - 是否有被频繁提到但还没有独立页面的重要概念
> - 是否缺失交叉引用
> - 是否存在可以通过 web search 填补的数据空白
>
> LLM 很擅长提出接下来值得调查的新问题，以及值得继续寻找的新来源。这能让 wiki 在不断增长时仍保持健康。
>
> ## 索引与日志
>
> 有两个特殊文件可以帮助 LLM（以及你）在 wiki 规模增长后继续高效导航。它们的作用不同：
>
> ### `index.md`
>
> 它是面向内容的。它是 wiki 中所有内容的目录——每个页面都列出来，附上链接、一句摘要，以及可选的元数据，例如日期或来源数量。
> 它按类别组织（实体、概念、来源等）。LLM 每次导入时都会更新它。
> 在回答查询时，LLM 先读 index，找出相关页面，再进一步钻取。这个方法在中等规模下效果出奇地好（大约 100 个来源、几百个页面），而且不需要基于 embedding 的 RAG 基础设施。
>
> ### `log.md`
>
> 它是按时间顺序组织的。它是一个只追加的记录，记下发生了什么、发生在何时——导入、查询、lint 检查。
> 一个有用的小技巧是：如果每条记录都以一致前缀开头（例如 `## [2026-04-02] ingest | Article Title`），那么这个日志就可以通过简单的 unix 工具进行解析——比如 `grep "^## \[" log.md | tail -5` 就能取出最近 5 条记录。
> log 能给你提供 wiki 演化时间线，也能帮助 LLM 理解最近都做了什么。
>
> ## 可选项：CLI 工具
>
> 到了某个阶段，你可能会想构建一些小工具，帮助 LLM 更高效地操作 wiki。最显而易见的是一个针对 wiki 页面本身的搜索引擎——在小规模下 index 文件就足够了，但随着 wiki 变大，你会想要真正的搜索能力。
> `qmd` 是一个不错的选择：它是一个面向 markdown 文件的本地搜索引擎，支持 hybrid BM25 / vector search 和 LLM re-ranking，而且全部运行在本地设备上。它既提供 CLI（这样 LLM 可以通过 shell 调用），也提供 MCP server（这样 LLM 可以把它当作原生工具使用）。
> 你也可以自己做一个更简单的版本——随着需要出现，LLM 可以帮你用 vibe-code 的方式快速写一个朴素的搜索脚本。
>
> ## Tips and tricks
>
> ### Obsidian Web Clipper
>
> 这是一个浏览器扩展，可以把网页文章转换成 markdown。对于快速把来源导入原始资料集合非常有用。
>
> ### 下载图片到本地
>
> 在 Obsidian 的 `Settings → Files and links` 中，把 “Attachment folder path” 设为一个固定目录（例如 `raw/assets/`）。
> 然后在 `Settings → Hotkeys` 中搜索 “Download”，找到 “Download attachments for current file”，并给它绑定一个快捷键（例如 `Ctrl+Shift+D`）。
> 这样在剪藏完一篇文章后，按一下快捷键，所有图片就都会被下载到本地磁盘。
> 这一步是可选的，但很有用——它能让 LLM 直接查看和引用图片，而不是依赖可能失效的 URL。
> 不过要注意，LLM 不能在一次处理里天然读取带有内联图片的 markdown——变通方式是先让 LLM 读文本，再单独查看部分或全部引用图片，从而补充上下文。过程有点笨，但足够好用。
>
> ### Obsidian 的 graph view
>
> 这是观察 wiki 整体形状的最佳方式——哪些页面彼此连接、哪些页面是枢纽、哪些页面是孤儿页。
>
> ### Marp
>
> 这是一个基于 markdown 的 slide deck 格式。Obsidian 有它的插件。适合直接从 wiki 内容生成演示文稿。
>
> ### Dataview
>
> 这是一个 Obsidian 插件，可以查询页面 frontmatter。
> 如果你的 LLM 会在 wiki 页面里添加 YAML frontmatter（比如 tags、dates、source counts），那么 Dataview 就可以动态生成表格和列表。
>
> ### Git 仓库
>
> 这个 wiki 本质上只是一个 markdown 文件组成的 git repo。
> 因此你天然就拥有版本历史、分支和协作能力。
>
> ## 为什么这套方法有效
>
> 维护知识库最令人厌烦的部分，不是阅读，也不是思考，而是“记账式维护”。
> 更新交叉引用、保持摘要最新、标记哪里有新数据推翻旧观点、在几十个页面之间维持一致性。人类之所以会放弃 wiki，是因为维护成本增长得比价值更快。
> 而 LLM 不会觉得无聊，不会忘记去更新一个交叉引用，并且一次就能改 15 个文件。wiki 之所以能持续被维护，是因为维护成本几乎为零。
>
> 人的工作是：筛选来源、引导分析、提出好问题、思考这些内容意味着什么。
> LLM 的工作是：其他所有事。
>
> 这个想法在精神上和 Vannevar Bush 于 1945 年提出的 Memex 有亲缘关系——一个个人化的、经过精心策展的知识存储系统，文档之间通过联想路径相互连接。Bush 的愿景其实更接近这个，而不是后来演化出来的 Web：私有的、主动策展的，而且文档之间的连接和文档本身一样有价值。
> 他当时解决不了的问题是：谁来做维护。LLM 解决了这个问题。
>
> ## Note
>
> 这份文档是刻意保持抽象的。它描述的是一种模式，而不是一种特定实现。
> 具体目录结构、schema 约定、页面格式、工具链——这些都会取决于你的领域、你的偏好，以及你选用的 LLM。
> 上面提到的一切都是可选的、模块化的——取你所需，忽略不需要的部分。举例来说：
>
> - 你的来源可能只有文本，所以你根本不需要图片处理。
> - 你的 wiki 可能足够小，因此只靠 index 文件就够了，不需要搜索引擎。
> - 你可能根本不关心 slide deck，只想要 markdown 页面。
> - 你可能需要的是一整套完全不同的输出格式。
>
> 正确使用它的方式，是把它分享给你的 LLM agent，然后和它一起把这个模式实例化成一个适合你需求的版本。
> 这份文档唯一的工作，就是把这个模式本身传达清楚。剩下的部分，你的 LLM 可以自己搞定。


### 任务 1：增加长期 raw sources 层

```text
只做这个任务：为仓库增加“长期保留、不可变、只读”的 raw sources 层设计与落地。

必要约束：
- 不迁移现有内容，只增加结构、说明、模板。
- 不能和 openspec/changes/<id>/sources/ 混淆，必须明确两者关系。
- 必须说明 raw sources 是 source of truth，knowledge 是编译产物。

执行步骤：
1. 检查当前仓库里 sources 的现状和命名风格。
2. 设计一个最小可行的长期 sources 目录，例如 sources/library/ 或等价结构。
3. 新增目录说明 README，以及最小索引/元数据模板。
4. 在知识文档里写清 raw sources、change sources、knowledge 的关系。
5. 补充最少量示例字段，方便后续 ingest 使用。

验收标准：
- 新目录结构清晰。
- 有 README 和模板，不是空目录。
- 文档明确“原始资料不可变，知识资产可演化”。

```

### 任务 2：新增 source ingest workflow

```text
只做这个任务：新增一个明确的 source ingest workflow，把“新资料进入仓库后如何更新知识库”写成可执行流程。

必要约束：
- 只做 ingest，不做 query 或 lint。
- 保留现有 OpenSpec/change 机制，不要发明第二套流程。
- 要明确输入、输出、人工确认点、失败处理。

执行步骤：
1. 阅读现有 harness/workflows 目录和 skills/README.md，保持风格一致。
2. 新增一个 source-ingest workflow 文档。
3. 工作流至少覆盖：接收入库、来源分级、claim 抽取、影响 topic 判断、change 建议、索引更新、日志追加。
4. 如有必要，补一份模板或示例输入结构。
5. 更新相关 README 或入口文档，让别人知道这个 workflow 存在。

验收标准：
- 仓库中出现独立 ingest workflow。
- 步骤可执行，不只是原则描述。
- 说明了与 change 流程的衔接点。
```

### 任务 3：把 log.md 变成一等公民

```text
只做这个任务：为知识库增加 append-only 的 log 机制，用来记录 ingest、query、lint 对知识库的影响。

必要约束：
- 不实现复杂数据库，只用 markdown 或 yaml 的最小方案。
- 日志必须能支持人工阅读和后续自动处理。
- 不能把 log 写成 changelog 的重复品。

执行步骤：
1. 在 knowledge/ 下合适的位置增加 log.md。
2. 设计统一日志条目格式，至少包含时间、动作类型、影响对象、来源/问题、结果、后续待办。
3. 补 README 说明何时写 log、何时不写。
4. 如现有脚本适合，补最小自动生成或追加建议；否则先用模板。
5. 更新 knowledge/README.md。

验收标准：
- 有实际 log 文件和固定格式。
- 文档清楚区分 log、change record。
- 后续 ingest/query/lint 可以直接复用它。
```

### 任务 4：让 index 真正可用 [已取消]

```text
indexes/ 已删除，不再维护独立索引文件。需要查找内容时直接 glob 或使用搜索工具。
```

### 任务 5：新增 lint workflow

```text
只做这个任务：增加知识库 lint workflow，用来定期发现结构和事实层面的健康问题。

必要约束：
- 先做 workflow 和检查项定义，不要求一次做成复杂脚本。
- 检查项必须贴合本仓库：证据、追溯、索引、术语、状态漂移、孤立页面。
- 要区分“自动能查的”和“需要人工判断的”。

执行步骤：
1. 新增 lint-knowledge-base workflow 文档。
2. 明确 lint 输入、输出、频率建议、产物位置。
3. 列出检查清单：broken links、占位索引、缺 frontmatter、claim/source 缺口、跨页矛盾、过期 planned 状态、术语漂移等。
4. 如合适，新增一个 lint report 模板。
5. 更新入口文档，让团队知道 lint 是正式操作模式。

验收标准：
- 仓库里有独立 lint workflow。
- 检查项可执行、可复核。
- 自动检查和人工检查边界清楚。
```

### 任务 6：把高价值 query 沉淀回 change

```text
只做这个任务：设计并落地一个“高价值问答 -> change 候选”的轻量机制。

必要约束：
- 不改变现有 change 主流程，只补 query 到 change 的桥接。
- 必须避免把每次聊天都写进仓库。
- 要定义“什么样的问题值得沉淀”。

执行步骤：
1. 设计一个轻量 query-to-change workflow 或规则文档。
2. 定义触发条件，例如：跨多个 topic、形成稳定结论、补齐明显知识空洞、形成新 comparison/decision。
3. 规定最小产物，例如 backlog 条目、change 建议模板或 request 草稿。
4. 说明人工确认点，避免无意义噪音入库。
5. 更新相关 README。

验收标准：
- 有明确的 query 沉淀规则。
- 定义了值得沉淀的问题类型。
- 能和 openspec/changes/ 无缝连接。
```

### 任务 7：加强 concept/entity pages 模型

```text
只做这个任务：增强仓库对跨 topic 概念/实体的建模能力。

必要约束：
- 不要大规模重构现有 knowledge 内容。
- 先补模型、目录说明、模板和索引规则。
- 必须兼容当前 topic-based 结构。

执行步骤：
1. 检查 glossary/meta/ 的现状。
2. 设计 concept/entity 的最小资产模型：放哪里、叫什么、和 topic 如何互链。
3. 新增模板或 README，说明什么适合成为 concept/entity page。
4. 补一个最小示例结构，但不要硬塞大量内容。

验收标准：
- concept/entity 有明确资产模型。
- 与 topic page 的边界清楚。
- 后续像 Bundler、EntryPoint、Paymaster 这类跨主题概念可以落地。
```

### 任务 8：增加“矛盾/替代/状态变化”元数据

```text
只做这个任务：为 claim 或 artifact 增加显式的冲突、替代、状态变化表达能力。

必要约束：
- 先做 schema/规则/模板层，不强迫全仓库批量迁移。
- 必须兼容现有 evidence 和 traceability 规则。
- 不能把“矛盾”写成模糊口头描述。

执行步骤：
1. 阅读 evidence-policy 和 traceability-policy。
2. 设计最小元数据字段，例如 supersedes、contradicts、status_changed_by、deprecated_by、confidence_note。
3. 把这些字段写进适当的规则、模板或示例中。
4. 说明何时使用、何时不用，避免滥用。
5. 更新 README 或规则索引引用。

验收标准：
- 仓库里有正式定义的冲突/替代表达方式。
- 与 evidence/traceability 能协同工作。
- 不要求一次性改旧文档。

```

### 任务 9：新增 research backlog / gap 池

```text
只做这个任务：把 evidence gap、missing primitive、待确认问题收敛成一个正式 backlog。

必要约束：
- backlog 必须是长期维护入口，不是临时 TODO。
- 必须能从 ingest、query、lint 三种动作汇总进来。
- 不能和 openspec/changes/ 的进行中任务混淆。

执行步骤：
1. 在 knowledge/ 下合适的位置增加 research-backlog.md。
2. 设计条目格式，至少包含类型、来源、相关 topic、优先级、建议动作、状态。
3. 明确 gap/backlog 与 change 的关系：什么时候升级为 change。
4. 更新知识库 README 和相关 workflow 文档。
5. 放入少量示例条目占位，展示格式。

验收标准：
- 仓库中有正式 backlog 文件。
- 条目格式统一，能承接后续自动化。
- 明确 backlog 和 change 的边界。

```

### 任务 10：补图片/图表来源资产处理

```text
只做这个任务：为图片、架构图、流程图等非纯文本来源补充归档与引用规范。

必要约束：
- 优先做目录、规则、元数据模板，不要求大规模导入资产。
- 必须和现有 diagrams 规则兼容。
- 要明确图片来源、版权/出处、关联 claim 或 diagram 的关系。

执行步骤：
1. 阅读 harness/rules/diagrams/ 和 scripts/diagrams/ 现状。
2. 设计图片/图表原始资产目录和元数据格式。
3. 说明原图、派生图、渲染图之间的关系。
4. 在 README 或 rules 中写明如何引用图片来源、如何追溯到 topic/claim。
5. 如有必要，补最小示例目录。

验收标准：
- 图片/图表有正式归档规则。
- 与 diagram workflow 不冲突。
- 能支持后续本地保存和追溯。

```

### 任务 11：增加本地搜索入口

```text
只做这个任务：为仓库增加一个简单但明确的本地搜索层。

必要约束：
- 先做轻量方案，优先复用 rg 或简单脚本。
- 不引入重型外部服务。

执行步骤：
1. 检查现有 scripts/ 和 README 是否已有搜索相关能力。
2. 新增一个最小搜索脚本或统一命令说明，支持按 topic、term、claim、source 等维度搜索。
3. 在 README 中说明搜索用法。
4. 给出 3 到 5 个清晰示例命令。
5. 运行至少一个示例验证结果。

验收标准：
- 仓库内有正式搜索入口，而不是零散命令。
- 文档可直接指导使用。
- 不依赖复杂基础设施。
```

### 任务 12：把 ingest/query/lint 写进系统操作模型

```text
只做这个任务：把 ingest / query / lint 三种运转模式正式写进仓库入口和配置说明。

必要约束：
- 不要重写 AGENTS.md 全文，只做最小增量修改。
- 必须与当前 task type、workflow、OpenSpec 模型兼容。
- 不能模糊掉 new-research / update-research / review / apply 这些现有概念。

执行步骤：
1. 修改 AGENTS.md 中“启动行为”“任务与路由”或等价章节，加入 ingest/query/lint 视角。
2. 如有必要，补充 openspec/config.yaml 或相关说明文档中的操作模型说明。
3. 说明它们与现有 change 流程的映射关系。
4. 保持术语一致，避免多套命名并存。
5. 检查全文是否仍清晰、简洁。

验收标准：
- 仓库入口文件明确出现 ingest/query/lint。
- 与现有 OpenSpec 任务模型关系明确。
- 不是重复描述，而是新增了可执行视角。
```

### 任务 13：统一 frontmatter / metadata 规范
```text
只做这个任务：为 artifact、verdict 等文档增加统一 frontmatter / metadata 规范。

必要约束：
- 先定义规范和模板，不强制一次性迁移所有旧文件。
- 字段要少而有用，服务于 lint、追溯。
- 不能和现有 HTML 注释元数据冲突不清。

执行步骤：
1. 检查当前 artifact.md、verdict.md 的元数据现状。
2. 设计一套最小 frontmatter 字段，例如 topic、type、domain、status、updated_at、source_count、related_topics。
3. 写入规则或模板说明，明确适用范围。
4. 选 1 到 2 个模板或示例文档演示新格式。
5. 更新相关 README 或检查脚本说明。

验收标准：
- frontmatter 规范明确、简洁、可扩展。
- 与 lint 有明确关系。
- 不要求立即全库迁移。
```

### 任务 14：补人审闸口和升级条件
```text
只做这个任务：把 human-in-the-loop 的评审闸口写清楚，特别是哪些更新必须人工确认。

必要约束：
- 不改变现有 review 概念，只把规则细化。
- 重点覆盖 decision 类结论、证据降级、跨主题冲突、状态变化。
- 规则要可执行，不是泛泛而谈。

执行步骤：
1. 阅读现有 review workflow 和 evidence/uncertainty 规则。
2. 新增或补充一份 review gate 规则，定义必须人工确认的场景。
3. 明确 L1/L2 不足、planned/shipped 状态变化、结论翻转、跨 topic 冲突时的处理方式。
4. 如合适，补一个 review checklist 或 decision gate 模板。
5. 更新相关入口说明。

验收标准：
- “哪些情况必须人审”被明确写出来。
- 和 review workflow 对齐。
- 能降低自动写入错误结论的风险。
```

### 任务 15：先把仓库定位写清楚
```text
只做这个任务：用最小改动把仓库定位从“研究写作仓库”提升为“把原始来源持续编译成知识资产的工作台”。

必要约束：
- 先做定位表述，不扩展流程细节。
- 修改应集中在 README/AGENTS 入口层。
- 文案要克制、准确，不写营销话术。

执行步骤：
1. 阅读 AGENTS.md、knowledge/README.md、openspec/changes/README.md 的开头部分。
2. 在最少的几个入口文件里补一段统一定位说明。
3. 强调三层关系：原始来源、过程 change、长期 knowledge。
4. 说明本仓库不是简单收集资料，而是持续编译知识。
5. 检查术语是否与现有 schema 一致。

验收标准：
- 新人读入口文件就能明白仓库定位。
- 文案不和现有 OpenSpec 模型冲突。
- 改动小但有效。
```