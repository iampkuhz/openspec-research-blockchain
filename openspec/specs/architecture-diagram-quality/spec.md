# 架构组件图质量规约

## 目的

定义区块链技术分析中架构组件图的质量标准。

**注意**：本规约是领域特定要求，通用 PlantUML 规范参见用户级 skills (`feipi-plantuml-generate-architecture-diagram` 和 `feipi-plantuml-generate-sequence-diagram`)。

## 两段式架构

架构组件图生成采用两段式架构：

| 阶段 | 负责方 | 交付物 |
|------|--------|--------|
| 阶段 1 | 发起方 | brief 需求模板（YAML 格式） |
| 阶段 2 | 画图方 | `<diagram-id>.puml` + `.svg` |

发起方填写需求模板，画图方（用户级 skill）根据模板生成并校验。

两段式架构详细说明见 skill 文档：`feipi-plantuml-generate-architecture-diagram/SKILL.md`

## 领域特定要求

### 1. 分层规范（区块链特定）

架构组件图必须区分以下层次：

| 层次 | 说明 | 示例组件 |
|------|------|----------|
| Protocol Layer | 协议核心层 | 共识引擎、验证器集、最终性模块 |
| Data Layer | 数据对象层 | Proposal、Vote、Certificate |
| Application Layer | 应用接口层 | RPC Endpoint、API Gateway |
| External Layer | 外部参与方 | 验证者、用户、管理员 |

### 2. 组件内聚要求

每个组件应满足：
- **单一职责**：一个组件只做一件事
- **明确边界**：输入输出清晰
- **可解释性**：组件名称能说明其作用

### 3. 视觉层次（推荐）

- **核心组件**：放在图中央，使用更醒目的颜色
- **辅助组件**：放在边缘，使用较淡的颜色
- **外部依赖**：放在边界外，使用灰色

## 与 Diagram Policy 的关系

本规约是 `openspec/specs/diagram-policy/spec.md` 在架构组件图领域的具体化。

## 相关文件

- `openspec/specs/diagram-policy/spec.md`：图表总政策
- `feipi-plantuml-generate-architecture-diagram/SKILL.md`：PlantUML 生成 skill（包含两段式架构说明、元素规范和样式库）
- `feipi-plantuml-generate-architecture-diagram/assets/templates/architecture-brief.yaml`：架构组件图需求模板
- `feipi-plantuml-generate-architecture-diagram/references/template-architecture-brief.md`：需求模板详细说明
