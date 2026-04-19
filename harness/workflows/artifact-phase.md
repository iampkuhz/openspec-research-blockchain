# Artifact 阶段规范

## 目的

定义本仓库 blockchain research change 中从 `draft.md` 生成 `artifact.md` / `verdict.md` 的正式规则，包括：
- artifact 在 research change 中的定位
- 进入 artifact 阶段的前置条件
- durable 内容提炼规则
- 过程性内容移除要求
- artifact 阶段完成标准

## 适用范围

本规范适用于本仓库所有 research change 的 artifact 阶段。

## artifact.md 的定位

`artifact.md` 是 research change 的长期资产 artifact，负责：
- 将稳定的 `draft.md` 内容提炼为可长期复用的知识
- 移除过程性痕迹，保留 durable 内容
- 作为主流程 `request -> plan -> draft -> artifact` 的最终交付物

**`artifact.md` 是长期资产，不是过程文件**。

## 进入 artifact 阶段的前置条件

必须满足以下条件方可进入 artifact 阶段：

1. **draft.md 已稳定**
   - `draft.md` 已通过 review 且内容稳定

2. **研究目标已达成**
   - `plan.md` 中定义的完成标准已满足

## apply 前校验 gate

在将内容写入 `knowledge/` 前，必须执行三层校验：

| 校验脚本 | 职责 | 失败处理 |
|----------|------|----------|
| `scripts/general/check_frontmatter.py` | 校验 frontmatter 字段、枚举值、deprecated field 拒绝 | 阻止 apply |
| `scripts/general/validate_knowledge_tree.py` | 校验目录结构、registry 一致性 | 阻止 apply |
| `scripts/research/check_artifact_contract.py` | 校验最小章节集合 | 阻止 apply |

执行顺序：先跑 `check_frontmatter.py`，再跑 `validate_knowledge_tree.py`，最后跑 `check_artifact_contract.py`。任一脚本返回 error 级别问题，不得写入 `knowledge/`。

## artifact 阶段的正式要求

### 长期资产结构要求

artifact 阶段的基础结构服从 `openspec/specs/canonical-output-model/spec.md`。

本规范仅补充 artifact 阶段特有的提炼与移除要求。

### 输出路径要求

| 对象类型 | 长期路径 |
|----------|----------|
| primitive / synthesis / domain | `knowledge/analysis/.../artifact.md` |
| decision | `knowledge/decisions/.../artifact.md` |

**decision 类型的 verdict.md**：
- 当已形成稳定判断时，必须额外输出 `verdict.md`
- `verdict.md` 与 `artifact.md` 并列，前者聚焦判断结论，后者保留完整分析

### durable 内容提炼要求

**必须保留的核心内容类型**：

- 关键术语（表格：术语、定义、作用）
  - **跨引用链接要求**：如果关键术语对应本仓库中已存在的 artifact（如 SIWE、DID Auth、EIP-4337 等），必须在术语名称上添加相对路径的 Markdown 链接，方便跳转查看
  - 示例：`[SIWE](../../account-abstraction/eip-4361-siwe/artifact.md)`
- **本质定义**（primitive/synthesis 必须保留"本质与表现形式"章节，包括结构化表格）
- 分析正文（组件架构、核心流程、演进关系、问题簇划分等）
- 设计取舍（为什么这样设计，而不是那样设计）
- 能力边界（能解决什么、不能解决什么、失败条件）
- 相关协议关系（与相邻协议/对象的关系定位）
- 可确认结论（基于证据的有限结论）
- Evidence Gap（已知的证据缺口）
- 参考资料（简化格式）

### 图表保留要求

**核心图表不得在提炼时丢失**：

- 对长期理解仍有独立信息价值的图表必须保留
- 图表优先原则在长期资产中仍成立（能可视化的内容应优先保留图表形式）

### 参考资料格式要求

**长期资产中必须简化格式**：

- 使用两列表达：`来源 | 说明`
- 不保留 L1/L2/L3/L4 证据等级
- 不单独设置"类型"列
- 链接直接嵌入来源名称

### 必须移除的内容

以下内容不得进入 `artifact.md`：

- 过程性注释和标记（如 `<!-- -->` 注释块）
- 中间处理术语（如【基于 L1/L2 证据】）
- 证据等级标注（L1/L2/L3/L4）
- `request.md`、`plan.md`、`draft.md` 的原样复制

### 风格要求

- 中文优先，英文术语优先保留
- 结论直接陈述，不使用过程性前缀
- 如有不确定性，使用用户可理解的表述（如【当前可确认】、【尚需验证】）

## artifact 阶段完成标准

artifact 阶段视为完成，当且仅当：

1. **durable 内容已提炼**
   - 核心内容类型已完整保留
   - 分析正文已提炼为长期可复用的形式

2. **过程性内容已移除**
   - 无过程性注释和标记
   - 无证据等级标注
   - 无中间处理术语

3. **格式合规**
   - 参考资料使用简化格式
   - 输出路径符合 `canonical-output-model` 要求

4. **decision 类型额外要求**
   - 如已形成稳定判断，`verdict.md` 已输出

## 与上位规范的关系

本规范是以下规范的 artifact 阶段特化：

| 上位规范 | 约束范围 |
|----------|----------|
| `openspec/schemas/blockchain-research/schema.yaml` | change 整体结构 |
| `openspec/specs/canonical-output-model/spec.md` | 长期资产结构本体 |
| `harness/rules/diagrams/diagram-policy.md` | 图表政策（artifact 阶段的图表保留） |
| `harness/rules/writing/language-rules.md` | 语言风格 |

本规范不重复上位规范的正文，仅定义：
- artifact 阶段的入口条件
- durable 内容提炼规则
- 过程性内容移除要求
- artifact 阶段的完成标准

## 相关规范

- `openspec/specs/canonical-output-model/spec.md` —— 长期产出模型（结构本体）
- `harness/rules/diagrams/diagram-policy.md` —— 图表政策
- `harness/rules/writing/language-rules.md` —— 语言风格
