# Decisions（场景决策）

这里存放场景决策的长期 artifact。

## 目录结构

```
decisions/
├── agentic-payment/           # 代理支付场景
│   └── chain-comparison/     # 具体决策问题：链选型
├── wallet-selection/          # 未来扩展：钱包选型场景
└── defi-yield/               # 未来扩展：DeFi 收益优化场景
```

## 两层目录结构

Decision 采用**场景 → 具体问题**的两层结构：

### 第一层：场景（Scenario）

定义具体的应用场景，如：
- `agentic-payment`：代理支付场景
- `wallet-selection`：钱包选型场景
- `defi-yield`：DeFi 收益优化场景

### 第二层：具体问题（Specific Decision）

在场景下定义具体的决策问题，如：
- `chain-comparison`：链选型比较
- `wallet-provider-selection`：钱包服务商选择
- `strategy-selection`：策略选择

## 交付物

每个 decision 默认长期保留：
- `artifact.md`：场景分析文档
- `criteria.md`：决策标准（如需要显式比较）
- `dependencies.md`：依赖声明
- `verdict.md`：条件性结论

## 与下层研究的关系

- Decision 必须依赖下层的 primitive/synthesis/domain 研究
- 必须在 `plan.md` 中显式声明依赖
- 依赖深度必须满足决策需求（deep/focused/light）
- Decision 不得重写下层研究的全文，只能引用和综合

## 新增 decision 的流程

1. 创建 change packet：`./scripts/new_change.sh decision <scenario>-<problem>-pass-1`
2. 编写 `request.md` → 生成 `plan.md`（含依赖声明） → 生成 `draft.md` → 提炼 `artifact.md` + `verdict.md`
3. 根据决策场景，放入对应的场景目录

## 命名规范

Decision 目录命名应清晰表达**场景 + 问题**：

**推荐**：
- `agentic-payment/chain-comparison/` ✅
- `wallet-selection/provider-evaluation/` ✅

**不推荐**：
- `agentic-payment/decision-1/` ❌（无意义编号）
- `wallet-selection/final/` ❌（模糊表述）
