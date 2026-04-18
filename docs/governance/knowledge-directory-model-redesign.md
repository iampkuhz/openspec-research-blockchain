# Knowledge 目录模型改造说明

## 目的

本文定义 `knowledge/` 长期资产目录的改造目标、目录模型、元数据规范、模板约束和校验脚本方案。

本说明文档当前作为治理设计文档使用，先用于统一目录模型与校验口径；后续如需正式收敛到 OpenSpec / Harness，再拆分进入 `openspec/specs/`、`openspec/config.yaml` 和相关 workflow/rules。

---

## 设计结论

### 核心原则

1. `knowledge/` 顶层继续保留两类长期资产：
   - `analysis/`：长期事实分析
   - `decisions/`：长期场景判断
2. `primitive` 按 `domain` 分组，`domain` 通过目录结构直接体现。
3. `synthesis` 在 `analysis/` 下扁平化存放，不再强制设置二级子目录。
4. `decision` 保持独立，不塞回 `analysis/` 或 `domain` 目录树。
5. 路径负责表达“分类和浏览入口”，frontmatter 负责表达“内容语义与校验信息”，registry 负责表达“枚举值定义”。

### 不再采用的做法

- 不再把 `domain` 视为 `object_type`。
- 不再要求为每个 `domain` 单独建设长期 `artifact.md`。
- 不再在 frontmatter 中保留 `status`。
- 不再在 frontmatter 中保留 `source_change`。
- 不再把 `topic_slug`、`primary_domain`、`decision_space` 作为 frontmatter 的必填字段；这些由路径推导。

---

## 术语约定

### `object_type`

长期研究对象只保留三类：

- `primitive`
- `synthesis`
- `decision`

### `domain`

`domain` 是 taxonomy / 浏览分组概念，不是独立 `object_type`。

它的职责是：

- 作为 `primitive` 的主分组轴
- 提供统一命名空间
- 为 `related_domains` 提供候选值集合

### `topic_slug`

`topic_slug` 指叶子目录名，用于表达当前研究对象自己的短名字。

示例：

- `knowledge/analysis/primitives/consensus/qbft/artifact.md`
  - `topic_slug = qbft`
- `knowledge/analysis/primitives/account-abstraction/eip-4337/artifact.md`
  - `topic_slug = eip-4337`
- `knowledge/analysis/primitives/agentic-payment/ap2/artifact.md`
  - `topic_slug = ap2`
- `knowledge/analysis/synthesis/bft-comparison/artifact.md`
  - `topic_slug = bft-comparison`

`topic_slug` 由路径推导，不要求在 frontmatter 中重复声明。

### `research_depth`

`research_depth` 是长期资产的研究深度标记，用于表达当前 artifact 的完成度和可复用边界。

候选值：

- `deep`
- `focused`
- `light`

它不决定文件名，不决定对象类型，也不决定目录位置。

---

## 目录模型

### Canonical 目录树

```text
knowledge/
  README.md

  analysis/
    README.md
    _registry/
      domains.yaml
      synthesis-kinds.yaml

    primitives/
      <domain_id>/
        README.md
        <topic_slug>/
          artifact.md

    synthesis/
      <topic_slug>/
        artifact.md

  decisions/
    README.md
    <decision_space>/
      README.md
      <topic_slug>/
        artifact.md
        verdict.md
        criteria.md              # 可选，仅复杂决策保留
```

### 路径语义

#### `analysis/primitives/<domain_id>/<topic_slug>/artifact.md`

用于存放单一协议、EIP、机制、能力单元的长期分析。

路径中各段含义：

- `primitives`：对象类型
- `<domain_id>`：主分组 domain
- `<topic_slug>`：当前 primitive 的短名字

#### `analysis/synthesis/<topic_slug>/artifact.md`

用于存放演进、比较、分类、关系分析。

`synthesis` 目录刻意扁平化，不再用目录层级硬编码 `comparison/`、`evolution/`、`taxonomy/`，这些通过 frontmatter 的 `synthesis_kind` 表达。

#### `decisions/<decision_space>/<topic_slug>/artifact.md`

用于存放场景判断型分析正文。

#### `decisions/<decision_space>/<topic_slug>/verdict.md`

用于存放条件性结论。`decision` 的长期结论单独存在，不与 `artifact.md` 混写。

#### `criteria.md`

仅当决策问题复杂且需要显式评审标准时保留。

---

## 需要建设的内容

### 1. 顶层说明文件

需要维护：

- `knowledge/README.md`
- `knowledge/analysis/README.md`
- `knowledge/decisions/README.md`

职责：

- 解释目录语义
- 解释收录范围
- 解释 registry 的位置
- 解释不同对象的最小交付物

### 2. Registry 文件

需要新增：

- `knowledge/analysis/_registry/domains.yaml`
- `knowledge/analysis/_registry/synthesis-kinds.yaml`

职责：

- 为 `domain` 提供统一候选值
- 为 `synthesis_kind` 提供统一候选值
- 为校验脚本提供枚举来源

### 3. 分组 README

建议维护：

- `knowledge/analysis/primitives/<domain_id>/README.md`
- `knowledge/decisions/<decision_space>/README.md`

职责：

- 说明该目录收什么、不收什么
- 解释该 domain 或 decision space 的边界
- 提供目录内对象列表的人工入口

注意：这些 README 是目录说明，不是研究 artifact。

### 4. 长期 artifact 文件

每个研究对象只保留自己的 canonical 文件：

- `primitive`：`artifact.md`
- `synthesis`：`artifact.md`
- `decision`：`artifact.md` + `verdict.md`

复杂决策可额外保留：

- `criteria.md`

---

## Registry 模板

### `knowledge/analysis/_registry/domains.yaml`

```yaml
domains:
  - id: consensus
    title: 共识
    description: 共识协议、投票流程、视图切换、最终性等机制分析
    aliases: []
    includes:
      - qbft
      - tendermint
      - simplex
      - malachite
    excludes:
      - 钱包产品能力

  - id: account-abstraction
    title: 账户抽象
    description: 账户模型、授权、执行入口、签名验证与 sponsor 相关机制
    aliases:
      - aa
    includes:
      - eip-4337
      - eip-7702
      - eip-7560
      - eip-4361-siwe
    excludes:
      - 纯支付路由协议

  - id: agentic-payment
    title: Agentic Payment
    description: agent 支付所需的发现、授权、谈判、支付传输与执行相关原语
    aliases: []
    includes:
      - a2a
      - ap2
      - acp
      - x402
      - mpp
    excludes:
      - 泛用 AI 编码工作流
```

### `knowledge/analysis/_registry/synthesis-kinds.yaml`

```yaml
kinds:
  - id: comparison
    title: 对比分析
    description: 横向比较多个对象的能力、边界、取舍或场景适配

  - id: evolution
    title: 演进分析
    description: 追踪一个问题域中多个对象的历史演进与替代关系

  - id: taxonomy
    title: 分类分析
    description: 形成层级、分类学或映射框架

  - id: landscape
    title: 全景分析
    description: 面向一个较大主题的体系化梳理，但不输出场景 verdict
```

---

## Frontmatter 规范

## 基本原则

1. frontmatter 是每个长期 Markdown 文档顶部的 YAML 块，不是全仓库共享单文件。
2. 能从路径推导的信息，不在 frontmatter 中重复维护。
3. frontmatter 只保留长期可复用、适合脚本校验的最小字段。

### 通用必填字段

适用于所有长期 `artifact.md`，以及 `decision` 的 `verdict.md`：

| 字段 | 类型 | 说明 |
|------|------|------|
| `object_type` | string | `primitive / synthesis / decision` |
| `title` | string | 用户可读标题 |
| `research_depth` | string | `deep / focused / light` |
| `updated_at` | date | 最后一次内容确认日期 |

### 通用可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `related_domains` | string[] | 当前对象还关联哪些 domain |
| `summary` | string | 一句话摘要，便于后续导航或索引 |

### `primitive` 额外字段

无额外必填字段。

`primary_domain` 由路径推导：

- `knowledge/analysis/primitives/account-abstraction/eip-4337/artifact.md`
  - `primary_domain = account-abstraction`

### `synthesis` 额外必填字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `synthesis_kind` | string | 必须来自 `synthesis-kinds.yaml` |

### `decision` 额外字段

无额外必填字段。

`decision_space` 由路径推导：

- `knowledge/decisions/agentic-payment/chain-comparison/artifact.md`
  - `decision_space = agentic-payment`

### 不再保留的字段

以下字段不进入新的长期 frontmatter：

- `status`
- `source_change`
- `topic_slug`
- `primary_domain`
- `decision_space`

说明：

- `topic_slug`、`primary_domain`、`decision_space` 已由路径表达。
- `status` 容易与研究深度、发布状态、审核状态混淆。
- `source_change` 属于过程层信息；change 归档后不应成为长期资产 frontmatter 的强绑定字段。

---

## Research Depth 规范

### 候选值

#### `deep`

适用场景：

- 该对象是核心基础对象
- 后续会被频繁复用
- 需要作为 `synthesis` 或 `decision` 的关键依赖

处理差异：

- 需要完整覆盖核心机制与边界
- 需要能够单独成为长期 reference
- 对 `primitive` 来说应优先覆盖结构、流程、取舍、边界和相关对象关系

#### `focused`

适用场景：

- 本轮只回答一个明确的子问题
- 需要可靠结论，但不追求全景覆盖
- 只服务当前某个 `synthesis` 或 `decision` 的一组依赖抽取

处理差异：

- 允许聚焦某一机制切片
- 允许省略与当前问题无关的全景部分
- 必须明确写出“本稿没有覆盖什么”

#### `light`

适用场景：

- 只需建立基本事实认知
- 只是辅助性对象
- 当前没有足够预算做深挖

处理差异：

- 只确认最核心事实和边界
- 必须明确证据缺口
- 不应作为高风险 `decision` 的唯一底层依据

### 是否为不同深度生成不同文件

不生成不同文件。

同一对象无论是 `light`、`focused` 还是 `deep`，长期 canonical 文件都保持为：

- `artifact.md`

原因：

1. 同一研究对象应该只有一个长期 canonical 正文。
2. 深度是“当前完成度”，不是“对象类型”。
3. 未来应支持同一路径内的深度升级：
   - `light -> focused -> deep`
4. 如果用不同文件名承载深度，会造成长期资产分裂和引用不稳定。

### 对内容的影响

深度不改变文件名，但改变内容最低要求。

#### `primitive`

| 深度 | 最低要求 |
|------|----------|
| `deep` | 必须包含：关键术语、研究范围、组件/角色结构、核心流程、设计取舍、能力边界、相关对象关系、证据缺口、参考资料 |
| `focused` | 必须包含：关键术语、问题聚焦范围、相关结构或流程切片、边界、有限结论、证据缺口、参考资料 |
| `light` | 必须包含：对象定义、与相邻对象边界、当前确认点、未覆盖范围、证据缺口、参考资料 |

#### `synthesis`

| 深度 | 最低要求 |
|------|----------|
| `deep` | 必须包含：分析框架、对象定位、关系分析、趋势或结构结论、依赖说明、证据缺口 |
| `focused` | 必须包含：比较或演进主线、当前依赖对象、有限结论、证据缺口 |
| `light` | 仅适合很小的梳理性综述；必须说明依赖不足与适用边界 |

#### `decision`

| 深度 | 最低要求 |
|------|----------|
| `deep` | 必须包含：场景定义、判断维度、依赖抽取、主要 trade-off、artifact 正文 + 条件性 verdict |
| `focused` | 必须包含：核心场景、关键比较维度、当前可成立判断、artifact 正文 + verdict |
| `light` | 仅允许做初筛或方向判断，不允许写成确定排名 |

---

## 模板

## 1. Primitive `artifact.md` 模板

### Frontmatter

```yaml
---
object_type: primitive
title: "<标题>"
research_depth: deep
related_domains:
  - <可选关联 domain>
summary: "<一句话摘要>"
updated_at: 2026-04-19
---
```

### 正文模板

```markdown
# <标题>

## 研究范围

说明本稿回答什么问题，不回答什么问题。

## 关键术语

| 术语 | 定义 | 在本题中的作用 |
|------|------|---------------|
| ... | ... | ... |

## 结构与角色

说明对象的主要组件、角色或分层。

## 核心流程

说明最关键的执行流程或机制路径。

## 设计取舍

回答“为什么这样设计，而不是那样设计”。

## 能力边界

说明能解决什么，不能解决什么，依赖什么前提。

## 相关对象关系

说明与相邻 protocol / EIP / 机制的关系。

## 当前可确认结论

- ...

## Evidence Gap

- ...

## 参考资料

| 来源 | 说明 |
|------|------|
| ... | ... |
```

### Primitive 示例文件头

路径：
`knowledge/analysis/primitives/account-abstraction/eip-4337/artifact.md`

```yaml
---
object_type: primitive
title: "EIP-4337 Account Abstraction"
research_depth: deep
related_domains:
  - agentic-payment
summary: "解释 EIP-4337 的执行入口、角色分层、设计取舍与能力边界。"
updated_at: 2026-04-19
---
```

## 2. Synthesis `artifact.md` 模板

### Frontmatter

```yaml
---
object_type: synthesis
title: "<标题>"
research_depth: focused
synthesis_kind: comparison
related_domains:
  - <可选关联 domain>
summary: "<一句话摘要>"
updated_at: 2026-04-19
---
```

### 正文模板

```markdown
# <标题>

## 研究问题

明确本 synthesis 到底比较什么、演进什么或映射什么。

## 依赖对象

| 对象 | 类型 | 当前使用方式 |
|------|------|-------------|
| ... | ... | ... |

## 分析框架

给出比较维度、演进阶段或分类框架。

## 对象定位

说明各对象在当前问题中的位置。

## 关系分析

说明替代、互补、继承、冲突或演进关系。

## 当前可确认结论

- ...

## Evidence Gap

- ...

## 参考资料

| 来源 | 说明 |
|------|------|
| ... | ... |
```

### Synthesis 示例文件头

路径：
`knowledge/analysis/synthesis/bft-comparison/artifact.md`

```yaml
---
object_type: synthesis
title: "BFT 共识算法对比分析"
research_depth: focused
synthesis_kind: comparison
related_domains:
  - consensus
summary: "对比多种 BFT 共识实现的流程、取舍和适用边界。"
updated_at: 2026-04-19
---
```

## 3. Decision `artifact.md` 模板

### Frontmatter

```yaml
---
object_type: decision
title: "<标题>"
research_depth: focused
related_domains:
  - <可选关联 domain>
summary: "<一句话摘要>"
updated_at: 2026-04-19
---
```

### 正文模板

```markdown
# <标题>

## 场景定义

明确当前要做什么判断，不回答什么。

## 判断维度

列出本次判断真正采用的比较维度。

## 依赖抽取

说明本 decision 依赖哪些下层研究，以及只抽取了什么。

## 对比分析

围绕场景进行对比，不重写下层完整机制。

## 主要 trade-off

说明当前对象之间的关键取舍。

## 当前可成立判断

- ...

## 未决问题

- ...

## 参考资料

| 来源 | 说明 |
|------|------|
| ... | ... |
```

### Decision `verdict.md` 模板

```yaml
---
object_type: decision
title: "<标题> Verdict"
research_depth: focused
related_domains:
  - <可选关联 domain>
summary: "<一句话摘要>"
updated_at: 2026-04-19
---
```

```markdown
# 结论

## 结论范围

说明 verdict 只回答什么，不回答什么。

## 当前可以成立的结论

- ...

## 结论成立的前提

- ...

## 不应过度推出的结论

- ...

## 后续动作

- ...
```

### Decision 示例文件头

路径：
`knowledge/decisions/agentic-payment/chain-comparison/artifact.md`

```yaml
---
object_type: decision
title: "Agentic Payment 链能力比较"
research_depth: focused
related_domains:
  - agentic-payment
  - account-abstraction
summary: "面向 agentic payment 场景比较不同候选链的能力边界和场景适配。"
updated_at: 2026-04-19
---
```

---

## 校验脚本方案

## 总体思路

目录模型改造后，校验分成三层：

1. 路径结构校验
2. frontmatter 校验
3. 内容契约校验

### 建议新增 / 调整的脚本

#### 1. 升级 `scripts/general/check_frontmatter.py`

职责：

- 校验长期 Markdown 是否有合法 frontmatter
- 按 `object_type` 校验必填字段
- 校验 `research_depth` 枚举
- 校验 `synthesis_kind` 是否出现在 registry 中
- 校验 `related_domains` 是否都出现在 `domains.yaml` 中
- 拒绝已废弃字段：
  - `status`
  - `source_change`
  - `topic_slug`
  - `primary_domain`
  - `decision_space`

额外校验：

- `primitive` 文件必须位于 `knowledge/analysis/primitives/<domain>/<topic>/artifact.md`
- `synthesis` 文件必须位于 `knowledge/analysis/synthesis/<topic>/artifact.md`
- `decision` 文件必须位于 `knowledge/decisions/<space>/<topic>/artifact.md` 或 `verdict.md`

#### 2. 新增 `scripts/general/validate_knowledge_tree.py`

职责：

- 校验 `knowledge/` 目录结构是否符合 canonical 模型
- 校验 `analysis/synthesis/` 下是否错误出现二级分类目录
- 校验每个 `primitive` topic 目录里必须有 `artifact.md`
- 校验每个 `decision` topic 目录里必须有 `artifact.md` 和 `verdict.md`
- 校验 registry 文件存在且格式正确
- 校验不存在未注册 `domain_id`
- 校验不存在空 topic 目录

建议用法：

```bash
python scripts/general/validate_knowledge_tree.py
```

#### 3. 新增 `scripts/research/check_artifact_contract.py`

职责：

- 按 `object_type + research_depth` 校验最小章节集合
- 检查 `primitive` 的 `deep / focused / light` 是否满足对应最低结构
- 检查 `synthesis` 是否包含依赖对象说明
- 检查 `decision` 是否同时存在 artifact 与 verdict 的契约关系

典型校验项：

- `primitive/deep` 缺少“设计取舍”时报错
- `primitive/focused` 缺少“研究范围”或“未覆盖范围”时报错
- `synthesis` 缺少“依赖对象”时报错
- `decision` 缺少“判断维度”或 `verdict.md` 缺少“结论范围”时报错

建议用法：

```bash
python scripts/research/check_artifact_contract.py knowledge/
```

#### 4. 调整 `scripts/publish/move_change_outputs.py`

职责调整：

- apply 时按新目录模型落位
- 从 change packet 提炼 durable 内容
- 自动生成规范化 frontmatter
- 在写入前调用：
  - `check_frontmatter.py`
  - `validate_knowledge_tree.py`
  - `check_artifact_contract.py`

### 校验失败级别

建议分三类：

| 级别 | 含义 | 处理方式 |
|------|------|----------|
| error | 破坏 canonical 结构或元数据 | 阻止 apply |
| warning | 内容不完整但不影响读写 | 提示修复 |
| info | 可优化项 | 输出建议 |

---

## 采用顺序

建议按以下顺序推进：

1. 先定本说明文档
2. 再创建 registry 文件
3. 再升级 frontmatter 校验
4. 再加目录树校验
5. 最后再把 apply 脚本切到新模型

这样可以先统一规则，再动数据和发布路径。
