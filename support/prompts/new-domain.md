# Prompt：新建 Domain

你现在要为一个新的 `domain` 研究目录创建初始内容。

## 输入

- domain 名称
- 这个 domain 为什么值得长期维护
- 当前已知的关键子问题
- 当前已知的相关 primitive / synthesis / decision 对象

## 任务

请输出一个可直接落到仓库中的 domain 初始版本，至少覆盖：

- `request.md`
- `plan.md`
- `draft.md`
- 如有必要，补 `dependencies.md`

## 强约束

- 中文为主，英文术语优先保留
- 这是长期主题地图，不是假装已经研究完成的总结
- 明确说明哪些内容是占位、哪些是示范写法
- 不要写成营销文案
- 明确给出范围、非范围、研究优先级
- glossary 层不是附录，必须进入 `draft.md` 的术语区

## 输出要求

- 逐文件输出
- 每个文件都用 Markdown
- `plan.md` 中明确该 domain 不是主要研究路径，而是长期维护入口
- `draft.md` 重点写主题结构、问题簇、研究边界，不要伪装成完成结论
