# spec-promote

把一个 research change 的稳定 draft.md 提炼为长期 canonical 结果。

**用法：**
- `/spec-promote`
- `/spec-promote openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 目标

- 把一个 change packet 中稳定的 `draft.md` 提炼为长期资产
- 对 `primitive / synthesis / domain`，提炼到 `knowledge/.../artifact.md`
- 对 `decision`，额外提炼长期 `verdict.md`

## 执行步骤

1. 确认目标 change 目录，规则与 `/spec-plan` 相同
2. 读取 `request.md`、`plan.md`、`draft.md`，以及可选的 `dependencies.md`、`decision-criteria.md`
3. 判断对象层级与目标 canonical 路径
4. 只提炼 durable 内容，不复制过程痕迹

## 强约束

### 内容提炼约束

- 不把 `request.md`、`plan.md`、`draft.md` 原样复制进长期目录
- glossary 层默认并入 `artifact.md` 的"关键术语"区
- `decision` 可以长期保留单独 `verdict.md`

### artifact.md 结构要求

**必须保留的核心章节**（按顺序）：

1. **目录**（导航目录）
2. **关键术语**
3. **组件架构**（必须保留，含组件分层和角色归属说明）
4. **核心流程**（必须保留，含流程说明和关键步骤）
5. **设计取舍**
6. **能力边界**
7. **相关协议关系**
8. **可确认结论**
9. **Evidence Gap**
10. **参考资料**（简化格式）

### 图表保留策略（重要）

**必须优先保留图表，尤其是**：

1. **架构图**（必须保留）
   - 组件架构图（primitive）
   - 演进框架图（synthesis）
   - 问题层分布图（domain/synthesis）

2. **核心流程图**（必须保留）
   - 关键交互时序图
   - 核心业务流转流程

3. **对比表格**（必须保留）
   - 能力归属表
   - 特性对比表
   - 链适配对比表

4. **关系网络图**（synthesis 必须保留）
   - EIP 演进关系图
   - 协议依赖关系图

**图表形式优先级（从高到低）**：

1. **PlantUML** → 保留 PlantUML 代码块（complex 图）
2. **Mermaid** → 保留 Mermaid 代码块（simple 图）
3. **Markdown 表格** → 保留表格（结构化信息）
4. **URL 图** → 保留外部链接引用（官方图表）
5. **本地图片** → 仅在必要时保留（控制文件大小）

**文件大小控制**：

- 优先使用代码型图表（PlantUML/Mermaid/表格），不增加文件大小
- URL 图只保留链接，不嵌入图片
- 本地图片仅在无替代方案时使用，需说明原因
- 确保 artifact.md 总体大小不过度膨胀

### 参考资料格式（重要）

**简化表格格式**（2 列）：

| 来源 | 说明 |
|------|------|
| [EIP-4337](https://eips.ethereum.org/EIPS/eip-4337) | 账户抽象主规范 |
| [EIP-4361 SIWE](https://eips.ethereum.org/EIPS/eip-4361) | 以太坊签名授权标准 |
| [Interledger Protocol](https://interledger.org/) | 跨账本支付协议 |

**格式要求**：
- 链接直接嵌入来源名称，使用 `[context](url)` 形式
- 只保留"来源"和"说明"两列
- 不设置"类型"列
- 不标注证据等级（L1/L2/L3/L4）

### 必须移除的内容

- 过程性注释和标记
- 【基于 L1/L2 证据】等中间处理术语
- 证据等级标注（L1/L2/L3/L4）
- `<!-- -->` 注释块

## 必须参考

- [draft.md 模板](../openspec/schemas/blockchain-research/templates/draft.md) - 定义 draft 结构和图表要求
- [图表政策](../openspec/specs/diagram-policy/spec.md) - 定义图表生成和校验标准
