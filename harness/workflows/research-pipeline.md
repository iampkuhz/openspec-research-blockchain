# Research Pipeline - 端到端研究流程

## 目标

端到端完成一个 research change 的完整生命周期：
- `request.md` → `plan.md` → `draft.md` → `artifact.md`

## 适用范围

本流程适用于本仓库所有 blockchain research change 的端到端执行。

## 输入输出

**输入**：
- 目标 change 目录路径（或从当前工作目录推断）
- 用户的研究意图（如尚未明确，则在 request 阶段补问）

**输出**：
- `openspec/changes/<change-name>/request.md`
- `openspec/changes/<change-name>/plan.md`
- `openspec/changes/<change-name>/draft.md`
- `knowledge/analysis/.../artifact.md` 或 `knowledge/decisions/.../artifact.md`

## 执行模式

**默认模式：全自动连续执行**

- 连续执行 4 个阶段，不等待用户逐阶段确认
- 如某阶段文件已存在且内容完整，自动跳过该阶段
- 如某阶段文件存在但不完整，自动增量修订

**可选模式：分阶段 review**

- 用户可要求在每阶段完成后暂停 review
- 需在触发命令中显式指定

## 阶段顺序

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌──────────┐
│ request │ -> │  plan   │ -> │  draft  │ -> │ artifact │
└─────────┘    └─────────┘    └─────────┘    └──────────┘
```

## 阶段定义

### 阶段 1：request

**目标**：定义研究意图与问题边界

**输入文件**：
- 无（或用户提供的初步想法）

**输出文件**：
- `request.md`

**规则来源**：
- `openspec/schemas/blockchain-research/templates/request.md`
- `openspec/specs/request-generation/spec.md`

**跳过条件**：
- `request.md` 已存在且包含：对象类型、研究路径、核心问题、触发原因、范围边界、已知输入、预期输出

**增量更新规则**：
- 如缺少上述任一必需字段，补全缺失部分

---

### 阶段 2：plan

**目标**：将研究问题转化为可执行计划

**输入文件**：
- `request.md`

**输出文件**：
- `plan.md`

**规则来源**：
- `openspec/schemas/blockchain-research/templates/plan.md`
- `openspec/specs/plan-generation/spec.md`

**跳过条件**：
- `plan.md` 已存在且包含：研究对象、问题拆解、待确认问题、交付范围、研究深度、来源规划、证据缺口、完成标准

**增量更新规则**：
- 如缺少上述任一必需字段，补全缺失部分

---

### 阶段 3：draft

**目标**：合并术语、分析正文、有限结论为单一交付物

**输入文件**：
- `request.md`
- `plan.md`

**输出文件**：
- `draft.md`

**规则来源**：
- `openspec/schemas/blockchain-research/templates/draft.md`
- `openspec/specs/draft-generation/spec.md`
- `openspec/specs/diagram-policy/spec.md`

**跳过条件**：
- `draft.md` 已存在且包含：概述、术语表、组件架构、核心流程（如必要）、设计取舍、能力边界、相关协议对比、结论、待确认问题、参考资料

**增量更新规则**：
- 如缺少上述任一必需章节，补全缺失部分
- 如图表未通过语法校验，重新生成

---

### 阶段 4：artifact

**目标**：将稳定的 draft 提炼为长期资产

**输入文件**：
- `request.md`
- `plan.md`
- `draft.md`

**输出文件**：
- `knowledge/analysis/.../artifact.md`（primitive / synthesis / domain 类型）
- `knowledge/decisions/.../artifact.md` + `verdict.md`（decision 类型，当已形成稳定判断时）

**规则来源**：
- `openspec/specs/canonical-output-model/spec.md`
- `openspec/specs/artifact-generation/spec.md`

**跳过条件**：
- 不适用（artifact 阶段必须执行，除非用户显式跳过）

**增量更新规则**：
- 如长期资产已存在，基于最新 draft 增量更新

---

## 全流程完成标准

pipeline 视为完成，当且仅当：

1. **四阶段均已执行或跳过**
   - 每个阶段的状态已记录（已执行/已跳过）

2. **输出文件完整**
   - `request.md`、`plan.md`、`draft.md` 已写入 change 目录
   - `artifact.md`（+ `verdict.md` 如适用）已写入长期知识目录

3. **内容合规**
   - 各阶段文件满足对应 OpenSpec spec 的完成标准

## 全流程总结要求

完成后应输出：

- 执行模式（全自动/分阶段 review）
- 各阶段状态（执行/跳过）
- 使用的 change 路径
- 研究对象类型和路径
- 提炼的长期资产路径
- 建议用户下一步操作（如 review artifact）

## 相关规范

- `openspec/specs/request-generation/spec.md` —— request 阶段规范
- `openspec/specs/plan-generation/spec.md` —— plan 阶段规范
- `openspec/specs/draft-generation/spec.md` —— draft 阶段规范
- `openspec/specs/artifact-generation/spec.md` —— artifact 阶段规范
- `openspec/specs/canonical-output-model/spec.md` —— 长期资产结构
