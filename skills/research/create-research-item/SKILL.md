---
name: create-research-item
description: 初始化一个新的研究项目，创建完整的目录结构和模板文件。
---

# Skill: Create Research Item

## Purpose

初始化一个新的研究项目，创建完整的目录结构和模板文件。

## Triggers

用户请求：
- "创建一个新的研究"
- "初始化 <topic> 的研究"
- "准备研究 <topic>"

## Required Inputs

- **topic**: 研究主题名称
- **type**: 研究对象类型 (primitive/synthesis/domain/decision)
- **domain** (可选): 所属域
- **path**: 研究路径 (deep-dive/evolution/scenario/comparison)

## Forbidden Inputs / Anti-patterns

- 不要在 knowledge/ 下直接创建文件（必须通过 OpenSpec change）
- 不要跳过 request.md 直接写分析
- 不要在没有明确研究问题时开始

## Files to Read

- `harness/workflows/intake-workflow.md` - 接入流程
- `harness/rules/general/repo-governance.md` - 仓库治理规则
- `knowledge/templates/topic-template/` - 知识模板

## Files to Write

### 1. OpenSpec Change

在 `openspec/changes/<change-id>/` 创建：

- `request.md` - 研究问题定义
- `plan.md` - 研究计划和来源规划
- `.openspec.yaml` - OpenSpec 元数据

### 2. 目录结构

```
openspec/changes/<change-id>/
├── request.md
├── plan.md
├── sources/
│   ├── inbox.yaml
│   └── fetched/
└── .openspec.yaml
```

## Local Validation Steps

1. 检查 change 名称格式：`<type>-<topic>-<path>-pass-1`
2. 检查 request.md 包含必要字段
3. 检查没有直接在 knowledge/ 下创建文件

## Output Contract

```yaml
change_id: <生成的 change-id>
change_path: openspec/changes/<change-id>/
status: created
next_step: "编辑 request.md 或使用 /spec-request 辅助生成"
```

## Quality Gate

- [ ] change 名称符合规范
- [ ] request.md 包含 goal/scope/non-goals
- [ ] 目录结构完整
- [ ] .openspec.yaml 正确配置 schema

## Failure Modes

### 无法确定对象类型

**处理**：询问用户或默认按 primitive 处理，在 request.md 中标注待确认。

### 类似研究已存在

**处理**：读取现有 artifact.md，评估是否需要更新而非新建。

### 研究范围过大

**处理**：建议拆分为多个 changes 或定义 pass 1 范围。

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
   - Type: primitive
   - Domain: account-abstraction
   - Path: deep-dive

2. 创建 change: primitive-eip-4337-deep-dive-pass-1

3. 创建目录结构和 request.md

4. 输出：
   "已创建研究项目 primitive-eip-4337-deep-dive-pass-1
    下一步：编辑 request.md 或使用 /spec-request 辅助生成"
```
