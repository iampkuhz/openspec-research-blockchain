# Intake Workflow - 研究请求接入

## 目标

接收并分类研究请求，确定研究类型、范围和路由。

## 触发条件

用户提出研究需求时触发。

## 必需输入

- 研究主题/问题
- 研究目的（可选）

## 加载规则

- harness/rules/general/repo-governance.md
- harness/rules/general/terminology-policy.md

## 步骤

## 步骤 1：判断研究对象类型

| 类型 | 描述 | 示例 | 产出位置 |
|------|------|------|----------|
| **primitive** | 单个协议/EIP/机制 | eip-4337, consensus-qbft | `knowledge/analysis/primitives/` |
| **synthesis** | 关系/演进/分类分析 | aa-eip-evolution, bft-comparison | `knowledge/analysis/synthesis/` |
| **domain** | 主题域定义 | account-abstraction | `knowledge/analysis/domains/` |
| **decision** | 场景决策 | agentic-payment | `knowledge/decisions/` |

### 步骤 2：判断研究路径

| 路径 | 描述 | 适用类型 |
|------|------|----------|
| `deep-dive` | 单个对象深度分析 | primitive |
| `evolution` | 演进历史分析 | synthesis |
| `scenario` | 场景驱动分析 | decision |

### 步骤 3：检查现有知识

```bash
# 检查 knowledge/analysis/ 和 knowledge/decisions/ 是否已有相关研究
find knowledge/ -name "*<topic>*"
```

**如果有现有知识**：
- 读取 `artifact.md`
- 评估是否需要更新
- 如需更新，走 `update-existing-knowledge.md` 流程

**如果没有**：
- 继续 new-research 流程

### 步骤 4：创建 OpenSpec Change

**必须**创建 `change`，禁止直接修改 `knowledge/`。

```bash
# 使用 OpenSpec 命令
openspec new change <name> --schema blockchain-research
```

命名规范：`<type>-<topic>-<path>-pass-1`

示例：
- `primitive-eip-4337-deep-dive-pass-1`
- `decision-agentic-payment-scenario-pass-1`

### 步骤 5：初始化 request.md

在 `openspec/changes/<change-id>/request.md` 中填写：

- 研究对象类型（primitive/synthesis/domain/decision）
- 研究路径（deep-dive/evolution/scenario）
- 研究背景和目的
- 范围与非目标
- 预期输出

**详情**：`openspec/schemas/blockchain-research/templates/request.md`

## 输出

- 研究对象类型
- 研究路径
- Change ID
- `openspec/changes/<change-id>/request.md`

## 完成标准

- [ ] 对象类型已确定
- [ ] 研究路径已确定
- [ ] `change` 已创建
- [ ] request.md 已填写

## 下一步

→ `harness/workflows/source-workflow.md`（收集 `source`）
→ 或使用 `skills/openspec-research-build-plan/` 辅助生成 plan.md

## 异常处理

### 无法确定对象类型

**处理**：
1. 询问用户更多信息
2. 默认按 primitive 处理
3. 在 request.md 中标注待确认

### 发现类似研究已存在

**处理**：
1. 读取现有 `artifact.md`
2. 评估差异
3. 如差异小，建议 update-research 而非 new-research

### 研究范围过大

**处理**：
1. 拆分为多个 changes
2. 定义 pass 1 范围
3. 在 request.md 说明后续 passes
