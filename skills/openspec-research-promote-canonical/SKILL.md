---
name: promote-canonical
description: 用于把 change packet 中的 durable 结果提炼进 knowledge/analysis/ 或 knowledge/decisions/，适合一轮研究完成后整理长期资产时使用。
---

# 提炼长期产物

## 何时使用

- change packet 已经完成本轮研究
- 需要把长期值得保留的内容提炼进 canonical 目录

## 输出要求

- `knowledge/analysis/...` 或 `knowledge/decisions/...` 下的长期文件

## 强约束

### 基本约束

- 不把 `request.md`、`plan.md` 直接复制进长期目录
- 只保留 durable 结果
- 不把 `evidence-matrix.md` 直接复制进长期目录
- `knowledge/analysis/` 默认只保留 `artifact.md`，必要时保留 `dependencies.md`
- glossary 层默认折叠进 `artifact.md` 的“关键术语”区
- `knowledge/decisions/` 保留 `artifact.md`、`criteria.md`、`dependencies.md`、`verdict.md`

### artifact.md 结构约束

**必须包含的章节**（按此顺序）：

1. **目录**（自动生成的导航目录）
2. **关键术语**（表格：术语、定义、作用）
3. **组件架构**（必须保留，包含组件分层说明和角色归属）
4. **核心流程**（必须保留，包含流程说明和关键步骤解释）
5. **设计取舍**（为什么这样设计，而不是那样设计）
6. **能力边界**（能解决什么、不能解决什么、失败条件）
7. **相关协议关系**（与相邻协议的关系定位）
8. **可确认结论**（基于证据的有限结论，不写证据等级标注）
9. **Evidence Gap**（已知的证据缺口）
10. **参考资料**（简化格式，见下方）

**禁止带入 artifact.md 的内容**：

- PlantUML 代码块（保留图表的文字描述，移除代码）
- 过程性注释（如 `<!-- 与图中序号对应 -->`）
- 中间处理术语（如【基于 L1/L2 证据】、【待确认问题】等）
- `request.md`、`plan.md`、`draft.md` 的原样复制

### 参考资料格式约束

**artifact.md 中的参考资料必须使用简化格式**：

| 来源 | 说明 |
|------|------|
| [EIP-4337](https://eips.ethereum.org/EIPS/eip-4337) | 主规范文档，Final 状态 |
| [eth-infinitism/account-abstraction](https://github.com/eth-infinitism/account-abstraction) | EntryPoint 参考实现 |

**要求**：
- 不区分 L1-L4 证据等级（这是过程层术语）
- 不单独设置"链接"列（链接直接嵌入来源名称）
- 不设置"类型"列
- 说明文字简洁，描述来源的用途即可

### 结论表述约束

- 不得使用【基于 L1/L2 证据】等过程性前缀
- 不得使用证据等级标注（L1/L2/L3/L4）
- 结论应直接陈述，如有不确定性使用【当前可确认】、【尚需验证】等用户可理解的表述
- 如需说明证据强度，使用【官方规范定义】、【参考实现确认】等描述性语言
