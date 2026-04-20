# OpenSpec / Harness / Skills 职责边界

**版本**：2.0  
**状态**：Proposed  
**适用范围**：本仓库全部规约、工作流、技能入口、治理与目录调整相关文件

---

## 1. 阅读触发规则

**任务语义优先，路径辅助。**  
只有当任务语义明确涉及以下内容时，才需要读取本文件：

- OpenSpec / Harness / Skills 的职责边界
- schema / specs / templates / config / governance 的修改
- 仓库目录架构调整
- `.claude/commands/`、`.claude/agents/`、skills 目录中与路由、角色合同、阶段编排相关的内容
- `AGENTS.md` 中与仓库导航、治理、分层有关的段落
- 对上述改动的评审

默认**不要**因为文件路径命中而自动加载本文件。  
普通 research、资料收集、图表生成、一般写作、与仓库分层无关的局部 skill 优化，都不应默认读取本文件。

---

## 2. 仓库定位

本仓库是 **blockchain research / knowledge production repo**。  
主产物是 **research knowledge artifacts**，不是业务代码实现仓库。

因此，本仓库里的边界判断应优先围绕：

- 正式研究规则是否成立
- 正式产物如何生成与沉淀
- AI 如何执行、检查与修复
- 技能入口如何最小化承载过程知识

---

## 3. 三层模型

### 3.1 OpenSpec canonical layer

OpenSpec 负责定义 **正式规则本体**。  
判断标准是：**即使没有 agent，这些规则仍然成立。**

OpenSpec 应承载：

1. **artifact contract**
   - 有哪些 artifact
   - artifact 之间的依赖关系
   - 哪些条件满足后才能进入下一阶段
   - 哪些条件满足后才允许 apply / archive / 沉淀

2. **artifact canonical structure**
   - 每个 artifact 的标准模板
   - 必填 section / 可选 section
   - 输出结构与命名约束

3. **canonical policy**
   - evidence policy
   - diagram policy
   - language policy
   - asset model
   - research object model
   - quality standard

4. **project-level formal rules**
   - 项目上下文
   - 按 artifact 注入的正式规则
   - 不允许被执行层重写的约束

### 3.2 Harness execution / governance layer

Harness 负责定义 **执行与治理手册**。  
判断标准是：**这些内容主要服务于 AI / agent 如何把 OpenSpec 规则落地。**

Harness 应承载：

1. **execution workflow**
   - 先读什么
   - 后做什么
   - 何时 review / repair / apply
   - 何时升级为 governance review

2. **derived checks**
   - 如何把 OpenSpec 的正式规则转成执行检查
   - 如何检查 evidence / diagram / language / template 合规性
   - 检查失败后的回修与复检流程

3. **execution governance**
   - traceability 操作流程
   - source collection / validation 配方
   - terminology lifecycle
   - changelog / update 操作约定
   - review checklist / repair checklist

4. **orchestration**
   - 主 agent / 子 agent 职责边界
   - 何时允许调用子 agent
   - 哪些子 agent 只能消费 package，不得扩写需求
   - 失败降级与交接规则

### 3.3 Skill / command adapter layer

Skill / command 负责定义 **动作入口与最小执行适配**。  
判断标准是：**这条说明是否只服务于某一个具体动作。**

Skill / command 应承载：

1. **action scope**
   - 这个入口解决什么问题
   - 输入是什么
   - 输出是什么

2. **action-local procedure**
   - 读取哪些正式输入
   - 调用哪些命令 / 工具 / MCP
   - 输出到什么位置
   - 本动作的失败降级策略

3. **references**
   - 需要引用哪个 OpenSpec contract
   - 需要遵守哪个 Harness governance 文档
   - 不在 skill 内重复定义全局规则

**Skill / command 不是 canonical policy source。**  
**Skill / command 也不是 repo governance source。**

---

## 4. 一句话边界

- **OpenSpec 管“什么算正式、产物长什么样、何时可沉淀”。**
- **Harness 管“AI 怎么干、怎么查、怎么修、怎么协作”。**
- **Skill / command 管“这次动作怎么触发、怎么接线”。**

---

## 5. 文件归属规则

### 5.1 必须放在 OpenSpec 的内容

满足任一项，优先归 OpenSpec：

- 这是正式规则本体
- 这是 artifact 的 canonical 结构
- 这是 schema / template / config / apply / archive / asset placement 的主定义
- 这是即使没有 agent 也仍成立的规则
- 这是 execution layer 只能遵循、不能改写的 policy

典型位置：

- `openspec/specs/**/spec.md`
- `openspec/schemas/**/schema.yaml`
- `openspec/schemas/**/templates/*.md`
- `openspec/config.yaml`

### 5.2 必须放在 Harness 的内容

满足任一项，优先归 Harness：

- 这是 AI / agent 的执行步骤
- 这是基于 OpenSpec 派生出来的检查
- 这是 review / repair / validation / routing / escalation 的操作机制
- 这是多 agent 协作边界
- 这是跨多个 skill 共用的治理规则

典型位置：

- `harness/workflows/*.md`
- `harness/governance/*.md`
- `harness/rules/**/*.md`
- `harness/agents/*.md`
- `harness/checklists/*.md`

### 5.3 只应放在 Skill / command 的内容

满足任一项，可归 skill / command：

- 这是单一动作入口
- 这条说明只服务一个命令 / skill
- 主要是输入 / 输出 / 调用链 / 本动作局部 fallback
- 可以通过引用治理文档避免重复规则

典型位置：

- `.claude/commands/*.md`
- `.claude/agents/*.md`
- `skills/*/SKILL.md` 或等价目录

---

## 6. Skill / command 的特殊约束

### 6.1 可以写什么

- 读取哪些文件
- 调用哪个命令 / 工具
- 输出到什么位置
- 本动作失败时如何降级
- 这个动作依赖哪份 OpenSpec / Harness 文档

### 6.2 不应该写什么

- repo 级长期治理规则
- artifact contract 的主定义
- canonical evidence / diagram / language policy
- 多个 skill 共享的通用路由原则
- 主 / 子 agent 的全局职责边界

### 6.3 写法要求

Skill / command 应尽量 **薄**：

- 只写动作私有逻辑
- 通过链接 / 引用接入全局治理
- 不复制大段仓库宪法
- 不把局部 convenience rule 升格为正式规则

---

## 7. 目录落位建议

建议形成以下分层：

```text
AGENTS.md
docs/
  governance/
    openspec-harness-boundary.md
    repo-routing.md
openspec/
  config.yaml
  specs/
  schemas/
    blockchain-research/
      schema.yaml
      templates/
harness/
  governance/
    agent-boundaries.md
    escalation-policy.md
  workflows/
    build-research-draft.md
    review-research-artifact.md
  rules/
    research/
    writing/
    diagrams/
    traceability/
  checklists/
    research-review-checklist.md
    diagram-review-checklist.md
.claude/
  commands/
  agents/
skills/
  ...