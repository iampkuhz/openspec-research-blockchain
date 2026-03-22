# OpenSpec 改动包

这里存放“当前一轮研究改动包”，对标普通 OpenSpec 仓库中的 `changes/change-name/`。

默认做法：

- 本目录只保留 `README.md` 进版本库
- 具体 `openspec/changes/<change-name>/` 默认作为本地工作区使用，并在 `.gitignore` 中忽略

建议用法：

1. 为一轮具体研究创建 `openspec/changes/<change-name>/`
2. 在该目录中生成或修改本轮需要的过程文件，例如 `request.md`、`brief.md`、`sources.md`、`evidence-matrix.md`
3. 本轮研究稳定后，把成熟内容提炼进 `knowledge/analysis/` 或 `knowledge/decisions/` 中对应的正式案例

不要把这里当作长期正式研究目录。

长期正式研究资产统一维护在 `knowledge/analysis/` 与 `knowledge/decisions/`。
