# 仓库治理规则

## 目的

定义本仓库的组织原则、目录约束和协作规范。

## 目录治理

### 知识目录分层

```
knowledge/
├── analysis/            # 事实分析资产
│   ├── primitives/      # 底层机制（按领域分组）
│   ├── synthesis/       # 演进/综合分析
│   └── domains/         # 主题域定义
├── decisions/           # 场景决策资产
├── glossary/meta/       # 全局术语 meta 信息
└── indexes/             # 索引文件
```

### 过程目录

```
openspec/
├── changes/             # 进行中的研究变更包
├── schemas/             # 研究 schema 定义
└── specs/               # 研究系统规范
```

### 路由与辅助目录

```
harness/                 # 规则索引、工作流定义
skills/                  # 可复用技能
scripts/                 # 脚本工具
```

## 核心原则

### 原则 1：变更必须走 OpenSpec

**禁止**直接修改 `knowledge/` 下的主线知识。

**必须**通过以下流程：
1. 在 `openspec/changes/` 创建 change
2. 完成研究并产出 draft
3. 通过 review 后 apply 到 knowledge

**例外**：仅当修复明显的拼写错误、格式问题时，可直接修改。

### 原则 2：单一资产模型

**禁止**在 `knowledge/` 下创建 `topics/` 或 `atoms/` 目录。

**必须**：
- primitive/synthesis/domain → `knowledge/analysis/` + `artifact.md`
- decision → `knowledge/decisions/` + `artifact.md` + `verdict.md`

### 原则 3：证据可追溯

**禁止**无来源的主张。

**必须**：
- 每个主张绑定到来源
- 区分 L1/L2/L3/L4 证据等级
- 记录证据缺口

### 原则 4：术语一致性

**禁止**在同一研究中混用不同术语指代同一概念。

**必须**：
- 使用 `knowledge/glossary/meta/` 定义的 taxonomy
- 新建术语时声明 category 和 layer
- 复用已有术语时检查边界

## 命名规范

### Change 命名

格式：`<type>-<topic>-<path>-pass-1`

| 类型 | 说明 | 示例 |
|------|------|------|
| `primitive` | 底层机制 | `primitive-eip-4337-deep-dive-pass-1` |
| `synthesis` | 演进/综合 | `synthesis-aa-eip-evolution-pass-1` |
| `domain` | 主题域 | `domain-account-abstraction-pass-1` |
| `decision` | 场景决策 | `decision-agentic-payment-scenario-pass-1` |

### 分析资产目录命名

| 类型 | 位置 | 命名格式 | 示例 |
|------|------|----------|------|
| primitive | `knowledge/analysis/primitives/<category>/` | `<category>-<name>` | `consensus-malachite` |
| synthesis | `knowledge/analysis/synthesis/<type>/` | `<type>-<name>` | `comparison-bft-consensus` |
| domain | `knowledge/analysis/domains/` | `<domain-name>` | `account-abstraction` |
| decision | `knowledge/decisions/` | `<scenario-name>` | `agentic-payment` |

### 文件命名

- 使用 kebab-case
- 过程文件：`request.md` / `plan.md` / `draft.md`
- 长期资产：`artifact.md` / `verdict.md`
- 评审文件：`review-summary.md`

## 质量门槛

### Change Apply 条件

- [ ] 评审结论为 approved
- [ ] 所有 high severity 问题已修复
- [ ] 术语使用符合 taxonomy
- [ ] 图表通过 validation（如适用）

### 资产更新条件

- [ ] changelog 已更新（如适用）
- [ ] indexes 已更新
- [ ] 依赖的资产已检查兼容性

## 例外处理

### 紧急修复

如需紧急修复主线知识：
1. 先创建 minimal change 记录
2. 修复后补充完整 evidence
3. 在变更记录中说明

### 实验性内容

实验性、未成熟的研究：
1. 放入 `openspec/changes/` 不急于 apply
2. 明确标记 `maturity: experimental`
3. 稳定后再 apply 到 `knowledge/`
