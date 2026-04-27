---
name: init-change
description: 初始化一个新的研究 change，创建 change.yaml、request.md、plan.md 及完整目录结构。
---

# Skill: Init Change

## Purpose

初始化一个新的研究 change，创建符合 blockchain-research schema 的目录结构与 manifest 文件。

## Triggers

用户请求：
- "创建一个新的研究"
- "初始化 <topic> 的研究"
- "准备研究 <topic>"

## Required Inputs

- **topic**: 研究主题名称
- **task_type**: 对象类型 (primitive/synthesis/decision/source_reading)
- **domain** (可选): 所属域
- **path**: 研究路径 (deep-dive/evolution/scenario/comparison)
- **change_operation**: create / update / extend / supersede / merge

## Forbidden Inputs / Anti-patterns

- 不要在 knowledge/ 下直接创建文件（必须通过 OpenSpec change）
- 不要跳过 request.md 直接写分析
- 不要在没有明确研究问题时开始

## Files to Write

### 1. OpenSpec Change Manifest

在 `openspec/changes/<change-id>/` 创建 `change.yaml`，包含：
- `id`: change 唯一标识
- `schema`: blockchain-research
- `task_type`: primitive / synthesis / decision
- `change_operation`: create / update / extend / supersede / merge
- `execution_scope`: single_artifact
- `instruction`: 研究任务描述
- `profile`: { task, operation }
- `artifacts`: 声明所有 artifact 路径
- `validators`: base / profile / operation 校验器
- `publish_targets`: 从 draft.md 到 knowledge/** 的映射

### 2. 研究文档

- `request.md` — 研究问题定义（目标、边界、非目标、预期输出）
- `plan.md` — 研究执行计划（问题拆解、来源规划、证据矩阵、完成标准）

### 3. 目录结构

```
openspec/changes/<change-id>/
├── change.yaml                  # 必须：change manifest
├── request.md                   # 必须：研究请求
├── plan.md                      # 必须：执行计划
├── sources/                     # 必须：来源目录
│   ├── source-pack.md           # 按需：来源清单
│   └── evidence-map.md          # 按需：证据映射
├── notes/                       # 可选：来源精读笔记
├── claims/                      # 可选：可验证主张
├── decision-criteria.md         # decision 类型时创建
├── draft.md                     # 必须：唯一主候选产物
├── review.md                    # 可选：评审记录
├── publish.md                   # 必须：发布映射
└── validation/                  # 可选：校验结果
```

## Local Validation Steps

1. 检查 change 名称格式：`<type>-<topic>-<path>-pass-1`
2. 检查 request.md 包含 goal/scope/non-goals
3. 检查 change.yaml 包含 task_type、change_operation、artifacts、publish_targets
4. 检查没有直接在 knowledge/ 下创建文件
5. 检查 sources/ 目录已创建

## Output Contract

```yaml
change_id: <生成的 change-id>
change_path: openspec/changes/<change-id>/
status: created
next_step: "编辑 request.md 或使用 /spec-research 辅助生成"
```

## Quality Gate

- [ ] change 名称符合规范
- [ ] change.yaml 包含必要字段（task_type、change_operation、artifacts、publish_targets）
- [ ] request.md 包含 goal/scope/non-goals
- [ ] 目录结构完整（含 sources/、notes/、claims/）

## Failure Modes

### 无法确定对象类型

**处理**：询问用户或默认按 primitive 处理，在 request.md 中标注待确认。

### 类似研究已存在

**处理**：读取现有 artifact，评估是否需要更新而非新建。

### 研究范围过大

**处理**：建议拆分为多个 child changes 或定义 pass 1 范围。

## When to Stop and Ask for Manual Triage

- 用户无法提供明确的研究主题
- 发现高度重复的现有研究
- 研究范围模糊无法界定

## Example Session

```
User: 创建一个新的 EIP-4337 深度研究

Assistant:
1. 确认信息：
   - Topic: eip-4337
   - Task type: primitive
   - Domain: account-abstraction
   - Path: deep-dive

2. 创建 change: primitive-eip-4337-deep-dive-pass-1

3. 创建 change.yaml、request.md、plan.md 及目录结构

4. 输出：
   "已创建研究项目 primitive-eip-4337-deep-dive-pass-1
    下一步：编辑 request.md 或使用 /spec-research 辅助生成"
```
