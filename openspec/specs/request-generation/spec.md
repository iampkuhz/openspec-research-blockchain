# Request 阶段规范

## 目的

定义本仓库 blockchain research change 中 `request.md` artifact 的正式规则，包括：
- request 在 research change 中的定位
- 进入 request 阶段的前置条件
- request 必须满足的形式要求
- request 完成标准

## 适用范围

本规范适用于本仓库所有 research change 的 request 阶段。

## request.md 的定位

`request.md` 是 research change 的起点 artifact，负责：
- 定义研究意图与问题边界
- 明确"为什么要研究"和"要回答什么"
- 作为主流程 `request -> plan -> draft -> artifact` 的入口交付物

**`request.md` 是研究意图定义，不是分析正文**。

## 进入 request 阶段的前置条件

必须满足以下条件方可进入 request 阶段：

1. **研究意图已萌芽**
   - 有明确的研究触发原因或问题意识

2. **change 目录已创建**
   - `openspec/changes/<change-name>/` 目录已存在

## request 阶段的正式要求

### 研究对象类型要求

必须明确声明研究对象类型：

| 类型 | 说明 | 交付重点 |
|------|------|----------|
| primitive | 底层机制/协议 | 组件架构、核心流程、设计取舍、能力边界 |
| synthesis | 演进/综合分析 | 演进框架、各对象定位、演进关系、趋势判断 |
| domain | 主题域 | 问题簇、与相邻 domain 关系、价值定位 |
| decision | 场景决策 | 场景定义、比较维度、有限结论 |

### 研究路径要求

必须声明研究路径：

- `deep-dive`：深度机制分析
- `evolution`：演进脉络梳理
- `scenario`：场景化分析
- `domain overview`：领域概览

### 核心问题要求

必须用 3 到 5 个问题描述研究目标：

- 问题必须是**开放性问题**，不是 Yes/No 问题
- 问题应与对象类型匹配：
  - primitive：核心机制、与相邻协议关系、能力边界
  - synthesis：演进脉络、对象关系定位、未来趋势
  - domain：问题簇划分、与相邻 domain 边界
  - decision：选型标准、选项优劣、适用场景

### 范围边界要求

必须明确以下内容：

**覆盖范围**：
- 覆盖对象：列出本次研究覆盖的具体对象
- 覆盖链/协议：如适用，列出覆盖的链或协议
- 时间窗口：研究的时间范围

**非目标**：
- 明确不回答的问题，避免研究范围蔓延
- 示例：
  - primitive：不覆盖具体产品的实现细节
  - synthesis：不深入每个对象的完整机制
  - decision：不生成绝对化的推荐结论

### 已知输入要求

必须记录手上已有的资料：

- 已有的资料、经验判断或直接背景
- synthesis/decision 类型建议列出：
  - 已有的 primitive 研究
  - 已有的 domain/synthesis 研究
  - 外部参考资料

### 预期输出要求

必须说明预期产出类型，且与对象类型匹配：

| 对象类型 | 预期输出 |
|----------|----------|
| primitive | `artifact.md`（机制分析） |
| synthesis | `artifact.md`（演进分析）+ 演进图 |
| domain | `artifact.md`（域定义） |
| decision | `verdict.md`（条件性结论） |

### 触发原因要求

必须说明研究触发原因：
- 新场景出现
- 需要上层判断
- 已有材料不足
- 规范发生变化

## request 阶段完成标准

request 阶段视为完成，当且仅当：

1. **对象类型明确**
   - 已声明对象类型（primitive / synthesis / domain / decision）
   - 已声明研究路径

2. **核心问题清晰**
   - 3 到 5 个开放性问题已定义
   - 问题与对象类型匹配

3. **范围边界具体**
   - 覆盖对象、协议、时间窗口已列出
   - 非目标已明确

4. **输入输出完备**
   - 已知输入已记录
   - 预期输出与对象类型匹配
   - 触发原因已说明

## 与上位规范的关系

本规范是以下规范的 request 阶段特化：

| 上位规范 | 约束范围 |
|----------|----------|
| `openspec/schemas/blockchain-research/schema.yaml` | change 整体结构 |
| `openspec/specs/language-style/spec.md` | 语言风格 |

本规范不重复上位规范的正文，仅定义：
- request 阶段的入口条件
- request 阶段的形式要求
- request 阶段的完成标准

## 相关规范

- `openspec/schemas/blockchain-research/templates/request.md` —— request 模板
- `openspec/specs/language-style/spec.md` —— 语言风格
