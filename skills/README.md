# skills/ — 仓库内置 Skills（迁移说明）

> **迁移状态**：本目录仍为 skill 定义的真源（source of truth）。
> `.claude/skills/` 已创建并包含指向本目录的符号链接。
> 新增或修改 skill 时，请在 `skills/` 下操作，然后在 `.claude/skills/` 下创建对应符号链接。

这些 skill 是 workflow 的叶子执行单元。

使用顺序应保持渐进式加载：

1. 先从 `AGENTS.md`、`CLAUDE.md`、`harness/workflows/_index.yaml` 判断任务类型
2. 再读取对应 workflow 与 `harness/rules/_phase_index.yaml`
3. 只有在阶段需要具体动作时，才展开到这里对应的 `SKILL.md`

本 README 只回答两类问题：
- 什么场景会启用这个 skill
- 应该打开哪个 `SKILL.md` 查看具体执行约束

---

## Skill Registry

### Research Skills (`skills/research/`)

| Skill | 用途 | 常见触发点 |
|-------|------|------------|
| `create-research-item/` | 初始化研究项目结构 | `intake-workflow.md` / `new_change.sh` 前后 |
| `extract-source-pack/` | 从 URL 提取来源包 | `source-workflow.md` |
| `write-definition-atom/` | 编写定义型 primitive 笔记 | 专项 research workflow |
| `write-mechanism-atom/` | 编写机制型 primitive 笔记 | 专项 research workflow |
| `write-evolution-atom/` | 编写演进型 primitive 笔记 | 专项 research workflow |
| `write-comparison-note/` | 编写横向比较笔记 | synthesis / comparison workflow |
| `review-knowledge-item/` | 评审知识产出物 | `review-workflow.md` |

### Maintenance Skills (`skills/maintenance/`)

| Skill | 用途 | 常见触发点 |
|-------|------|------------|
| `refresh-existing-topic/` | 刷新现有主题 | update / maintenance 场景 |
| `merge-change-into-knowledge/` | 合并 change 到 knowledge | apply / publish 场景 |

### OpenSpec Research Skills (`skills/openspec-research-*/`)

| Skill | 用途 | 常见触发点 |
|-------|------|------------|
| `openspec-research-build-request/` | 生成或修订 `request.md` | request 阶段 |
| `openspec-research-build-plan/` | 生成或修订 `plan.md` | plan 阶段 |
| `openspec-research-build-draft/` | 生成或修订 `draft.md` | draft 阶段 |
| `openspec-research-build-artifact/` | 提炼长期 `artifact.md` / `verdict.md` | artifact 阶段 |
| `openspec-research-build-research/` | 端到端串联 request → artifact | `research-pipeline.md` |

---

## 用户级 Skills（全局）

以下 global skills 不在本仓库内维护，但 workflow 会显式依赖它们：

| Skill | 用途 | 常见触发点 |
|-------|------|------------|
| `feipi-plantuml-generate-architecture-diagram` | 生成 PlantUML 架构图 | diagram / draft 阶段 |
| `feipi-plantuml-generate-sequence-diagram` | 生成 PlantUML 时序图 | diagram / draft 阶段 |

---

## 使用原则

### 1. 先 workflow，后 skill

不要从 skill 反推流程。
应先确定当前处于哪个 workflow / phase，再打开对应 `SKILL.md`。

### 2. skill 只负责叶子动作

`SKILL.md` 负责：
- 输入输出
- 调用时机
- 叶子动作约束

`SKILL.md` 不应复制上位 workflow / spec 的完整正文。

### 3. 以阶段入口为真源

若 `SKILL.md` 与以下文件冲突，以这些入口为准：
- `harness/workflows/*.md`
- `harness/rules/_phase_index.yaml`
- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/specs/*.md`

---

## 直接入口

如需查看具体执行说明，直接打开对应文件：

- `skills/openspec-research-build-request/SKILL.md`
- `skills/openspec-research-build-plan/SKILL.md`
- `skills/openspec-research-build-draft/SKILL.md`
- `skills/openspec-research-build-artifact/SKILL.md`
- `skills/openspec-research-build-research/SKILL.md`

---

## 维护要求

新增或调整 skill 时，至少同步更新：

1. 本 README 的索引
2. 对应 `SKILL.md` 的输入输出
3. 触发它的 workflow / command / agent 文档
4. 如有脚本 gate，补充脚本路径与验收方式
