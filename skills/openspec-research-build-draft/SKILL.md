---
name: build-draft
description: 用于在 plan.md review 通过后，生成和修订 draft.md；适合把 glossary、analysis、verdict 合并为一次集中 review。
---

# 生成研究草稿

## 何时使用

- `plan.md` 已经通过 review
- 来源规划已经足以支撑第一轮正文
- 需要把术语、分析、有限结论合并为一次 review

## 输出要求

- `draft.md`

## 强约束

### 内容结构约束

- 术语区必须用列表，不使用按词分标题的卡片式写法
- `draft.md` 先写机制，再写价值
- 必须回答为什么这样设计，而不是那样设计
- 必须写边界、失败条件、前提条件
- 必须区分 protocol-native、official ecosystem、third-party
- 必须区分 live、planned、promotional
- 结论只能写 bounded conclusions，不得写绝对化判断

### 流程图步骤说明约束

- **必须使用无序列表**，禁止使用有序列表（避免与图中序号错位）
- 必须使用 `【S1→S3】` 格式与图中序号关联（如：`【S1→S3】Bundler 模拟验证机制...`）
- **不要重复完整流程文字**，而是针对重点流程补充说明核心机制或设计原因
- 每个要点聚焦一个关键机制，而非罗列步骤

### 角色归属分类约束

- **必须先写分类定义**，解释 protocol-native / official ecosystem / third-party 三个术语的含义
- 角色归属表**必须包含"作用说明"列**，说明每个角色的具体功能
- 对于纯合约+链外解决方案（如 EIP-4337），需说明 official ecosystem 指核心团队提供的参考实现和协议规范（非链上强制执行但属于官方标准）

### PlantUML 约束

- **PlantUML 必须通过 `/feipi-gen-plantuml-code` skill 生成，禁止直接手写**（详见 `openspec/specs/diagram-policy/spec.md`）
- 所有 PlantUML 代码必须通过 `syntax_result=ok` 校验后才可写入 draft
