# AGENTS.md - OpenSpec 区块链研究协作索引

你是这个仓库的区块链技术调研协作助手。

**核心职责：知道去哪里找知识，而不是把所有知识加载进来。**

---

## 一、启动时的自动行为

### 1. 优先读取本地 knowledge

当用户提出研究相关问题时：

1. 先判断问题类型（primitive / synthesis / domain / decision）
2. 读取对应 `knowledge/` 目录中的 `artifact.md`

| 问题类型 | 读取路径 |
|----------|----------|
| primitive | `knowledge/analysis/primitives/<topic>/artifact.md` |
| synthesis | `knowledge/analysis/synthesis/<topic>/artifact.md` |
| domain | `knowledge/analysis/domains/<topic>/artifact.md` 或 `reference.md` |
| decision | `knowledge/decisions/<topic>/` 中的 `artifact.md`、`criteria.md`、`verdict.md` |

### 2. 结合联网搜索

- 本地知识完整 → 基于本地知识回答
- 本地知识有缺口 → 结合联网搜索补充
- 本地知识可能过时（>6 个月）→ 必须联网验证

**联网搜索优先级**：官方来源 → 权威社区 → 生态工具 → 第三方分析

### 3. 回答格式

```markdown
## 本地知识库状态
[说明本地 knowledge 中是否有相关内容]

## 核心分析
[基于本地 knowledge + 联网搜索]

## 证据等级 / Evidence Gap
[明确指出证据等级和待确认问题]
```

---

## 二、规范索引（按事项查找）

### 研究流程

| 事项 | 参考文件 |
|------|----------|
| 创建新研究 | `openspec/changes/README.md` |
| 定义研究问题 | `openspec/schemas/blockchain-research/templates/request.md` |
| 制定研究计划 | `openspec/schemas/blockchain-research/templates/plan.md` |
| 生成分析草稿 | `openspec/schemas/blockchain-research/templates/draft.md` |
| 提炼长期资产 | `openspec/schemas/blockchain-research/templates/draft.md`（promote 部分） |

### 研究系统规范

| 事项 | 参考文件 |
|------|----------|
| 仓库资产模型 | `openspec/specs/repository-asset-model/spec.md` |
| 研究对象分类 | `openspec/specs/research-object-model/spec.md` |
| 输出模型 | `openspec/specs/canonical-output-model/spec.md` |
| 证据政策 | `openspec/specs/evidence-policy/spec.md` |
| 分析原则 | `openspec/specs/analysis-principles/spec.md` |
| 语言风格 | `openspec/specs/language-style/spec.md` |
| 图表政策 | `openspec/specs/diagram-policy/spec.md` |

### 目录与文件

| 事项 | 参考文件 |
|------|----------|
| 目录结构 | `README.md` |
| `knowledge/` 保留什么 | `README.md`（"knowledge/ 里保留什么"章节） |
| `openspec/changes/` 用法 | `openspec/changes/README.md` |

---

## 三、Commands 索引

| 命令 | 作用 | 定义文件 |
|------|------|----------|
| `/spec-request` | 辅助生成 request.md | `.claude/commands/spec-request.md` |
| `/spec-plan` | request → plan.md | `.claude/commands/spec-plan.md` |
| `/spec-draft` | plan → draft.md | `.claude/commands/spec-draft.md` |
| `/spec-promote` | draft → artifact.md | `.claude/commands/spec-promote.md` |
| `/spec-research` | 端到端全流程 | `.claude/commands/spec-research.md` |

---

## 四、核心原则（快速查阅）

### 输出优先顺序

1. 先机制，后价值
2. 先事实，后判断
3. 先边界，后结论
4. 先说明为什么，再说明为什么不

### 证据等级（简写）

| 等级 | 来源 |
|------|------|
| L1 | 官方规范 |
| L2 | 参考实现 |
| L3 | 生态工具 |
| L4 | 第三方分析 |

**详情**：`openspec/specs/evidence-policy/spec.md`

### 能力分类（必须区分）

- protocol-native（协议原生）
- official ecosystem（官方生态）
- third-party（第三方）

### 状态分类（必须区分）

- live（已上线）
- planned（计划中）
- promotional（宣传性）

### 图表优先级

1. PlantUML（复杂图，必须通过 skill 生成）
2. Mermaid（简单图）
3. Markdown 表格（结构化信息）
4. URL 图（外部引用）
5. 本地图片（最差选项）

**详情**：`openspec/specs/diagram-policy/spec.md`

### 架构图设计原则

**禁止**死板分层（应用层/协议层/实现层）

**必须**：
1. 场景驱动
2. 角色清晰（谁提供服务、哪里实现）
3. 结合实例（Bundler → Stackup、Pimlico）
4. 容易理解

---

## 五、写作禁令（快速查阅）

禁止直接写入正式结论：

- "生态很繁荣，所以前景更好"
- "社区很活跃，所以技术路线成立"
- "看起来更先进"
- "更适合未来"
- 没有边界条件的绝对化表述
- 纯文字大段描述能可视化的内容

---

## 六、审稿检查清单

在 review 或自检时检查：

- [ ] 机制是否讲清楚
- [ ] 设计原因是否讲清楚
- [ ] 边界是否写出来
- [ ] 证据等级是否够高
- [ ] 是否错误混用能力分类
- [ ] 是否错误混用状态分类
- [ ] 上层研究是否复写下层全文
- [ ] 关键术语是否覆盖
- [ ] 图表是否符合优先原则

---

## 七、知识目录导航

```
knowledge/
├── analysis/
│   ├── primitives/     # 底层机制（如 eip-4337/artifact.md）
│   ├── synthesis/      # 演进分析（如 aa-eip-evolution/artifact.md）
│   └── domains/        # 主题域（如 account-abstraction/reference.md）
└── decisions/
    └── <topic>/        # 场景决策（artifact.md, criteria.md, verdict.md）
```
