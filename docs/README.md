# docs/ — 仓库治理与元文档

本目录存放仓库自身的治理文档与元数据说明，与知识资产和研究产出区分开。

**与其他目录的关系**：

| 目录 | 定位 | 示例 |
|------|------|------|
| `docs/`（本目录） | 仓库自身的治理规则、边界定义、元文档 | governance、架构决策记录 |
| `knowledge/` | 编译后的知识资产（研究结论） | `analysis/`、`decisions/` |
| `openspec/specs/` | 研究工作的正式规则（OpenSpec） | evidence-policy、analysis-principles |
| `openspec/changes/` | 研究过程产出（临时） | request、plan、draft |
| `sources/` | 原始不可变的研究资料 | 论文、官方文档 |
| `harness/` | 执行手册与校验规则 | workflows、rules、hooks |

**不是这里的职责**：
- 不在这里存放研究结论（那是 `knowledge/` 的职责）
- 不在这里存放研究规则（那是 `openspec/specs/` 的职责）
- 不在这里存放研究过程产出（那是 `openspec/changes/` 的职责）

---

## 目录结构

```
docs/
├── governance/              # 治理文档
│   ├── README.md            # 治理索引
│   ├── openspec-harness-boundary.md  # OpenSpec 与 Harness 边界定义
│   └── ...
└── 更改清单.md              # 历史变更记录（遗留格式）
```

## 治理文档索引

参见 [`docs/governance/README.md`](./governance/README.md)
