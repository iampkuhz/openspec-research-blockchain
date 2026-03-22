# 仓库资产模型

## 目的

定义本仓库中的长期资产类别，以及它们与临时 change artifacts 的区别。

## 要求

- 仓库必须把长期事实分析资产与长期场景决策资产分开。
- 仓库必须使用 `knowledge/` 作为长期正式产出的共同父目录。
- 长期事实分析资产统一放在 `knowledge/analysis/` 下。
- 长期场景决策资产统一放在 `knowledge/decisions/` 下。
- 长期正式正文默认使用 `reference.md`，而不是过程中的 `analysis.md`。
- `request.md`、`brief.md` 这类过程 artifacts 必须放在 `openspec/changes/<change-name>/` 下。
- `sources.md`、`evidence-matrix.md` 这类过程性证据组织文件默认保留在 `openspec/changes/<change-name>/` 下。
- 仓库必须在 `openspec/specs/` 下维护可复用的研究系统 specs。

## 备注

- 这个 spec 约束的是仓库布局，而不是某一个具体 case 的正文内容。
