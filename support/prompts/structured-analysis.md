# Prompt：结构化分析

请基于已有的 `request.md`、`brief.md`、`sources.md`、`glossary.md` 生成或改写 `analysis.md`。

## 任务

输出一份结构化技术分析，顺序固定为：

1. 分析入口
2. 机制拆解
3. 设计原因
4. 边界与前提
5. 与相邻对象的关系
6. 价值与影响
7. 当前可确认与待确认项

## 强约束

- 先机制，后价值
- 先事实，后判断
- 必须回答“为什么这样做，而不是那样做”
- 必须区分 protocol-native、official ecosystem、third-party
- 必须区分 live、planned、promotional
- 若证据不足，明确写出不确定性，不要脑补
- 如果这是上层研究，只抽取依赖对象中和当前问题直接相关的部分
