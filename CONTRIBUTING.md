# 协作维护说明

## 目标

本仓库的贡献重点不是“多写内容”，而是“把研究对象、证据、依赖和结论组织得可复用”。

## 新增研究的最小流程

1. 判断研究对象属于 `domain`、`primitive`、`synthesis`、`decision` 哪一层。
2. 判断主要路径属于 `deep-dive`、`evolution`、`scenario` 哪一类。
3. 在 `openspec/changes/<change-name>/` 中完成本轮研究过程。
4. 至少在 change packet 中放入三个核心 artifact：
   - `request.md`
   - `plan.md`
   - `draft.md`
5. 如为上层研究，补充：
   - `dependencies.md`
   - `evidence-matrix.md`
6. 如为场景型对比，额外补充：
   - `decision-criteria.md`
7. 本轮研究稳定后，把 durable 结果提炼进 `knowledge/analysis/` 或 `knowledge/decisions/`，而不是把 `request.md`、`plan.md` 直接留在长期目录里。

## 命名规范

- 目录名使用稳定、可预测的 kebab-case。
- `primitive` 和 `synthesis` 不应默认按某个 `domain` 作为父路径分组。
- `domain` 关联应通过 `plan.md`、`dependencies.md` 或正文链接声明，而不是通过硬编码目录层级声明。
- `synthesis` 和 `decision` 目录名应直接体现研究问题，而不是使用模糊代号。

## 内容规范

- 中文为主，英文术语优先保留。
- 先机制，后价值；先事实，后判断。
- 结论优先基于 `L1/L2` 证据。
- 必须显式写出边界、未决问题和证据缺口。

## 提交前检查

- 对象层级是否正确
- 路径类型是否正确
- `plan.md` 是否写明 research budget 与来源规划
- 上层研究是否写明依赖对象与依赖原因
- `draft.md` 的术语区是否覆盖关键术语
- `draft.md` 是否区分确定结论与条件性判断

## 不要做的事

- 不要把钱包、SDK、infra 服务能力直接写成协议原生能力。
- 不要把 roadmap 当成已上线能力。
- 不要为了完整而复制下层研究全文。
- 不要把 marketing 语言直接写进分析和 verdict。
