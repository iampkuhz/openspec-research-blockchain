# 基于 OpenSpec 的区块链技术调研工作台

这个仓库用于长期维护区块链技术调研资产，区别于一次性报告。研究流程沉淀为可复用的研究系统。

## 仓库定位

六类资产及其位置：

| 资产类型 | 目录 | 说明 |
|---------|------|------|
| 长期事实分析 | `knowledge/analysis/` | primitive / synthesis / domain |
| 长期场景决策 | `knowledge/decisions/` | decision 及其依赖 |
| 当前研究改动包 | `openspec/changes/` | 进行中的研究 |
| 研究系统 specs | `openspec/specs/` | 跨 case 复用的规则 |
| 工作流定义 | `openspec/schemas/` | OpenSpec schema |
| AI 协作技能 | `skills/` | 客户端命令映射 |

## 研究主链

区别于默认 OpenSpec 的 `proposal/spec/design/tasks`，本仓库使用 research-driven 主链：

```
request.md -> plan.md -> draft.md -> promote
```

| 文件 | 作用 |
|------|------|
| `request.md` | 定义问题、范围、非目标 |
| `plan.md` | 研究计划 + 来源规划 |
| `draft.md` | 术语 + 机制分析 + 有限结论 |
| `promote` | 提炼到 `knowledge/.../artifact.md` |

## 对象模型

技术分析主链：`primitive -> [synthesis] -> domain`

- `primitive`：单个协议、EIP、机制
- `synthesis`：多个对象的关系分析（可选）
- `domain`：主题域知识组织层
- `decision`：场景决策（独立层）

约束：`synthesis` 非强制；`domain` 不是 `primitive` 的父目录；一个 primitive 可被多个 domain 复用。

## `knowledge/` 里保留什么

| 文件 | 存放位置 | 说明 |
|------|---------|------|
| `request.md` | `openspec/changes/` | 问题定义，过程文件 |
| `plan.md` | `openspec/changes/` | 研究计划 + 来源规划，过程文件 |
| `draft.md` | `openspec/changes/` | 术语 + 分析 + 结论，过程文件 |
| `artifact.md` | `knowledge/analysis/` 或 `knowledge/decisions/` | 长期正式产物 |
| `dependencies.md` | `openspec/changes/` 或 `knowledge/` | 依赖声明 |
| `criteria.md` | `knowledge/decisions/` | 长期决策标准（decision 专用） |
| `verdict.md` | `knowledge/decisions/` | 条件性结论（decision 专用） |

注：glossary 并入 `artifact.md` 的"关键术语"区，不单独保留。

## 常用命令

### OpenSpec 原生命令

```bash
openspec update                                          # 刷新指令层
openspec new change <name> --schema blockchain-research  # 创建 change
openspec instructions plan --change <name>               # 生成 plan.md
openspec instructions draft --change <name>              # 生成 draft.md
```

### Qoder 快捷命令

```
/spec-plan <change-path>       # request.md -> plan.md
/spec-draft <change-path>      # plan.md -> draft.md
/spec-promote <change-path>    # draft.md -> knowledge/.../artifact.md
/spec-research <change-path>   # 端到端完成全流程
```

### 本地快捷

```bash
make change-primitive NAME=<change-name>  # 创建 primitive change
make install-skills                       # 安装 skills
```

## 使用流程

| 步骤 | 命令 | 检查点 | 产物 |
|------|------|--------|------|
| 1. 开 change | `openspec new change <name> --schema blockchain-research` | 名称、层级是否正确 | `openspec/changes/<name>/` |
| 2. 写 request | 手工编辑 `request.md` 或 `/spec-request` | 只定义问题，不回答机制 | `request.md` |
| 3. 生成 plan | `/spec-plan <path>` | 研究深度、来源、待确认问题 | `plan.md` |
| 4. 生成 draft | `/spec-draft <path>` | 术语表、组件图、角色归属 | `draft.md` |
| 5. 提炼产物 | `/spec-promote <path>` | 无过程痕迹 | `knowledge/.../artifact.md` |

示例（EIP-4337）：
```
openspec new change primitive-eip-4337-deep-dive-pass-1 --schema blockchain-research
# 编辑 request.md 或使用 /spec-request 辅助生成
/spec-plan openspec/changes/primitive-eip-4337-deep-dive-pass-1
# review plan.md
/spec-draft openspec/changes/primitive-eip-4337-deep-dive-pass-1
# review draft.md
/spec-promote openspec/changes/primitive-eip-4337-deep-dive-pass-1
# 产物：knowledge/analysis/primitives/eip-4337/artifact.md
```

**端到端流程**：
```
/spec-research openspec/changes/primitive-eip-4337-deep-dive-pass-1
# 自动完成 request -> plan -> draft -> promote 全流程，每阶段暂停等待确认
```

## 先看哪里

- 快速开始：`AGENTS.md`
- 研究系统 specs：`openspec/specs/`
