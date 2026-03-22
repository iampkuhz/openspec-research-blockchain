# Prompt：新建 Primitive 深挖

你现在要为一个新的 `primitive` 研究对象创建 `deep-dive` 初始版本。

## 输入

- primitive 名称
- 所属 domain
- 研究问题
- 已知的核心规范或官方资料

## 任务

请输出以下文件的初始内容：

- `request.md`
- `brief.md`
- `sources.md`
- `analysis.md`
- `glossary.md`
- `verdict.md`
- 如有必要，补 `evidence-matrix.md`

## 强约束

- 先机制，后价值
- 先事实，后判断
- 明确设计原因，而不是只描述功能
- 说明它为什么这样做，而不是那样做
- 区分协议原生能力、官方生态能力、第三方能力
- 区分已上线能力、规划中能力、宣传性表述
- 明确标出 `evidence gap` 与 `unresolved ambiguity`

## 输出要求

- `brief.md` 中 research budget 默认写为 `deep`
- `analysis.md` 至少包括：问题、机制、设计原因、边界、影响
- `glossary.md` 至少给出 5 张术语卡
- `verdict.md` 不得使用绝对化结论
