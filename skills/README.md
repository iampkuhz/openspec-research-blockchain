# 仓库内置 Skills

这些 skill 用于配合本仓库的 workflow 使用。

---

## Skill  Registry

### Research Skills (`skills/research/`)

| Skill | 用途 | 触发时机 |
|-------|------|----------|
| `create-research-item/` | 初始化研究项目结构 | 创建新研究 |
| `extract-source-pack/` | 从 URL 提取来源包 | 来源收集 |
| `write-definition-atom/` | 编写定义类型笔记 | 定义写作 |
| `write-mechanism-atom/` | 编写机制类型笔记 | 机制写作 |
| `write-evolution-atom/` | 编写演进类型笔记 | 演进写作 |
| `write-comparison-note/` | 编写比较分析笔记 | 比较分析 |
| `review-knowledge-item/` | 评审知识产出物 | 评审阶段 |

### Maintenance Skills (`skills/maintenance/`)

| Skill | 用途 | 触发时机 |
|-------|------|----------|
| `refresh-existing-topic/` | 刷新现有主题 | 更新检查 |
| `merge-change-into-knowledge/` | 合并 change 到 knowledge | apply 阶段 |

### OpenSpec Research Skills (`skills/openspec-research-*/`)

| Skill | 用途 | 触发时机 |
|-------|------|----------|
| `openspec-research-build-plan/` | 辅助生成 plan.md | 计划阶段 |
| `openspec-research-build-draft/` | 辅助生成 draft.md | 写作阶段 |
| `openspec-research-build-artifact/` | 辅助提升到 canonical 资产 | apply 阶段 |

---

## 用户级 Skills（全局）

以下 skills 配置在 `~/.claude/skills/`，优先使用：

| Skill | 用途 |
|-------|------|
| `feipi-plantuml-generate-architecture-diagram` | 生成 PlantUML 架构图 |
| `feipi-plantuml-generate-sequence-diagram` | 生成 PlantUML 时序图 |

---

## Skill 使用方式

### 1. 通过 Workflow 触发

大部分 skills 会在 workflow 执行时自动调用。

示例：
- `intake-workflow.md` → `create-research-item/`
- `source-workflow.md` → `extract-source-pack/`
- `principle-atom-workflow.md` → `write-*-atom/`

### 2. 直接调用

用户可以直接请求使用特定 skill。

示例：
- "使用 `review-knowledge-item` 评审这个 draft"
- "运行 `create-research-item` 创建新研究"

### 3. 通过 OpenSpec 命令

部分技能通过 OpenSpec 命令触发：
```bash
openspec instructions plan --change <name>    # 使用 openspec-research-build-plan
openspec instructions draft --change <name>   # 使用 openspec-research-build-draft
```

---

## 添加新 Skill

1. 在对应类别目录创建 skill 目录
2. 创建 `SKILL.md` 定义触发、输入输出、调用关系
3. 更新本 README.md
4. 测试 skill 功能
