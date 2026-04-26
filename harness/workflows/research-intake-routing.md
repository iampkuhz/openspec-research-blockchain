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

### 步骤 4：判断 change_operation

判断是新建还是更新：
- `create`：新研究
- `update`：更新已有 knowledge

### 步骤 5：拆分 child changes（如适用）

复杂任务必须拆成多个 child changes。

**示例**：

```
用户需求：对比 Tendermint / HotStuff / Simplex 并做低延迟联盟链选型
输出：
- primitive change: Tendermint
- primitive change: HotStuff
- primitive change: Simplex
- synthesis change: BFT consensus comparison
- decision change: low-latency consortium chain choice
```

拆分原则：
- 每个 primitive 独立一个 change
- synthesis 依赖其引用的所有 primitive
- decision 依赖其引用的所有 primitive 和 synthesis

### 步骤 6：初始化 change.yaml

使用 `openspec/schemas/blockchain-research/templates/change.yaml` 模板实例化：
- 声明 task_type
- 声明 change_operation
- 声明 execution_scope
- 声明 artifacts 路径
- 声明 validators

### 步骤 7：生成 request.md

使用 `openspec/schemas/blockchain-research/templates/request.md` 模板：
- 研究对象类型明确（primitive / synthesis / decision）
- 研究路径明确（deep-dive / evolution / scenario）
- 3-5 个开放性核心问题
- 范围边界（覆盖什么、不覆盖什么）
- 预期输出

### 步骤 8：生成 plan.md

使用 `openspec/schemas/blockchain-research/templates/plan.md` 模板：
- 研究深度声明（deep / focused / light）
- 来源分层规划（L1/L2/L3/L4）
- 图表规划（每张图的必要性）
- 证据缺口声明
- 完成标准

### 步骤 9：不生成 draft.md

本阶段只产出 request.md 和 plan.md，不提前写分析正文。

### 步骤 10：不写 knowledge/**

禁止直接修改 knowledge/ 主线。

---

## 完成后进入

- `/spec-research-step`：继续 sources / draft / review
- 如拆了 child changes：依次执行每个 child change 的 step
