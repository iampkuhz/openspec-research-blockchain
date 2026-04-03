# OpenSpec Changes

这里存放"当前一轮研究改动包"。

## 用途

`openspec/changes/` 用于承载研究过程文件，包括：

- `request.md` - 研究问题定义
- `plan.md` - 研究计划与来源规划
- `draft.md` - 集中 review 稿
- `decision-criteria.md` - 决策标准（可选）
- `sources/` - 来源文件
- `notes/` - 知识笔记
- `review/` - 评审记录

## 与 knowledge/ 的关系

| 位置 | 用途 | 保留内容 |
|------|------|----------|
| `openspec/changes/` | 过程层 | 过程文件、评审记录 |
| `knowledge/analysis/` | 长期资产 | `artifact.md`（稳定分析结果） |
| `knowledge/decisions/` | 长期资产 | `artifact.md` + `verdict.md` |

**重要**：
- 过程文件（`request.md`、`plan.md` 等）**不**进入 `knowledge/`
- 只有稳定的分析结果通过 OpenSpec `apply` 命令提升到 `knowledge/`

## 使用方法

### 1. 创建 Change

```bash
openspec new change <name> --schema blockchain-research
```

命名规范：`<type>-<topic>-<path>-pass-1`

示例：
- `primitive-eip-4337-deep-dive-pass-1`
- `decision-agentic-payment-scenario-pass-1`

### 2. 生成过程文件

```bash
# 生成 plan.md
openspec instructions plan --change <name>

# 生成 draft.md
openspec instructions draft --change <name>
```

### 3. 评审

在 `openspec/changes/<change-id>/review/` 中记录评审意见。

### 4. Apply

```bash
openspec apply --change <name>
```

将稳定内容提升到 `knowledge/`。

## 目录结构

```
openspec/changes/
├── README.md                 # 本文件
├── <change-id>/              # 具体改动包
│   ├── request.md
│   ├── plan.md
│   ├── draft.md
│   ├── sources/
│   ├── notes/
│   └── review/
└── archive/                  # 已完成的改动包（可选）
```

## 生命周期

1. **创建** → 在 `openspec/changes/` 创建改动包
2. **研究** → 填充 `request.md`、`plan.md`、`draft.md`
3. **评审** → 记录评审意见
4. **Apply** → 稳定内容提升到 `knowledge/`
5. **归档** → 可选移动到 `archive/` 或在本地保留

## 本地工作区

默认做法：
- `openspec/changes/<change-id>/` 作为本地工作区使用
- 已完成的 change 可选归档或删除
- 版本库中主要保留 `knowledge/` 长期资产
