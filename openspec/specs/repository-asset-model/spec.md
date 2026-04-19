# 仓库资产模型

## 目的

定义本仓库中的长期资产类别，以及它们与过程型 change artifacts 的区别。

## 要求

- 仓库必须把长期事实分析资产与长期场景决策资产分开。
- 仓库必须使用 `knowledge/` 作为长期正式产出的共同父目录。
- 长期事实分析资产统一放在 `knowledge/analysis/` 下。
- 长期场景决策资产统一放在 `knowledge/decisions/` 下。
- 长期正式正文统一使用 `artifact.md`。
- `request.md`、`plan.md`、`draft.md`、`decision-criteria.md` 这类过程 artifacts 必须放在 `openspec/changes/<change-name>/` 下。
- 仓库必须在 `openspec/specs/` 下维护可复用的研究系统 specs。

## 资产类型

| 类型 | 位置 | 文件名 | 用途 |
|------|------|--------|------|
| primitive | `knowledge/analysis/primitives/<domain_id>/<topic_slug>/` | `artifact.md` | 底层机制分析 |
| synthesis | `knowledge/analysis/synthesis/<topic_slug>/` | `artifact.md` | 演进/综合分析 |
| decision | `knowledge/decisions/<domain_id>/<topic_slug>/` | `artifact.md` + `verdict.md` | 场景决策 |

## 分组概念

- `domain` 是目录分组概念，不是独立资产类型。
- `domain_id` 只用于组织 `primitive` 与 `decision` 的长期目录。

## 备注

- 这个 spec 约束的是仓库布局，而不是某一个具体 case 的正文内容。
- `artifact.md` 是唯一长期正式正文文件名；`reference.md` 和 `criteria.md` 都不是当前 canonical 长期文件名。

## Change 归档

- `openspec/changes/<change-id>/` 中的研究过程文件在 publish/apply 完成后，必须移动到 `openspec/archive/<change-id>/`。
- 归档由主会话 orchestrator 在 publish gate 完成后执行。
- 未归档的 change 目录视为"进行中"状态；已归档的视为"已完成"状态。
- 归档时保持目录结构不变，仅移动整个 change 目录到 `archive/` 子目录。
- `sources/`、`diagrams/`、`review/` 等审计线索文件随 change 一起归档，不得丢弃。
