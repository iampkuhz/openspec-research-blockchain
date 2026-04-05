# Plan 阶段规范

## 目的

定义本仓库 blockchain research change 中 `plan.md` artifact 的正式规则，包括：
- plan 在 research change 中的定位
- 进入 plan 阶段的前置条件
- plan 必须满足的形式要求
- plan 完成标准

## 适用范围

本规范适用于本仓库所有 research change 的 plan 阶段。

## plan.md 的定位

`plan.md` 是 research change 的第一轮集中 review artifact，负责：
- 将 request 中的研究意图转化为可执行计划
- 合并研究计划与来源规划为单一交付物
- 作为从 request 阶段迈向 draft 阶段的过渡交付物

**`plan.md` 是 review 文件，不是分析正文**。

## 进入 plan 阶段的前置条件

必须满足以下条件方可进入 plan 阶段：

1. **request.md 已成型**
   - `request.md` 已存在且研究意图清晰

2. **问题可拆解为可执行计划**
   - 研究对象可以被拆解为具体的研究路径

## plan 阶段的正式要求

### 结构要求

`plan.md` 必须包含以下章节：

1. 研究对象（类型、路径、相关 domains）
2. 问题拆解
3. 待确认问题
4. 交付范围
5. 研究深度（deep/focused/light）
6. 来源规划（L1/L2/L3/L4）
7. 证据缺口
8. 完成标准
9. 排除范围

**可选章节（依研究类型而定）**：
- 依赖声明（synthesis/decision 必需）
- 证据矩阵（复杂研究推荐）

### 研究对象要求

必须明确声明：
- **对象类型**：domain / primitive / synthesis / decision
- **研究路径**：deep-dive / evolution / scenario / domain overview
- **相关 domains**：可多个

### 待确认问题要求

**primitive 类型必须覆盖**：
- 设计选择类：为什么选择当前架构路径
- 能力边界类：哪些声称的能力依赖外部假设

**synthesis/decision 类型必须覆盖**：
- 演进关系类：各对象的关系定位（替代/互补/演进）
- 问题分层类：各对象解决的问题层
- 依赖缺口类：哪些 primitive 缺失或深度不足

### 来源规划要求

来源必须按以下层级组织：

| 层级 | 类型 | 示例 |
|------|------|------|
| L1 | 规范层 | spec / EIP |
| L2 | 实现层 | repo / docs |
| L3 | 生态层 | blog / release |
| L4 | 解读层 | analysis |

**来源链接要求**：
- 每条来源必须附可点击链接
- 如无法确认准确 URL，必须标注 `[待补链接：原因]`，不得只写纯文字描述
- L3/L4 层链接如无法验证，必须标注 `[未验证]`
- L1/L2 层链接应优先验证，如无法验证同样标注 `[未验证]`
- 严禁写入未经核实的推测 URL

**来源规划表结构**：三列 `来源 | 类型 | 说明`，不得加"状态"列（plan 阶段全部是 pending）

### 图表规划要求

`交付范围` 章节中必须显式列出图表类 deliverable：

- **组件图（必须）**：展示角色/组件/层级关系
- **流程图（可选）**：时序图，展示核心执行路径，必须明确标注"可有可无"或"必须"
- **对比表/归属表（推荐）**：能力归属、链适配对比等结构化表格

**原则**：
- 多用图表辅助阅读
- 每张图/表必须有独立的信息价值

### 研究深度要求

必须声明研究深度：

| 深度 | 说明 |
|------|------|
| deep | 全面深挖，产出可复用的 reference |
| focused | 针对特定问题深入，不追求全面 |
| light | 快速了解，确认基本事实 |

**synthesis/decision 类型**：需对每个依赖的 primitive 声明所需深度。

### 依赖声明要求（synthesis/decision 必需）

上层研究必须显式声明对下层 primitive 的依赖：
- 如果 primitive 缺失或深度不足，必须在 plan 中规划补充调研，不能降低要求

### 证据缺口要求

必须列出：
- 缺失的关键材料
- 缺失的实现证据
- 相互矛盾之处

### 风格要求

- 中文优先，英文术语优先保留
- 不提前写分析正文
- 不提前给确定性结论

## plan 阶段完成标准

plan 阶段视为完成，当且仅当：

1. **结构完整**
   - 包含所有必须章节
   - 章节顺序符合模板要求

2. **来源合规**
   - 所有来源按 L1/L2/L3/L4 层级组织
   - 每条来源附可点击链接或 `[待补链接：原因]`
   - 无法验证的链接已标注 `[未验证]`

3. **待确认问题完备**
   - primitive 类型已覆盖设计选择类和能力边界类问题
   - synthesis/decision 类型已覆盖演进关系、问题分层、依赖缺口类问题

4. **图表规划清晰**
   - `交付范围` 已显式列出所有图表 deliverable
   - 每张图/表的用途和必要性已说明

5. **完成标准包含以下固定项**：
   - `[ ] draft.md 包含【参考资料】章节，每条来源均附可点击链接`
   - `[ ] 所有链接已通过工具验证存活，或明确标注 [未验证] 并说明原因`

## 与上位规范的关系

本规范是以下规范的 plan 阶段特化：

| 上位规范 | 约束范围 |
|----------|----------|
| `openspec/schemas/blockchain-research/schema.yaml` | change 整体结构 |
| `openspec/specs/language-style/spec.md` | 语言风格 |
| `openspec/specs/evidence-policy/spec.md` | 证据政策 |
| `openspec/specs/diagram-policy/spec.md` | 图表政策（plan 阶段的图表规划） |

本规范不重复上位规范的正文，仅定义：
- plan 阶段的入口条件
- plan 阶段的形式要求
- plan 阶段的完成标准

## 相关规范

- `openspec/schemas/blockchain-research/templates/plan.md` —— plan 模板
- `openspec/specs/language-style/spec.md` —— 语言风格
- `openspec/specs/evidence-policy/spec.md` —— 证据政策
- `openspec/specs/diagram-policy/spec.md` —— 图表政策
