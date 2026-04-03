# 仓库资产模型

## 目的

定义本仓库中的长期资产类别，以及它们与临时 change artifacts 的区别。

## 要求

- 仓库必须把长期事实分析资产与长期场景决策资产分开。
- 仓库必须使用 `knowledge/` 作为长期正式产出的共同父目录。
- 长期事实分析资产统一放在 `knowledge/analysis/` 下。
- 长期场景决策资产统一放在 `knowledge/decisions/` 下。
- 长期正式正文统一使用 `artifact.md`。
- `request.md`、`plan.md`、`draft.md` 这类过程 artifacts 必须放在 `openspec/changes/<change-name>/` 下。
- 仓库必须在 `openspec/specs/` 下维护可复用的研究系统 specs。

## 资产类型

| 类型 | 位置 | 文件名 | 用途 |
|------|------|--------|------|
| primitive | `knowledge/analysis/primitives/<category>/<name>/` | `artifact.md` | 底层机制分析 |
| synthesis | `knowledge/analysis/synthesis/<category>/<name>/` | `artifact.md` | 演进/综合分析 |
| domain | `knowledge/analysis/domains/<category>/<name>/` | `artifact.md` | 主题域定义 |
| decision | `knowledge/decisions/<category>/<name>/` | `artifact.md` + `verdict.md` | 场景决策 |

## 备注

- 这个 spec 约束的是仓库布局，而不是某一个具体 case 的正文内容。
- `artifact.md` 是唯一长期正式文件名，`reference.md` 是别名（已弃用）。
