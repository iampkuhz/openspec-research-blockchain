# OpenSpec 运行分层

> 角色：运行说明版。仓库级结构约束分别见 [openspec/specs/repository-asset-model/spec.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/openspec/specs/repository-asset-model/spec.md) 与 [openspec/specs/canonical-output-model/spec.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/openspec/specs/canonical-output-model/spec.md)。

## 为什么要单独写这份说明

普通 OpenSpec 仓库里，大家通常会自然区分：

- `changes/change-name/`：当前改动包
- `specs/`：长期规范
- 业务代码或正式实现：长期结果

本仓库是研究仓库，不是软件实现仓库，所以这里需要把“长期结果”再拆成两类：

- `knowledge/analysis/`：长期事实分析资产
- `knowledge/decisions/`：长期场景决策资产

并统一挂在：

- `knowledge/`

同时，还要把“研究系统本身的长期规范”放进 `openspec/specs/`，而不是把它们混进某个具体 case。

## 四层分工

### 1. 工作流定义层

位置：

- `openspec/config.yaml`
- `openspec/schemas/blockchain-research/`

职责：

- 定义默认 schema
- 注入仓库级 context
- 定义产物关系图、依赖关系、模板和规则

这一层解决的是：研究流程怎么跑。

### 2. 研究系统 specs 层

位置：

- `openspec/specs/...`

职责：

- 存放可跨多次调研复用的准则、倾向和结构性规范
- 承接从多轮 change 中沉淀下来的通用经验

这一层解决的是：以后类似研究都该怎么做。

### 3. 当前研究改动层

位置：

- `openspec/changes/<change-name>/`

职责：

- 承载当前一轮研究改动
- 放置 `request.md`、`brief.md` 等过程文件
- 容纳一次具体补证、补图、改写、升级结论的工作过程
- 默认作为本地工作区使用

对标普通 OpenSpec：

- 它就是研究仓库里的 `changes/change-name/`

### 4. 长期正式资产层

位置：

- `knowledge/analysis/domains/...`
- `knowledge/analysis/primitives/...`
- `knowledge/analysis/synthesis/...`
- `knowledge/decisions/...`

职责：

- 承载长期维护的正式研究资产
- 作为后续研究和决策的长期依赖入口
- 承接被研究改动包验证过、值得长期保存的内容

保留规则：

- `knowledge/analysis/` 默认只保留 `analysis.md`、`glossary.md`，必要时保留 `dependencies.md`
- `knowledge/decisions/` 默认保留 `analysis.md`、`criteria.md`、`dependencies.md`、`glossary.md`、`verdict.md`
- `request.md`、`brief.md`、`sources.md`、`evidence-matrix.md`、case 级 `README.md` 默认不进入长期目录

但这层内部还要再拆：

- `knowledge/analysis/...`：长期正式技术知识
- `knowledge/decisions/...`：长期场景应用产出

## 当前仓库里的示例 case 属于哪一层

当前 `knowledge/analysis/` 和 `knowledge/decisions/` 下的示例 case 属于：

- 长期正式资产层

它们的作用不是模拟一次正在进行的 `change`，而是定义：

- 长期目录结构应该长什么样
- 每类对象长期保留哪些文件
- 上层研究如何声明依赖和研究预算

与此同时，`openspec/changes/` 只保留目录级说明；具体 change packet 由每次研究临时创建。

## 推荐操作方式

### 新开一个研究主题

1. 先决定未来的正式结果是进入 `knowledge/analysis/` 还是 `knowledge/decisions/`
2. 再在 `openspec/changes/<change-name>/` 开本轮 change packet
3. 在 change packet 中完成本轮 request / brief / sources / analysis / verdict 等过程
4. 将稳定下来的 durable 结果提炼进 `knowledge/analysis/` 或 `knowledge/decisions/`

### 修改一个已有正式 case

1. 不建议直接把大量工作草稿堆进 `knowledge/analysis/` 或 `knowledge/decisions/`
2. 先开一个新的 `openspec/changes/<change-name>/`
3. 在 change packet 中完成补证、改写、结论升级
4. 再把结果合并进对应的 canonical 目录

### 沉淀新的研究系统准则

1. 开一个新的 `openspec/changes/<change-name>/`
2. 在 change packet 中说明为什么当前规则需要调整
3. 将稳定下来的原则回写到 `openspec/specs/<spec-name>/spec.md`
4. 同步更新 `README.md`、`AGENTS.md`、`openspec/config.yaml`、`support/docs/`

## 为什么现在改成 `primitive -> [optional synthesis] -> domain`，而把 `decision` 独立出来

更准确的理解是：

- 技术分析主链：`primitive -> [optional synthesis] -> domain`
- 场景应用层：`decision`

原因是：

- `domain` 仍然属于技术分析体系的一部分，它负责长期主题组织和知识聚合
- `synthesis` 并不是强制层，只有在关系分析本身值得长期维护时才单独存在
- `decision` 已经不是纯技术分析对象，而是把知识资产应用到具体场景中的判断产物

## 为什么不让 domain 变成路径父级

因为一个 `primitive` 或 `synthesis` 完全可能被多个 `domain` 复用。

所以：

- `knowledge/analysis/primitives/` 和 `knowledge/analysis/synthesis/` 应保持相对扁平
- 与哪些 `domain` 相关，应通过元数据、链接和 dependency map 声明
