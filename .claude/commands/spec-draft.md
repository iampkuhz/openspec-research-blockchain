# spec-draft

为当前仓库中的一个 research change 生成或改写 draft.md。

**用法：**
- `/spec-draft`
- `/spec-draft openspec/changes/<change-name>/`
- `/spec-draft /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 目标

- 为一个 change packet 生成或改写 `draft.md`
- `draft.md` 合并"关键术语 + 分析正文 + 有限结论"
- 它是第二轮集中 review 文件

## 执行步骤

1. 先确认目标 change 目录。
2. 路径解析规则与 `/spec-plan` 相同。
3. 读取该 change 下的：
   - `request.md`
   - `plan.md`
   - `dependencies.md`（如有）
   - `evidence-matrix.md`（如有）
4. 如存在已有 `draft.md`，基于它增量改写
5. 按本仓库规则生成或更新 `draft.md`

## 输出要求

- 直接写入目标 change 下的 `draft.md`
- 不要只给建议，不要只输出草案到聊天里
- 完成后总结：
  - 使用了哪个 change 路径
  - 更新了哪些 section
  - 建议用户重点 review 哪些部分

## 强约束

### 图表策略（优先级排序）

**图表优先级（从高到低）**：

1. **PlantUML**（复杂图首选）
   - 适用：组件架构图、核心流程时序图、复杂关系网络
   - 必须通过 `/feipi-gen-plantuml-code` skill 生成
   - 必须通过 `syntax_result=ok` 校验

2. **Mermaid**（简单图备选）
   - 适用：简单流程图、时序图、时间线
   - GitHub 原生支持，语法简洁

3. **Markdown 表格**（结构化信息首选）
   - 适用：特性对比、能力归属、时间线、状态对比
   - 零依赖、占用空间最小

4. **URL 图**（外部引用）
   - 适用：已有官方图表、复杂架构图
   - 直接引用官方来源链接

5. **本地图片文件**（最差选项）
   - 仅在以上方案都无法满足时使用
   - 需说明原因

### 架构图设计原则

**禁止死板分层**：

- 不得按"应用层、协议层、实现层"等抽象分层组织架构图
- 必须按**真实场景**归纳组件和模块

**必须遵循的原则**：

1. **场景驱动**：按实际使用场景组织组件（如"用户交易提交场景"、"Bundler 打包场景"）
2. **角色清晰**：每个组件标注"谁提供的服务"、"哪里实现"
3. **结合实例**：组件说明必须结合现有著名项目、工具（如：Bundler → Stackup、Pimlico）
4. **容易理解**：组件命名和分组要让人一眼看懂，避免过度抽象

**示例结构**：

```
用户钱包场景：
├── 用户交互入口（MetaMask、Rabby）
├── 签名验证（1271 合约钱包、智能合约）
└── 交易广播（Public RPC、Bundler 私有 RPC）

Bundler 处理场景：
├── Bundler 服务（Stackup、Pimlico、Infra）
├── Builder/中继器
└── EntryPoint 合约（链上）
```

### 内容结构约束

- 中文优先，英文术语优先保留
- 必须包含**目录**
- 术语区必须使用**表格**（三列：术语、定义、作用）
- 必须先画**组件图**（展示组件、层级、负责人），再画时序图（如必要）
- 所有 PlantUML 必须通过 `/feipi-gen-plantuml-code` skill 生成，禁止直接手写
- 所有 PlantUML 必须通过 `syntax_result=ok` 校验后才可写入 draft
- 顺序固定为：
  - 概述
  - 术语表（表格）
  - 组件架构（必须包含组件图）
  - 核心流程（时序图，如必要）
  - 设计取舍
  - 能力边界
  - 相关协议对比
  - 结论
  - 待确认问题
  - 参考资料（必须包含链接和说明）
- 必须区分 live、planned、promotional
- 若证据不足，明确写不确定性，不要脑补

### 图表保留原则

**draft.md 必须保留所有核心图表**：

- 演进时间线图（synthesis）
- 组件架构图（primitive）
- 核心流程图（primitive）
- 能力归属表
- 对比表格
- 关系网络图（synthesis）

**图表信息密度要求**：

- 每张图必须有独立的信息价值
- 不得用文字重复图表已清晰表达的内容
- 文字只补充图中不易展示的：设计原因、trade-off、边界情况

## 必须参考

- `openspec/schemas/blockchain-research/templates/draft.md`
- `openspec/specs/diagram-policy/spec.md`
