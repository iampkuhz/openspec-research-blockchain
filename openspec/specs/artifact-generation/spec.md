# Artifact 阶段规范

## 目的

定义本仓库 blockchain research change 中从 `draft.md` 生成 `artifact.md` / `verdict.md` 的正式规则，包括：
- artifact 在 research change 中的定位
- 进入 artifact 阶段的前置条件
- artifact 必须满足的形式要求
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

## artifact 阶段的正式要求

### 长期资产结构要求

artifact 阶段的输出路径服从 `openspec/specs/canonical-output-model/spec.md`：

- `primitive` / `synthesis` / `domain` 类型：输出至 `knowledge/analysis/.../artifact.md`
- `decision` 类型：输出至 `knowledge/decisions/.../artifact.md` + `verdict.md`（可选）

### artifact.md 结构要求

**必须保留的核心章节**（按顺序）：

1. 目录（导航目录）
2. 关键术语（表格：术语、定义、作用）
3. 组件架构（含组件分层和角色归属说明）
4. 核心流程（含流程说明和关键步骤）
5. 设计取舍
6. 能力边界
7. 相关协议关系
8. 可确认结论
9. Evidence Gap
10. 参考资料（简化格式）

### 图表保留要求

**必须优先保留图表**：

- **架构图（必须）**：组件架构图、演进框架图、问题层分布图
- **核心流程图（必须）**：关键交互时序图、核心业务流转流程
- **对比表格（必须）**：能力归属表、特性对比表、链适配对比表
- **关系网络图（synthesis 必须）**：EIP 演进关系图、协议依赖关系图

**原则**：每张图/表必须有独立的信息价值。

### 参考资料格式要求

**必须使用简化表格格式**（2 列）：

| 来源 | 说明 |
|------|------|
| [EIP-4337](url) | 账户抽象主规范 |

**格式要求**：
- 链接直接嵌入来源名称
- 只保留"来源"和"说明"两列
- 不设置"类型"列
- 不标注证据等级（L1/L2/L3/L4）

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

1. **结构完整**
   - 包含所有必须章节
   - 章节顺序符合要求

2. **图表完备**
   - 所有核心图表已保留
   - 图表具有独立信息价值

3. **内容合规**
   - 已移除所有过程性内容
   - 参考资料使用简化格式
   - 无证据等级标注

4. **输出路径正确**
   - 对象类型与目标长期路径匹配
   - 符合 `canonical-output-model` 要求

## 与上位规范的关系

本规范是以下规范的 artifact 阶段特化：

| 上位规范 | 约束范围 |
|----------|----------|
| `openspec/schemas/blockchain-research/schema.yaml` | change 整体结构 |
| `openspec/specs/canonical-output-model/spec.md` | 长期资产结构 |
| `openspec/specs/diagram-policy/spec.md` | 图表政策（artifact 阶段的图表保留） |
| `openspec/specs/language-style/spec.md` | 语言风格 |

本规范不重复上位规范的正文，仅定义：
- artifact 阶段的入口条件
- artifact 阶段的形式要求
- artifact 阶段的完成标准

## 相关规范

- `openspec/specs/canonical-output-model/spec.md` —— 长期产出模型
- `openspec/specs/diagram-policy/spec.md` —— 图表政策
- `openspec/specs/language-style/spec.md` —— 语言风格
