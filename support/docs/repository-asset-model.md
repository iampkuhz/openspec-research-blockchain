# 仓库资产模型

> 角色：说明版。仓库级硬规范见 [openspec/specs/repository-asset-model/spec.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/openspec/specs/repository-asset-model/spec.md)。

## 先说结论

这个仓库里不止四类研究对象，而是至少六类“仓库资产”：

1. 工作流定义资产
2. 研究系统 specs
3. 当前改动资产
4. 长期技术分析资产
5. 长期场景决策资产
6. 支撑方法资产

如果硬要和 spec-driven SDD 对齐，不能机械做 1:1 映射；更合理的是先看“它们在仓库里分别承担什么角色”。

## 六类资产

### 1. 工作流定义资产

位置：

- `openspec/config.yaml`
- `openspec/schemas/blockchain-research/`

作用：

- 定义 schema
- 定义产物关系图
- 定义规则、模板和 prompt 约束

这类资产回答的是：研究流程怎么跑。

### 2. 研究系统 specs

位置：

- `openspec/specs/`

作用：

- 沉淀跨多次调研可复用的研究原则
- 形成研究系统本身的长期规范

这类资产回答的是：以后类似研究都该怎么做。

### 3. 当前改动资产

位置：

- `openspec/changes/<change-name>/`

作用：

- 承载本轮正在进行的研究改动包
- 容纳工作草稿、纠偏记录、补证过程和过程性判断
- 默认作为本地工作区使用，可在版本库中只保留 `README.md`

这类资产回答的是：这次具体改了什么。

### 4. 长期技术分析资产

位置：

- `knowledge/analysis/primitives/`
- `knowledge/analysis/synthesis/`
- `knowledge/analysis/domains/`

作用：

- 承载长期正式技术知识
- 构成技术分析主链：`primitive -> [optional synthesis] -> domain`
- 只保留 stable 结果，不保留 `request.md`、`brief.md`、`sources.md`、`evidence-matrix.md`、case 级 `README.md`

这类资产最接近 SDD 里的长期 `specs` 与知识底座。

### 5. 长期场景决策资产

位置：

- `knowledge/decisions/`

作用：

- 在具体场景里消费技术分析资产
- 结合需求、约束、候选方案做判断
- 只保留 stable 结果，不保留 `request.md`、`brief.md`、`sources.md`、`evidence-matrix.md`、case 级 `README.md`

它不等于 SDD 里的 `code`，但如果一定要找“最接近应用层结果”的东西，它比 `knowledge/analysis/` 更接近“把知识真正拿来用”的那一层。

补充一层：

- `knowledge/` 是长期正式产出的共同父目录
- 它的作用是把正式产出与 `openspec/changes/`、`openspec/specs/`、`support/` 清楚分开

### 6. 支撑方法资产

位置：

- `support/docs/`
- `support/templates/`
- `support/prompts/`
- `skills/`

作用：

- 沉淀方法论
- 提供写作模板
- 提供 AI 协作入口

其中：

- `support/` 负责把同类支撑资产收在同一个父目录下
- `skills/` 因客户端常有固定目录约束，所以作为顶层例外保留

## 与 spec-driven SDD 的对应关系

| spec-driven SDD | 本仓库里的最接近对应物 | 说明 |
| --- | --- | --- |
| `changes/` | `openspec/changes/<change-name>/` | 几乎是直接对应 |
| `specs/` | `openspec/specs/` + `knowledge/analysis/` | 前者是研究系统 specs，后者是长期技术分析资产 |
| `code/` | 无严格 1:1 对应；最接近的是 `knowledge/decisions/` | 决策资产是在应用知识，但不是可执行代码 |
| `config / schema / workflow` | `openspec/config.yaml` + `openspec/schemas/...` | 直接对应工作流定义层 |

## 为什么这里没有严格意义上的 code 层

因为这个仓库的主要目标不是交付软件实现，而是交付可复用的研究资产。

所以：

- `knowledge/analysis/` 是长期知识底座
- `knowledge/decisions/` 是把知识底座应用到场景中的产物
- 但它仍然不是软件代码

如果未来你在仓库里加入：

- 数据抓取脚本
- 证据整理脚本
- 表格生成脚本
- 自动化校验工具

那时才会出现真正意义上的 `scripts/` 或 `tools/` 代码层。
