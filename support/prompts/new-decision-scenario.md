# Prompt：新建 Decision 场景

你现在要为一个新的 `decision` 研究对象创建 `scenario` 初始版本。

## 输入

- decision 名称
- 场景描述
- 候选方案列表
- 已知依赖的 domain / primitive / synthesis 对象

## 任务

请输出以下文件的初始内容：

- `request.md`
- `brief.md`
- `sources.md`
- `analysis.md`
- `glossary.md`
- `verdict.md`
- `dependencies.md`
- `decision-criteria.md`
- `evidence-matrix.md`

## 强约束

- 这是具体场景的比较，不是泛泛评测
- 先定义比较标准，再写比较
- 依赖下层研究时必须声明 budget 与复用边界
- 不允许把生态宣传、roadmap 或第三方封装直接写成协议原生能力
- 不允许输出没有前提条件的绝对排名

## 输出要求

- `decision-criteria.md` 必须区分 hard constraints、soft preferences、open questions
- `analysis.md` 必须把已确认项、部分确认项、待验证项分开
- `verdict.md` 必须写清场景前提、最优条件、放弃条件和补证方向
