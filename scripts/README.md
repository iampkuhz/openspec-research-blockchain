# Scripts

脚本工具目录。

## 结构

```
scripts/
├── README.md             # 本文件
├── general/              # 通用脚本
│   ├── init_research_item.py
│   ├── build_index.py
│   ├── check_frontmatter.py
│   └── check_traceability.py
├── research/             # 研究脚本
│   ├── normalize_claims.py
│   ├── build_comparison_matrix.py
│   ├── validate_sources.py
│   └── find_term_drift.py
├── publish/              # 发布脚本
│   ├── move_change_outputs.py
│   └── generate_topic_index.py
└── diagrams/             # 图表脚本（备选）
    ├── render.sh
    ├── validate_diagram_model.py
    ├── check_diagram_references.py
    └── compare_svg.sh
```

## 使用方法

### 通用脚本

```bash
# 初始化研究项目
python scripts/general/init_research_item.py --topic <topic> --type <primitive|synthesis|domain|decision>

# 构建 topic 索引
python scripts/general/build_index.py --output knowledge/indexes/topic-index.md

# 检查 frontmatter
python scripts/general/check_frontmatter.py [file|directory]

# 检查可追溯性
python scripts/general/check_traceability.py --topic <topic>
```

### 研究脚本

```bash
# 标准化 claims
python scripts/research/normalize_claims.py --topic <topic>

# 构建比较矩阵
python scripts/research/build_comparison_matrix.py --topics topic1,topic2,topic3 --output matrix.yaml

# 验证来源
python scripts/research/validate_sources.py --topic <topic>

# 查找术语漂移
python scripts/research/find_term_drift.py --term <term>
```

### 发布脚本

```bash
# 移动 change 到 knowledge
python scripts/publish/move_change_outputs.py --change <change-id> --topic <topic> --domain <domain>

# 生成 topic 索引
python scripts/publish/generate_topic_index.py --output knowledge/indexes/topic-index.md
```

### 图表脚本（备选）

**注意**：架构图和时序图优先使用用户级 skills（`feipi-gen-plantuml-arch-diagram` 和 `feipi-gen-plantuml-sequence-diagram`）。

以下脚本仅在手动创建图表时使用：

```bash
# 渲染 PlantUML（手动创建时）
./scripts/diagrams/render.sh <diagram.puml> [--output-dir <dir>]

# 验证 diagram model（手动创建时）
python scripts/diagrams/validate_diagram_model.py <model.yaml>

# 检查 diagram 引用（手动创建时）
python scripts/diagrams/check_diagram_references.py <diagram-id> --topic <topic>

# 比较 SVG 差异
./scripts/diagrams/compare_svg.sh <old.svg> <new.svg>
```

## 依赖

Python 脚本需要以下依赖：

```bash
pip install pyyaml
```

## 添加新脚本

1. 确定脚本类别（general/research/publish）
2. 在对应目录创建脚本
3. 更新本 README.md
4. 测试脚本功能
