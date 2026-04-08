# 00 Scope And Boundary

## 目标

把仓库执行面升级为第一版 multi-agent 模式，同时保持 OpenSpec 作为正式规则层不变。

## 本轮要解决什么

- 把“谁负责什么”从隐式 prompt 习惯变成显式 agent contract
- 让 workflow 和命令层统一消费同一套 agent 定义
- 保留独立 review / audit 视角
- 修掉会误导 agent 的关键入口漂移

## 本轮不解决什么

- 不新增 OpenSpec spec 来定义 agent runtime
- 不做完整 Qoder parity
- 不做全仓历史文档清洗
- 不实现专门的调度器程序

## 边界划分

### 必须留在 OpenSpec 的内容

- artifact contract
- apply 准入条件
- 资产模型
- 研究对象模型
- 正式语义约束

### 必须落在 Harness / Commands 的内容

- agent roster
- 激活条件
- handoff artifact
- review / repair / fallback
- 命令如何编排 active agents

## 本轮改造的主文件面

- `harness/agents/`
- `harness/workflows/`
- `.claude/commands/`
- `AGENTS.md`
- 一批关键 rules / skills / README 入口

## 完成定义

满足以下条件即可视为第一版升级完成：

1. `Harness` 中存在正式 agent registry 与 contract。
2. `research-pipeline` 能说明 agent 激活与协作协议。
3. Claude 入口命令改为 agent-aware。
4. 关键入口语义不再与当前 canonical 资产模型冲突。
