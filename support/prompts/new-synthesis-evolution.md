# Prompt：新建 Synthesis 演进

你现在要为一个新的 `synthesis` 研究对象创建 `evolution` 初始版本。

## 输入

- synthesis 名称
- 所属 domain
- 需要纳入的 primitive 列表
- 当前核心问题

## 任务

请输出以下文件的初始内容：

- `request.md`
- `plan.md`
- `draft.md`
- `dependencies.md`
- 如有必要，补 `evidence-matrix.md`

## 强约束

- 这是关系 / 演进 / 分层分析，不是把多个 primitive 摘要拼接起来
- 必须声明每个依赖对象的 research budget：`deep / focused / light`
- 必须解释每个依赖只需要该深度的原因
- 不允许复写下层全文
- 关系判断必须尽量由 `L1/L2` 支撑

## 输出要求

- `dependencies.md` 里必须写清 extraction strategy
- `plan.md` 必须说明纳入哪些对象、为什么纳入、还缺什么证据
- `draft.md` 必须包含：演进主线、分层关系、替代 / 互补关系、边界、有限结论
