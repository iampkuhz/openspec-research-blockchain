# Scripts 工具集

本目录包含仓库自动化脚本工具。

---

## 目录结构

```
scripts/
├── README.md             # 本文件
├── general/              # 通用工具（任何阶段可用）
│   ├── init_research_item.py    # 初始化研究项目
│   ├── build_index.py           # 构建 topic 索引
│   ├── check_frontmatter.py     # 检查 YAML frontmatter
│   └── check_traceability.py    # 检查 claim→source 追溯
├── research/             # 研究辅助（写作阶段使用）
│   ├── normalize_claims.py        # 标准化 claims 格式
│   ├── build_comparison_matrix.py # 构建特性对比矩阵
│   ├── validate_sources.py        # 验证来源有效性
│   ├── find_term_drift.py         # 查找术语定义漂移
│   └── validate_draft_diagram_contract.py # 校验 draft.md 中 PlantUML contract
├── publish/              # 发布工具（apply 阶段使用）
│   ├── move_change_outputs.py     # 移动 change 到 knowledge/
│   └── generate_topic_index.py    # 生成 topic 索引文件
├── diagrams/             # 图表工具（校验用）
│   ├── check_plantuml.sh          # PlantUML 语法校验
│   ├── validate_diagram_model.py  # 验证 diagram model 结构
│   └── check_diagram_references.py # 检查图表引用完整性
├── openspec/             # OpenSpec 工具
│   └── new_change.sh              # 创建 change 包
└── maintenance/          # 维护工具（仓库运维用）
    ├── install_repo_skills.sh     # 安装 repo skills 到本地
    ├── render.sh                  # 渲染 PlantUML → SVG
    └── compare_svg.sh             # 比较两个 SVG 差异
```

---

## 使用方法

### 通用脚本（general/）

| 脚本 | 功能 | 命令示例 |
|------|------|----------|
| `init_research_item.py` | 初始化研究项目结构，创建必要的目录和空文件 | `python scripts/general/init_research_item.py --topic eip-4337 --type primitive` |
| `build_index.py` | 扫描 knowledge/ 目录并生成 topic 索引文件 | `python scripts/general/build_index.py --output knowledge/indexes/topic-index.md` |
| `check_frontmatter.py` | 检查 Markdown 文件的 YAML frontmatter 是否完整（如 topic、version 字段） | `python scripts/general/check_frontmatter.py knowledge/analysis/primitives/` |
| `check_traceability.py` | 检查指定 topic 的 claim→source 追溯链是否完整 | `python scripts/general/check_traceability.py --topic eip-4337` |

### 研究脚本（research/）

| 脚本 | 功能 | 命令示例 |
|------|------|----------|
| `normalize_claims.py` | 标准化 claims 格式，统一 claim_id 命名和 YAML 结构 | `python scripts/research/normalize_claims.py --topic eip-4337` |
| `build_comparison_matrix.py` | 根据多个 topic 的 claims 生成特性对比矩阵（YAML 格式） | `python scripts/research/build_comparison_matrix.py --topics eip-4337,eip-7702 --output comparison.yaml` |
| `validate_sources.py` | 验证来源 URL 是否可访问、证据等级是否适当 | `python scripts/research/validate_sources.py --topic eip-4337` |
| `find_term_drift.py` | 查找某个术语在不同 topic 中的定义是否一致（检测术语漂移） | `python scripts/research/find_term_drift.py --term UserOperation` |
| `validate_draft_diagram_contract.py` | 校验 `draft.md` 中 PlantUML block 的 contract、hash 和 diagram package 一致性 | `python scripts/research/validate_draft_diagram_contract.py openspec/changes/<id>/draft.md` |

### 发布脚本（publish/）

| 脚本 | 功能 | 命令示例 |
|------|------|----------|
| `move_change_outputs.py` | 将通过评审的 change 产物移动到 knowledge/ 长期目录 | `python scripts/publish/move_change_outputs.py --change primitive-eip-4337-deep-dive-pass-1 --topic eip-4337 --domain account-abstraction` |
| `generate_topic_index.py` | 生成或更新 topic 索引 Markdown 文件（含分类和链接） | `python scripts/publish/generate_topic_index.py --output knowledge/indexes/topic-index.md` |

### 图表脚本（diagrams/）

> **重要**：架构图和时序图优先使用用户级 skills（`feipi-plantuml-generate-architecture-diagram` 和 `feipi-plantuml-generate-sequence-diagram`）。
>
> **`check_plantuml.sh` 仅用于手工 troubleshooting，不是 draft pipeline 的正式 gate**。
>
> 正式 PlantUML 验证通过全局 skill 的 `validation.json` 进行。

| 脚本 | 功能 | 命令示例 |
|------|------|----------|
| `check_plantuml.sh` | PlantUML 语法校验（**仅用于手工 troubleshooting**） | `bash scripts/diagrams/check_plantuml.sh diagrams/source/architecture.puml` |
| `validate_diagram_model.py` | 验证 diagram model YAML 的字段完整性（diagram_id、title、components 等） | `python scripts/diagrams/validate_diagram_model.py diagrams/models/architecture-model.yaml` |
| `check_diagram_references.py` | 检查 diagram 在 draft.md 或其他文件中是否被正确引用 | `python scripts/diagrams/check_diagram_references.py architecture --topic eip-4337` |

### OpenSpec 脚本（openspec/）

| 脚本 | 功能 | 命令示例 |
|------|------|----------|
| `new_change.sh` | 创建 OpenSpec change 包，初始化 request.md/plan.md/draft.md 模板 | `bash scripts/openspec/new_change.sh primitive eip-4337-deep-dive-pass-1` |

### 维护脚本（maintenance/）

这些脚本用于仓库运维，不直接参与研究流程。

| 脚本 | 功能 | 命令示例 |
|------|------|----------|
| `install_repo_skills.sh` | 将 skills/ 目录链接到 Codex/Qoder 本地 skills 目录 | `bash scripts/maintenance/install_repo_skills.sh` |
| `render.sh` | 渲染 PlantUML → SVG（**仅用于手工渲染，非正式交付**） | `bash scripts/maintenance/render.sh diagrams/source/architecture.puml --output-dir diagrams/build/` |
| `compare_svg.sh` | 比较两个 SVG 文件的差异（用于检查图表变更） | `bash scripts/maintenance/compare_svg.sh old/architecture.svg new/architecture.svg` |

**注意**：正式 PlantUML 交付必须通过全局 skill 生成，不得直接使用 `render.sh` 渲染手写 PlantUML。

---

## 依赖安装

```bash
pip install pyyaml
```

---

## 脚本分类规则

| 分类 | 放入目录 | 判断标准 |
|------|----------|----------|
| `general/` | 通用工具 | 任何阶段都可用，不特定于某个 workflow |
| `research/` | 研究辅助 | 在 research workflow 中使用（source/atom/comparison） |
| `publish/` | 发布工具 | 在 merge/apply workflow 中使用 |
| `diagrams/` | 图表校验 | 专门用于图表语法校验和引用检查 |
| `openspec/` | OpenSpec 工具 | 与 OpenSpec 变更创建相关的操作 |
| `maintenance/` | 维护工具 | 仓库运维、本地环境配置、临时操作 |

---

## 添加新脚本

1. 确定脚本分类（见上表）
2. 在对应目录创建脚本文件
3. 在本 README.md 中登记（表格 + 树状图）
4. 测试脚本功能
