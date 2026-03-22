# 语言与写作风格

> 角色：说明版。仓库级硬规范见 [openspec/specs/language-style/spec.md](/Users/zhehan/Documents/tools/llm/openspec/openspec-research-blockchain/openspec/specs/language-style/spec.md)。

## 语言原则

- 中文优先
- 英文术语优先保留
- 专业、克制、结构化
- 适合长期维护

## 术语处理

以下内容优先保留英文原文：

- 协议名
- 标准名
- 字段名
- 合约名
- EIP / ERC / RIP 编号
- 专业机制名

正确示例：

- `Account Abstraction`
- `EntryPoint`
- `UserOperation`
- `paymaster`
- `bundler`

不建议为了形式统一，强行把它们全部翻译成中文后再解释。

## 正文风格

推荐：

- 先定义对象
- 再说明作用
- 再拆机制
- 再讨论边界
- 最后给结论

避免：

- 空泛抒情
- 趋势口号
- 没有证据约束的判断

## 结论风格

结论必须：

- 具体
- 有前提
- 有边界
- 有证据来源

结论不应：

- 绝对化
- 夸张化
- 宣传化

## 文件命名

- 使用稳定的 kebab-case
- 目录名尽量直接表达对象或问题
- 避免 `misc`、`notes-final-v2` 这类不稳定命名

## 模板使用原则

模板不是空壳，也不是必须逐字照抄。

正确做法：

- 保留模板的结构性约束
- 按题目删减无关部分
- 保证关键字段不缺失

## 示例与占位

示例 case 可以包含示范写法，但必须明确说明：

- 哪些是模板占位
- 哪些是示范表达
- 哪些尚未验证
