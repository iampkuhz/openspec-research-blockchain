# 仓库治理规则

## 目的

定义本仓库的组织原则、目录约束和协作规范。

## 目录治理

### 知识目录分层

```
knowledge/
├── glossary/          # 全局术语 meta 信息（非具体术语表）
├── domains/           # 主题域知识组织层
├── topics/            # 具体主题（primitive / synthesis）
├── indexes/           # 索引文件
└── templates/         # 知识模板
```

### 变更管理目录

```
openspec/
├── changes/           # 进行中的研究变更包
├── templates/         # Change 模板
└── archive/           # 归档的旧变更
```

### 能力目录

```
harness/               # 规则、工作流、提示词、评估
skills/                # 可复用技能
scripts/               # 脚本工具
```

## 核心原则

### 原则 1：变更必须走 OpenSpec

**禁止**直接修改 `knowledge/` 下的主线知识。

**必须**通过以下流程：
1. 在 `openspec/changes/` 创建 change
2. 完成研究并产出 draft
3. 通过 review 后 merge 到 knowledge

**例外**：仅当修复明显的拼写错误、格式问题时，可直接修改。

### 原则 2：原子化知识

**禁止**将不同主题混在同一文件。

**必须**：
- 每个 topic 有独立的目录
- 支持拆分为多个 atom（definition / mechanism / evolution）
- claims 与 atoms 一一对应

### 原则 3：证据可追溯

**禁止**无来源的主张。

**必须**：
- 每个 claim 绑定到 source id
- 区分 L1/L2/L3/L4 证据等级
- 记录 evidence gaps

### 原则 4：术语一致性

**禁止**在同一 topic 内混用不同术语指代同一概念。

**必须**：
- 使用 `knowledge/glossary/meta/` 定义的 taxonomy
- 新建术语时声明 category 和 layer
- 复用已有术语时检查边界

## 命名规范

### Change 命名

格式：`<topic>-<path>-<pass>`

示例：
- `primitive-eip-4337-deep-dive-pass-1`
- `evolution-aa-eip-pass-2`
- `comparison-bft-consensus-pass-1`

### Topic 命名

- primitive: 使用技术名称（eip-4337, consensus-qbft）
- synthesis: 使用关系描述（bft-comparison, aa-evolution）
- domain: 使用主题名称（account-abstraction, agentic-payment）

### 文件命名

- 使用 kebab-case
- 模板文件使用 `.template.md` 或 `.template.yaml` 后缀
- 评审文件使用 `-review.md` 后缀

## 质量门槛

### Change 合并条件

- [ ] 所有 claims 都有 source 绑定
- [ ] 术语使用符合 taxonomy
- [ ] 图表通过 validation
- [ ] review 问题都已解决或记录为 open questions

### Topic 更新条件

- [ ] changelog.md 已更新
- [ ] 相关 indexes 已更新
- [ ] 依赖的 topics 已检查兼容性

## 例外处理

### 紧急修复

如需紧急修复主线知识：
1. 先创建 minimal change 记录
2. 修复后补充完整 evidence
3. 在 changelog.md 中说明

### 实验性内容

实验性、未成熟的研究：
1. 放入 `openspec/changes/` 不急于 merge
2. 或创建 `knowledge/topics/.experimental/` 子目录
3. 明确标记 maturity: experimental
