# 研究对象模型规范

## 研究类型定义

### primitive（原语）

**定义**：底层机制研究，关注单一对象的技术实现细节。

**研究重点**：
- 核心术语定义
- 组件架构与分层
- 执行流程
- 设计取舍
- 能力边界（protocol-native / official / third-party）

**交付物**：
- `artifact.md`：机制分析文档

**研究深度**：
- deep：全面深挖，产出可复用的 reference
- focused：针对特定问题深入，不追求全面
- light：快速了解，确认基本事实

**深度标记**：primitive artifact 必须在文档开头标注研究深度

### synthesis（合成）

**定义**：演进或综合分析，关注多个对象之间的关系和发展脉络。

**研究重点**：
- 演进框架（时间线、阶段划分）
- 各对象定位（问题层、状态）
- 演进关系分析（替代/互补/演进）
- 趋势判断

**交付物**：
- `artifact.md`：演进分析文档
- 演进图（PlantUML 时间线图）

**依赖要求**：
- 必须显式声明对 primitive 的依赖
- 必须检查每个依赖 primitive 的深度是否满足需求
- 如果 primitive 缺失或深度不足，必须在 plan 中规划补充调研

### domain（主题域）

**定义**：主题域定义，关注问题空间的划分和边界。

**研究重点**：
- 问题簇划分
- 与相邻 domain 的关系
- 价值定位

**交付物**：
- `reference.md`：域定义文档

### decision（决策）

**定义**：场景决策，关注特定场景下的选型或判断。

**研究重点**：
- 场景定义
- 比较维度
- 有限结论（条件性 verdict）

**交付物**：
- `verdict.md`：条件性结论文档
- `criteria.md`：决策标准（可选）

**依赖要求**：
- 必须显式声明对下层研究的依赖
- 依赖深度必须满足决策需求

## 研究路径定义

### deep-dive

深度研究单一对象，产出完整的机制分析。

适用类型：primitive

### evolution

分析多个对象的演进关系和发展脉络。

适用类型：synthesis

### scenario

针对特定场景进行比较或选型。

适用类型：decision

### domain overview

定义主题域的范围和问题簇。

适用类型：domain

## 研究深度定义

### deep

- 全面深挖，产出可复用的 reference
- 覆盖机制完整性、设计原因、边界定义
- 适用于核心 primitive 或关键 synthesis

### focused

- 针对特定问题深入，不追求全面
- 适用于有明确边界的子问题
- 适用于非核心 primitive

### light

- 快速了解，确认基本事实
- 适用于辅助性对象或初步探索
- 适用于已有研究的引用参考

## 依赖管理规范

### 依赖声明原则

1. **上层不重复下层**：synthesis/decision 只引用 primitive 的结论，不重复其完整机制分析
2. **明确抽取边界**：每个依赖说明"引用什么"而不是"复制什么"
3. **深度匹配**：依赖的 primitive 深度必须满足上层研究需求
4. **动态补充**：如果 primitive 缺失或深度不足，必须在 plan 中规划补充调研

### 依赖检查流程

在 plan 阶段，必须完成以下检查：

1. **列出所有依赖**：明确本次研究依赖哪些下层对象
2. **评估当前状态**：
   - 检查 knowledge 中是否存在该对象的 artifact
   - 如果存在，检查其研究深度
3. **判断差异**：
   - 如果当前深度 >= 所需深度：直接引用
   - 如果当前深度 < 所需深度：规划补充调研
4. **规划补充**：在 plan 中明确补充调研的范围和深度

### 依赖表格规范

```markdown
### 依赖对象列表

| 对象 | 类型 | 当前状态 | 所需深度 | 当前深度 | 差异处理 |
|------|------|----------|----------|----------|----------|
| EIP-4337 | primitive | 已存在 | deep | deep | 直接引用 |
| EIP-7702 | primitive | 已存在 | deep | light | 补充调研 |
| EIP-7560 | primitive | 不存在 | focused | none | 新建调研 |
```

### 补充调研规划

如果存在深度不足的依赖，必须在 plan 中规划补充调研：

```markdown
### 补充调研计划

| 对象 | 当前深度 | 所需深度 | 补充范围 | 优先级 |
|------|----------|----------|----------|--------|
| EIP-7702 | light | deep | 核心机制、与 4337 关系 | 高 |
```

## 前置检查逻辑

### synthesis/decision 前置检查

在开始 synthesis/decision 研究前，必须完成：

1. **依赖清单**：列出所有依赖的 primitive
2. **深度评估**：评估每个 primitive 的当前深度
3. **差异分析**：识别深度不足的 primitive
4. **补充规划**：在 plan 中规划补充调研

**重要原则**：
- 不能因为当前没调研过某个 primitive 就降低要求
- 必须按照本次调研的需求明确依赖的数据
- 缺少或深度不足**必须**要补充

### primitive 前置检查

在开始 primitive 研究前，必须完成：

1. **类型确认**：确认是新建还是补充
2. **深度确认**：如果是补充，明确补充范围
3. **依赖确认**：确认对相邻 primitive 的依赖

## 深度标记规范

### primitive artifact 深度标记

每个 primitive artifact 必须在文档开头标注研究深度：

```markdown
<!--
研究深度：deep / focused / light
对象类型：primitive
研究路径：deep-dive
-->
```

或在 YAML frontmatter 中标记：

```markdown
---
research_depth: deep
object_type: primitive
research_path: deep-dive
---
```

### 深度标记的使用

上层研究在引用 primitive 时，应检查其深度标记：

- 如果深度满足需求：直接引用
- 如果深度不足：规划补充调研

### 深度升级

primitive 可以通过补充调研升级深度：

- light → focused：补充特定方面的深入分析
- focused → deep：扩展为全面分析
- 升级后的 artifact 应更新深度标记

## 文件结构规范

### change packet 结构

```
openspec/changes/{change-name}/
├── request.md      # 研究问题定义
├── plan.md         # 研究计划（含依赖声明、证据矩阵）
├── draft.md        # 研究草稿
└── .openspec.yaml  # change 元数据
```

### knowledge 结构

```
knowledge/
├── analysis/
│   ├── primitives/
│   │   └── {category}/
│   │       └── {object-type}-{name}/
│   │           └── artifact.md  # 带深度标记
│   ├── synthesis/
│   │   └── {category}/
│   │       └── {synthesis-type}-{name}/
│   │           └── artifact.md
│   └── domains/
│   │   └── {domain-type}-{name}/
│   │       └── reference.md
│   └── decisions/
│       └── {decision-type}-{name}/
│           ├── artifact.md
│           ├── criteria.md（可选）
│           └── verdict.md
```

### 目录命名规范

#### primitives 目录

**二级分类**：primitives 下必须按技术领域设置二级分类。

**分类定义**：

| 分类名 | 说明 | 命名前缀 | 示例 |
|--------|------|----------|------|
| `consensus` | 共识算法 | `consensus-` | consensus-malachite, consensus-tendermint |
| `account-abstraction` | 账户抽象 | `aa-` | aa-eip-4337, aa-eip-7702 |
| `mempool` | 内存池机制 | `mempool-` | mempool-p2p, mempool-encrypted |
| `staking` | 质押机制 | `staking-` | staking-slashing, staking-rewards |
| `bridge` | 跨链桥 | `bridge-` | bridge-IBC, bridge-layerzero |
| `agentic-payment` | 代理支付 | `agentic-payment-` | agentic-payment-a2a, agentic-payment-x402 |

**命名格式**：`{category-prefix}-{name}`

- `{category-prefix}`: 分类前缀（见上表）
- `{name}`: 具体名称（小写，连字符分隔）

**示例**：
- `consensus-malachite` ✓
- `consensus-tendermint` ✓
- `consensus-qbft` ✓
- `consensus-simplex` ✓
- `aa-eip-4337` ✓
- `malachite` ✗（缺少分类前缀）
- `eip-4337` ✗（缺少分类前缀）

#### synthesis 目录

**二级分类**：synthesis 下必须按分析类型设置二级分类。

**分类定义**：

| 分类名 | 说明 | 命名前缀 | 示例 |
|--------|------|----------|------|
| `comparison` | 对比分析 | `comparison-` | comparison-bft-consensus |
| `evolution` | 演进分析 | `evolution-` | evolution-aa-eip |
| `taxonomy` | 分类学分析 | `taxonomy-` | taxonomy-agentic-payment |

**命名格式**：`{category-prefix}-{name}`

- `{category-prefix}`: 分类前缀（见上表）
- `{name}`: 描述性名称（小写，连字符分隔）

**示例**：
- `comparison-bft-consensus` ✓
- `evolution-aa-eip` ✓
- `bft-consensus` ✗（缺少分类前缀）
- `aa-eip-evolution` ✗（缺少分类前缀）

#### domain 目录

**二级分类**：domain 下按主题域划分，可选二级分类。

**命名格式**：`domain-{name}`

**示例**：
- `domain-account-abstraction` ✓
- `domain-consensus` ✓
- `account-abstraction` ✗（缺少 `domain-` 前缀）

#### decision 目录

**二级分类**：decision 下按场景域划分，建议设置二级分类。

**命名格式**：`decision-{scenario}`

**示例**：
- `decision-aa-wallet-selection` ✓
- `decision-consensus-selection` ✓
- `chain-comparison` ✗（缺少 `decision-` 前缀）

### 命名原则

1. **区分度优先**：名称必须能清晰区分不同对象，避免使用过短的通用名称
2. **分类前缀必需**：所有 primitive/synthesis/domain/decision 名称必须包含分类前缀
3. **小写 + 连字符**：统一使用小写字母和连字符（`-`），不使用下划线或空格
4. **英文优先**：使用英文术语，便于与国际技术文档对齐
5. **缩写规范**：对于长分类名，可定义标准缩写（如 `account-abstraction` → `aa-`）

### 现有分类注册表

以下为本仓库已注册的分类和前缀：

#### primitives 分类

| 分类 | 前缀 | 状态 | 包含对象 |
|------|------|------|----------|
| consensus | `consensus-` | active | consensus-malachite, consensus-simplex, consensus-tendermint, consensus-qbft, consensus-malaketh-turbo |
| account-abstraction | `aa-` | active | aa-eip-4337, aa-eip-7560, aa-eip-7702 |
| agentic-payment | `agentic-payment-` | active | agentic-payment-a2a, agentic-payment-acp, agentic-payment-ap2, agentic-payment-mpp, agentic-payment-x402 |

#### synthesis 分类

| 分类 | 前缀 | 状态 | 包含对象 |
|------|------|------|----------|
| comparison | `comparison-` | active | comparison-bft-consensus |
| evolution | `evolution-` | active | evolution-aa-eip |
| taxonomy | `taxonomy-` | active | taxonomy-agentic-payment |
