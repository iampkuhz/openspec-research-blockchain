# 机制型 Primitive 写作规则

> 本文件来自已合并的 `write-primitive-mechanism` skill，降级为 `write-primitive-draft` 的参考子章节。

## 执行步骤

1. **先做实体分类**
   - 把关键实体分成 `role / component / data object / state / external system`
   - 标明控制方、是否跨信任边界、应落入哪类图

2. **再做图表清单**
   - 明确每张图要回答的问题
   - 判断哪些图是必需、哪些可以省略
   - 若省略，必须写明原因

3. **按机制语义决定必要视图**
   - 有多角色或 trust assumption → 必须有角色与信任边界图
   - 需要解释单角色内部实现 → 必须有角色内部组件图
   - 依赖跨角色交互 → 必须有跨角色核心流程图
   - 依赖命名状态 / round / epoch / timeout / challenge → 必须有状态图或状态表

4. **生成图表**
   - Architecture / Sequence 类型遵守仓库 diagram policy
   - State 类型使用 Mermaid / Markdown 表格 / ASCII fallback
   - 同构角色优先复用 canonical 内部组件图，补差异表

5. **撰写正文**
   - 图承担主干结构
   - 文字只补充设计原因、trade-off、边界情况和失败条件

6. **回写 claims 并自检**
   - 检查必要视图是否覆盖
   - 检查是否混用了角色、组件、状态

## 质量保证

- 有实体分类表
- 有图表清单表
- 设计动机清晰
- 关键设计有对比
- 边界情况覆盖
- 复杂度分析（如适用）
- 多角色机制有角色与信任边界图
- 需要内部结构时有角色内部组件图
- 跨角色机制有核心流程图
- 显式状态机制有状态图或状态表
- diagram 准确且未混用抽象层

## 失败模式处理

- 机制细节在来源中不明确：标注 evidence gap，记录不确定性
- 流程图过于复杂：分解为 happy path / failure path，多图表达
- 抽象层混用：重新做实体分类，再拆成角色图、组件图、状态图
- 同构角色被重复作图：保留 1 张 canonical 内部组件图，补差异表，删除重复图

## 禁止事项

- 不要只描述"是什么"而不解释"为什么"
- 不要混入演进历史
- 不要忽略边界情况
- 不要混用不同抽象层
- 不要跳过实体分类表和图表清单表
- 不要把角色、组件、状态混在一张图里

## 历史路径

本文件来自 `skills/research-authoring/write-primitive-mechanism/SKILL.md`，其中引用的 `atoms/` 路径和 `atom-mechanism-rules.md` 等旧语义已不再作为主流程使用。当前主流程使用 `draft.md` 作为 primitive 产出。
