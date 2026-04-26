---
name: write-primitive-draft
description: 编写 primitive 类型的 draft.md 正文，聚合 definition/evolution/mechanism 子章节写作规则。
---

# 编写 Primitive 型草稿

## 适用场景

- 研究内容为 `primitive`，需要定义某个概念/机制/组件。
- 适用 `primitive` profile。
- 研究以文献/规范阅读为主，需要按来源组织分析（`source_reading` 路径）。

## 输入

- `sources/claims/*.md` 提取的 claims。
- `sources/evidence-map.md`。
- `request.md` / `plan.md`。
- 如有，`sources/notes/*.md` 来源笔记。

## 输出

- `draft.md`（写入当前 change 目录下）。

## 读取文件

- `request.md`、`plan.md`。
- `sources/claims/*.md`、`sources/evidence-map.md`。
- `openspec/schemas/blockchain-research/templates/draft.md`。

## 写入文件

- `openspec/changes/<change-id>/draft.md`

## 子章节写作规则（references/）

本 skill 聚合了三种 primitive 写作子语义，详细规则见：

- `references/definition/` —— 定义型 primitive：形式化定义、关键术语、边界条件
- `references/evolution/` —— 演进型 primitive：演进阶段、驱动因素、不变原则、分歧点
- `references/mechanism/` —— 机制型 primitive：实体分类、图表清单、设计动机、核心流程、状态转换、边界情况

## 执行步骤

1. **生成分析内容**
   - 对 mechanism-heavy 内容，先做实体分类（role / component / data / state / external）
   - 再做图表清单，明确哪些图是必需、回答什么问题、为什么可省略
   - 先写术语表（表格形式）
   - 再写分析正文

2. **按 primitive 子视图决定必要视图**
   - 有多角色或 trust assumption → 角色与信任边界总览图
   - 对每个 materially 不同的核心角色族 → 角色内部组件图
   - 有跨角色交互 → 跨角色核心流程图
   - 有显式状态 / round / epoch / timeout / challenge → 状态图或状态表
   - 始终补能力归属表；若复用 canonical 内部组件图，补角色差异表

3. **生成图表**
   - Architecture / Sequence 类型调用对应全局 skill（`feipi-plantuml-generate-architecture-diagram` / `feipi-plantuml-generate-sequence-diagram`）
   - 遵守 diagram contract（brief → puml → validation）
   - 同构角色优先复用 canonical 内部组件图，补差异表

4. **撰写正文**
   - 图承担主干结构
   - 文字补充设计原因、trade-off、边界情况和失败条件

5. **回写 claims 并自检**
   - 检查必要视图是否覆盖
   - 检查每个 claim 是否可追溯到来源

## 禁止事项

- 不得生成 `work-products/*.md`。
- 不得跳过 claims 直接写结论。
- 不得直接写 `knowledge/**`。
- 不得跳过实体分类表和图表清单表。
- 不得把角色、组件、状态混在一张图里。

## 自检

- draft 是否包含角色的定义、边界与信任假设？
- 每个 claim 是否可追溯到来源？
- 必要视图是否按条件补齐？
- 术语是否与既有 glossary 一致？
