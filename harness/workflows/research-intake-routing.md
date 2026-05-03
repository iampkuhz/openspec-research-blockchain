# Research Intake Routing — `/spec-research` 执行规约

**对应 Command**：`/spec-research`
**输出**：`change.yaml`、`request.md`、`plan.md`

---

## 执行逻辑

### 步骤 1：读取用户需求

接收用户的研究意图，明确要研究什么。

### 步骤 2：读取 openspec 配置

读取 `openspec/config.yaml` 与 `openspec/schemas/blockchain-research/schema.yaml`，确认：
- 当前 schema 支持的 artifact 类型
- change 模板结构
- apply 规则

### 步骤 3：判断 task_type

根据用户需求判断属于哪类研究：

| task_type | 适用场景 |
|---|---|
| `source_reading` | 阅读并消化单个或多个来源 |
| `primitive` | 单个协议/机制/产品的底层研究 |
| `synthesis` | 多个 primitive 的横向对比或演进分析 |
| `decision` | 场景驱动的选型或决策分析 |

长期 Knowledge research change 的新建 ID 只使用 `primitive`、`synthesis`、`decision` 三类前缀。

### 步骤 4：拆分 child changes（如适用）

复杂任务必须拆成多个 child changes。

**示例**：

```
用户需求：对比 Tendermint / HotStuff / Simplex 并做低延迟联盟链选型
输出：
- primitive change: primitive_blockchain-consensus_tendermint
- primitive change: primitive_blockchain-consensus_hotstuff
- primitive change: primitive_blockchain-consensus_simplex
- synthesis change: synthesis_blockchain-consensus_bft-comparison
- decision change: decision_blockchain-consensus_low-latency-choice
```

拆分原则：
- 每个 primitive 独立一个 change
- synthesis 依赖其引用的所有 primitive
- decision 依赖其引用的所有 primitive 和 synthesis

### 步骤 5：检查已有 change

在创建新 change 之前，必须先检查 `openspec/changes/` 下是否已有同主题的 change：

1. 为每个候选 child change 先确定 `task_type`、`domain_id`、`topic_slug` 和 3-8 个主题关键词。
2. 搜索范围是 `openspec/changes/` 的直接子目录，不包含 `archive/`。
3. 同时检查目录名、`change.yaml` 的 `id` / `task_type` / `publish_targets`、`request.md` 标题和 `plan.md` 标题。
4. 匹配时同时兼容新旧命名：
   - 新格式：`<task-type>_<domain-id>_<topic-slug>`
   - 旧格式：`<task-type>-<domain-or-topic...>`
   - 缺 task-type 的历史目录：当标题、publish target 或关键词高度重合时也视为候选重复。
5. 如果存在匹配且状态未完成（缺少 `draft.md`、`review.md`、`publish.md` 任一文件，或 review verdict 为 `needs revision`，或 publish target 尚未写入 `knowledge/**`），**继续推进该已有 change**，禁止新建。
6. 如果存在匹配且已完成，询问用户是要创建新 change（`extend` / `update`）还是刷新已有 knowledge。
7. 只有在无匹配时才创建新的。

**此步骤对每个 child change 分别执行。**

**如果步骤 5 决定继续推进已有 change，则跳过步骤 7 的 ID 创建，直接复用已有目录。change.yaml 的 `id` 保持不变，即使其命名不符合步骤 7 的新格式；不得因为历史命名不合规而新建重复 change。**

### 步骤 6：判断 change_operation

判断是新建还是更新：
- `create`：新研究
- `update`：更新已有 knowledge

### 步骤 7：确定 change ID

新建 change 时，ID 必须遵循以下格式：

```
<task-type>_<domain-id>_<topic-slug>
```

| 字段 | 说明 | 规则 |
|------|------|------|
| `task-type` | 研究类型标识 | `primitive` / `synthesis` / `decision` |
| `domain-id` | 研究领域标识 | kebab-case，如 `blockchain-integration` |
| `topic-slug` | 具体主题标识 | kebab-case，2-4 个词 |

**正确示例**：

| task_type | domain | topic | change ID |
|-----------|--------|-------|-----------|
| primitive | blockchain-integration | public-chain-architecture | `primitive_blockchain-integration_public-chain-architecture` |
| synthesis | blockchain-integration | integration-guide | `synthesis_blockchain-integration_integration-guide` |
| decision | blockchain-consensus | low-latency-choice | `decision_blockchain-consensus_low-latency-choice` |

**禁止格式**：

| 错误格式 | 示例 | 问题 |
|----------|------|------|
| 缺少 task-type 前缀 | `public-chain-architecture` | 无法从目录名判断研究类型 |
| 缺少 domain 层 | `primitive_public-chain-architecture` | domain 是必需的分组维度 |
| task-type 用 `-` 连接 | `primitive-public-chain-architecture` | task-type 后必须用 `_` 不是 `-` |
| domain/topic 内部用 `_` | `primitive_blockchain_integration_public_chain_architecture` | domain-id 和 topic-slug 内部必须用 `-` |

**执行校验**：
1. change ID 必须匹配正则 `^(primitive|synthesis|decision)_[a-z0-9-]+_[a-z0-9-]+$`。
2. 创建 change.yaml 前，必须校验 `id` 字段符合此格式。
3. change 目录名必须与 `id` 完全一致。
4. 该校验只适用于新建 change；继续推进历史 change 时不重命名目录。

### 步骤 8：初始化 change.yaml

使用 `openspec/schemas/blockchain-research/templates/change.yaml` 模板实例化：
- 声明 task_type
- 声明 change_operation
- 声明 execution_scope
- 声明 artifacts 路径
- 声明 validators

### 步骤 9：生成 request.md

使用 `openspec/schemas/blockchain-research/templates/request.md` 模板：
- 研究对象类型明确（primitive / synthesis / decision）
- 研究路径明确（deep-dive / evolution / scenario）
- 3-5 个开放性核心问题
- 范围边界（覆盖什么、不覆盖什么）
- 预期输出

同时遵守 `harness/rules/artifacts/request-rules.md`。如果是二次研究，既有 artifact 只能作为参考基线，request 不得切断新来源搜索或回源验证。

### 步骤 10：生成 plan.md

使用 `openspec/schemas/blockchain-research/templates/plan.md` 模板：
- 研究深度声明（deep / focused / light）
- 来源分层规划（L1/L2/L3/L4）
- 图表规划（每张图的必要性）
- 证据缺口声明
- 完成标准

### 步骤 11：不生成 draft.md

本阶段只产出 request.md 和 plan.md，不提前写分析正文。
在 `/spec-research` 端到端场景中，本阶段应作为 intake capsule 执行，完成后停止并把来源 handoff 交回主会话。

### 步骤 12：不写 knowledge/**

禁止直接修改 knowledge/ 主线。

---

## 完成后进入

- `/spec-research-step`：继续 sources / draft / review
- 如拆了 child changes：依次执行每个 child change 的 step
