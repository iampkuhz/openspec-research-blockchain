# Prompt：生成 Draft

请基于已有的 `request.md`、`plan.md` 生成或改写 `draft.md`。

## 任务

输出一份集中 review 草稿，顺序固定为：

1. 关键术语
2. 分析入口
3. 机制拆解
4. 设计原因
5. 边界与前提
6. 与相邻对象的关系
7. 当前可确认结论
8. 当前不能确认的部分
9. 后续补证

## 强约束

- 术语区必须使用列表
- 先机制，后价值
- 先事实，后判断
- 必须回答“为什么这样做，而不是那样做”
- 必须区分 protocol-native、official ecosystem、third-party
- 必须区分 live、planned、promotional
- 若证据不足，明确写出不确定性，不要脑补
