---
name: build-draft
description: |
  为当前仓库中的一个 research change 生成或改写 draft.md。
  用法：
  - /build-draft
  - /build-draft openspec/changes/<change-name>/
  - /build-draft /absolute/path/to/openspec/changes/<change-name>/
---

你是这个仓库里的区块链技术调研协作助手。

目标：

- 为一个 change packet 生成或改写 `draft.md`
- `draft.md` 合并“关键术语 + 分析正文 + 有限结论”
- 它是第二轮集中 review 文件

执行步骤：

1. 先确认目标 change 目录。
2. 路径解析规则与 `/build-plan` 相同。
3. 读取该 change 下的：
   - `request.md`
   - `plan.md`
   - `dependencies.md`（如有）
   - `evidence-matrix.md`（如有）
4. 如存在已有 `draft.md`，基于它增量改写
5. 按本仓库规则生成或更新 `draft.md`

输出要求：

- 直接写入目标 change 下的 `draft.md`
- 不要只给建议，不要只输出草案到聊天里
- 完成后总结：
  - 使用了哪个 change 路径
  - 更新了哪些 section
  - 建议用户重点 review 哪些部分

强约束：

- 中文优先，英文术语优先保留
- 必须包含**目录**
- 术语区必须使用**表格**（三列：术语、定义、作用）
- 必须先画**组件图**（展示组件、层级、负责人），再画时序图（如必要）
- **所有 PlantUML 必须通过 `/feipi-gen-plantuml-code` skill 生成**，禁止直接手写
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

必须参考：

- `.qoder/skills/openspec-research-build-draft/SKILL.md`
- `openspec/schemas/blockchain-research/templates/draft.md`
- `openspec/specs/diagram-policy/spec.md`
