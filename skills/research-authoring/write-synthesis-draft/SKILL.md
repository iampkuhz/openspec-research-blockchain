---
name: research-write-synthesis-draft
description: 当研究类型为 synthesis 且比较对象的 claims 已提取完成，需要横向对比多个对象在固定维度上的差异并生成 draft.md 时使用。
---

# 编写 Synthesis 型草稿

## 适用场景

- 研究内容为 `synthesis`，需要横向对比多个对象在同一维度上的差异。
- 适用 `synthesis` profile。

## 输入

- 比较对象列表与比较维度。
- `sources/claims/*.md` 提取的 claims。
- `sources/evidence-map.md`。
- `request.md` / `plan.md`。
- 各比较对象的 atoms 或已有分析。

## 输出

- `draft.md`（写入当前 change 目录下），包含比较分析正文。

## 读取文件

- `request.md`、`plan.md`。
- `sources/claims/*.md`、`sources/evidence-map.md`。
- `openspec/schemas/blockchain-research/templates/draft.md`。
- 各比较对象的 atoms 或已有分析。

## 写入文件

- `openspec/changes/<change-id>/draft.md`

## 执行要点

1. 比较维度必须固定且相关，不得随意切换
2. 每个主张必须有证据支撑，不得主观判断无证据支持
3. 不得混用不同抽象层的对象
4. 必须包含适用场景分析
5. 必须包含不适用场景分析
6. 标注证据等级

## 失败模式处理

- 对象不可比：说明不可比原因，或重新定义比较范围
- 某对象数据不足：标注证据缺口，降低相关结论置信度
- 维度选择不当：重新选择与比较目的相关的维度

## 禁止事项

- 不得生成 `work-products/*.md`。
- 不得跳过 claims 直接写结论。
- 不得直接写 `knowledge/**`。

## 自检

- 比较目的是否明确？
- 维度是否固定且相关？
- 每个比较主张是否有证据支撑？
- 适用/不适用场景是否清晰？
- 证据等级是否标注？
