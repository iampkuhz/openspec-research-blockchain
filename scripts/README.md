# Scripts 工具集

本目录包含仓库自动化脚本工具。

脚本是 workflow / skill 的辅助校验层，不应替代上位规范。
使用顺序应为：

1. 先从 `AGENTS.md`、`CLAUDE.md`、`harness/workflows/_index.yaml` 判断当前阶段
2. 再从 workflow / skill 中定位需要的脚本 gate
3. 最后只运行该阶段显式声明需要的脚本

本 README 只做脚本索引，不单独定义研究流程。

---

## 目录结构

```text
scripts/
├── README.md
├── general/
│   ├── init_research_item.py
│   ├── check_frontmatter.py
│   ├── check_traceability.py
│   └── validate_knowledge_tree.py
├── research/
│   ├── normalize_claims.py
│   ├── build_comparison_matrix.py
│   ├── validate_sources.py
│   ├── find_term_drift.py
│   ├── check_artifact_contract.py
│   └── validate_draft_diagram_contract.py
├── publish/
│   └── move_change_outputs.py
├── diagrams/
│   ├── check_plantuml.sh
│   ├── validate_diagram_model.py
│   └── check_diagram_references.py
├── openspec/
│   └── new_change.sh
└── maintenance/
    ├── install_repo_skills.sh
    ├── render.sh
    └── compare_svg.sh
```

---

## 使用方法

### 通用脚本（general/）

| 脚本 | 功能 | 命令示例 |
|------|------|----------|
| `init_research_item.py` | 初始化研究项目结构，创建必要目录和空文件 | `python scripts/general/init_research_item.py --topic eip-4337 --type primitive` |
| `check_frontmatter.py` | 检查 `knowledge/` 下长期 Markdown 的 YAML frontmatter 是否完整 | `python scripts/general/check_frontmatter.py knowledge/analysis/primitives/` |
| `check_traceability.py` | 检查指定 topic 的 claim→source 追溯链是否完整 | `python scripts/general/check_traceability.py --topic eip-4337` |
| `validate_knowledge_tree.py` | 校验 `knowledge/` 树是否满足长期目录结构约束 | `python scripts/general/validate_knowledge_tree.py knowledge` |

### 研究脚本（research/）

| 脚本 | 功能 | 命令示例 |
|------|------|----------|
| `normalize_claims.py` | 标准化 claims 格式，统一 claim_id 命名和 YAML 结构 | `python scripts/research/normalize_claims.py --topic eip-4337` |
| `build_comparison_matrix.py` | 根据多个 topic 的 claims 生成特性对比矩阵 | `python scripts/research/build_comparison_matrix.py --topics eip-4337,eip-7702 --output comparison.yaml` |
| `validate_sources.py` | 验证来源 URL 是否可访问、证据等级是否适当 | `python scripts/research/validate_sources.py --topic eip-4337` |
| `find_term_drift.py` | 查找术语在不同 topic 中的定义是否一致 | `python scripts/research/find_term_drift.py --term UserOperation` |
| `check_artifact_contract.py` | 校验长期 `artifact.md` / `verdict.md` 的 frontmatter 与 object contract | `python scripts/research/check_artifact_contract.py knowledge` |
| `validate_draft_diagram_contract.py` | 校验 `draft.md` 中 diagram contract、hash 与 package 一致性 | `python scripts/research/validate_draft_diagram_contract.py openspec/changes/<id>/draft.md` |

### 发布脚本（publish/）

| 脚本 | 功能 | 命令示例 |
|------|------|----------|
| `move_change_outputs.py` | 将通过评审的 change 产物移动到 `knowledge/` 长期目录 | `python scripts/publish/move_change_outputs.py --change primitive-eip-4337-deep-dive-pass-1 --topic eip-4337 --domain account-abstraction` |

### 图表脚本（diagrams/）

> 重要：架构图和时序图优先使用用户级 skills（`feipi-plantuml-generate-architecture-diagram` 和 `feipi-plantuml-generate-sequence-diagram`）。
>
> `check_plantuml.sh` 仅用于手工 troubleshooting，不是 draft pipeline 的正式 gate。
>
> 正式 PlantUML 验证通过全局 skill 产出的 `validation.json` 进行。

| 脚本 | 功能 | 命令示例 |
|------|------|----------|
| `check_plantuml.sh` | PlantUML 语法校验，仅用于手工 troubleshooting | `bash scripts/diagrams/check_plantuml.sh diagrams/source/architecture.puml` |
| `validate_diagram_model.py` | 验证 diagram model YAML 的字段完整性 | `python scripts/diagrams/validate_diagram_model.py diagrams/models/architecture-model.yaml` |
| `check_diagram_references.py` | 检查 diagram 在 `draft.md` 或其他文件中是否被正确引用 | `python scripts/diagrams/check_diagram_references.py architecture --topic eip-4337` |

### OpenSpec 脚本（openspec/）

| 脚本 | 功能 | 命令示例 |
|------|------|----------|
| `new_change.sh` | 创建 OpenSpec change 包，初始化模板文件 | `bash scripts/openspec/new_change.sh primitive eip-4337-deep-dive-pass-1` |

### 维护脚本（maintenance/）

这些脚本用于仓库运维，不直接参与研究流程。

| 脚本 | 功能 | 命令示例 |
|------|------|----------|
| `install_repo_skills.sh` | 将 `skills/` 目录链接到本地 skills 目录 | `bash scripts/maintenance/install_repo_skills.sh` |
| `render.sh` | 渲染 PlantUML → SVG，仅用于手工渲染 | `bash scripts/maintenance/render.sh diagrams/source/architecture.puml --output-dir diagrams/build/` |
| `compare_svg.sh` | 比较两个 SVG 文件差异 | `bash scripts/maintenance/compare_svg.sh old/architecture.svg new/architecture.svg` |

正式 PlantUML 交付必须通过全局 skill 生成，不得直接使用 `render.sh` 作为正式产出路径。

---

## 与 workflow 的关系

| 阶段 | 常用脚本 | 说明 |
|------|----------|------|
| draft | `validate_draft_diagram_contract.py` | 校验 diagram package 与 draft contract |
| source review | `validate_sources.py` | 验证来源可访问性与证据级别 |
| artifact / apply | `check_frontmatter.py`、`check_artifact_contract.py`、`validate_knowledge_tree.py` | 校验长期资产结构、frontmatter 与目录落点 |

如果 workflow / skill 没有显式要求某个脚本，不应机械性全部运行。

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
| `research/` | 研究辅助 | 在 research workflow 中使用 |
| `publish/` | 发布工具 | 在 merge / apply workflow 中使用 |
| `diagrams/` | 图表校验 | 专门用于图表语法校验和引用检查 |
| `openspec/` | OpenSpec 工具 | 与 OpenSpec change 创建相关 |
| `maintenance/` | 维护工具 | 仓库运维、本地环境配置、临时操作 |

---

## 添加新脚本

1. 确定脚本分类
2. 在对应目录创建脚本文件
3. 在本 README 中登记
4. 补充调用它的 workflow / skill / command 文档
5. 测试脚本功能
