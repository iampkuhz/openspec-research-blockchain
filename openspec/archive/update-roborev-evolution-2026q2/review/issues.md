# Review Issues: update-roborev-evolution-2026q2

**Reviewed by**: review-critic-agent
**Reviewed at**: 2026-04-21
**Change ID**: update-roborev-evolution-2026q2
**Object type**: primitive
**Research path**: evolution

---

## High Severity Issues

### ISSUE-001: PlantUML 图表缺少 `diagrams/` 目录与 `diagram.puml` 文件

- **Location**: `draft.md` 行 112-193（角色与组件架构图）、行 199-278（核心流程时序图）
- **Problem**: draft.md 中嵌入了两个 PlantUML 代码块，但 `openspec/changes/update-roborev-evolution-2026q2/diagrams/` 目录不存在，缺少对应的 `diagram.puml` 文件。根据 `harness/rules/diagrams/diagram-review-checklist.md` 检查项 1 与检查项 2，PlantUML 图表必须：
  1. 通过全局 skill 生成
  2. 在 `openspec/changes/<change-id>/diagrams/<id>/diagram.puml` 存在对应文件
  3. PlantUML block 前必须有 `<!-- diagram: ... -->` contract comment
- **Impact**: 违反了 PlantUML 图表合同要求，图表无法通过 validation 脚本校验，renderability 无法保证。这是 diagram-review-checklist 中定义的 **Blocker** 级别问题。
- **Recommendation**: 执行 `feipi-plantuml-generate-architecture-diagram` 和 `feipi-plantuml-generate-sequence-diagram` skills 生成正式 `diagram.puml` 文件，或在 review 阶段降级为 ASCII/表格 fallback 格式。同时添加 contract comments。
- **Status**: open

### ISSUE-002: 大量核心主张缺少对应的 excerpt 文件支撑

- **Location**: `draft.md` 全文多处 【L2, GH-RELEASES】、【L2, GH-COMMITS-EARLY】、【L2, GH-INTERNAL-DAEMON】、【L2, GH-INTERNAL-STORAGE】、【L2, GH-PACKAGING-SYSTEMD】、【L2, GH-CMD-REFINE】、【L2, CODER-ACP-SDK】 等标注
- **Problem**: `sources/inbox.yaml` 定义了 12 个 L2 来源，但 `sources/excerpts/` 目录下仅有 4 个 excerpt 文件：
  - `gh-config.md` (GH-CONFIG)
  - `gh-gomod.md` (GH-GOMOD)
  - `gh-internal-agent.md` (GH-INTERNAL-AGENT)
  - `gh-internal-worktree.md` (GH-INTERNAL-WORKTREE)
  
  缺失的 excerpt 包括（但不限于）：
  - GH-RELEASES（演进阶段划分的最直接证据）
  - GH-COMMITS-EARLY（大爆炸式初始架构的证据）
  - GH-INTERNAL-DAEMON（daemon 架构、systemd socket activation、hooks.go 含 beads）
  - GH-INTERNAL-STORAGE（SQLite + PostgreSQL 双后端）
  - GH-PACKAGING-SYSTEMD（systemd unit 文件）
  - GH-CMD-REFINE（refine 终止条件）
  - CODER-ACP-SDK（ACP 是 Coder 外部 SDK）
  - GH-REPO-META（repo 创建日期）
  - GH-README（项目定义）
  - beads 相关来源

  plan.md 完成标准明确要求：`所有 L2 来源（GitHub repo、release notes、关键源码）已通过 MCP 工具实际抓取并写入 sources/excerpts/`
- **Impact**: traceability L1/L2 层级断裂。虽然 draft 中使用 `【L2, source-id】` 标注了来源，但缺少实际 excerpt 内容来验证这些来源是否确实包含所声称的信息。违反了 `harness/rules/general/traceability-policy.md` L1 层级要求（每个关键 claim 必须能回到至少一个具体 source）。
- **Recommendation**: 补充所有 L2 来源的 excerpt 文件到 `sources/excerpts/`，确保每个有 【L2, ...】 标注的核心主张都有对应的 excerpt 内容可查。如果部分来源确实无法抓取，应在 `source-review.md` 中明确标注 `[未验证] 安全策略拦截` 并说明替代方案。
- **Status**: open

### ISSUE-003: plan.md 请求的核心问题 3（边界层）回答不充分

- **Location**: `draft.md` 概述与能力边界章节；对照 `plan.md` 核心问题 3
- **Problem**: plan.md 核心问题 3 明确要求：「边界层：RoboRev 与 PR 级 review 工具（CodeRabbit、Qodo Merge）的边界在哪里？哪些能力是 RoboRev 原生提供的，哪些依赖外部组件？」。draft.md 中：
  - 概述表中有"类比理解"行提到"类似 GitHub PR review 的自动化版本"，但只是类比，不是边界分析
  - "能力边界"章节只有强项/弱项/不确定性，没有与 PR 级 review 工具（CodeRabbit、Qodo Merge）的显式边界对比
  - 哪些能力原生、哪些依赖外部组件，没有系统性的回答
- **Impact**: 未满足 plan.md 定义的交付范围，核心问题未完全回答。作为 primitive 类型的 deep 研究，缺少边界定义会导致 artifact 的定位不完整。
- **Recommendation**: 在 draft.md 中新增"与 PR 级 review 工具的边界"小节，至少回答：
  1. RoboRev 管什么（commit 级、AI agent 产出、本地/CI 触发、内置修复闭环）
  2. 不管什么（PR 级人类 review、SaaS 托管、代码质量评分等）
  3. 原生能力 vs 外部依赖的系统性列表
- **Status**: open

### ISSUE-004: 多处具体技术细节主张无 excerpt 来源

- **Location**: `draft.md` 多个段落
- **Problem**: 以下具体技术主张标注了 L2 来源，但对应来源的 excerpt 文件不存在，无法验证：

  | 主张 | 标注来源 | 缺失 excerpt |
  |------|----------|-------------|
  | v0.40.0 引入 ACP（2026-03-03） | GH-RELEASES | 无 |
  | ACP 引入后 3 天内接入 Kiro/Cursor/Pi | GH-RELEASES | 无 |
  | v0.45.0 fix/refine 闭环 | GH-RELEASES | 无 |
  | v0.48.0 worktree 沙箱（2026-03-18） | GH-RELEASES | 无 |
  | v0.49.0 Unix domain socket（2026-03-24） | GH-RELEASES | 无 |
  | v0.50.0 systemd（2026-04-01） | GH-RELEASES + GH-PACKAGING-SYSTEMD | 无 |
  | v0.51.0 OpenAPI（2026-04-09） | GH-RELEASES | 无 |
  | v0.5.0 首个 release（2026-01-09） | GH-RELEASES + GH-COMMITS-EARLY | 无 |
  | worker pool 默认 4 worker | GH-INTERNAL-DAEMON | 无 |
  | refine.go --max-iterations 默认 10 | GH-CMD-REFINE | 无 |
  | `roborev compact` 功能 | GH-CMD-REFINE 或 GH-README | 无 |
  | `roborev insights` 命令 | GH-RELEASES | 无 |
  | `auto_close_passing_reviews` | GH-RELEASES | 无 |
  | PR comment upsert / review matrix | GH-RELEASES | 无 |
  | Husky git hook manager 支持 | GH-README 或 GH-RELEASES | 无 |
  | PR #3 Copilot CLI / PR #5 OpenCode | GH-COMMITS-EARLY 或 GH-README | 无 |
  | PR #33 JSONL 事件流 | GH-COMMITS-EARLY | 无 |
  | agentsview 集成（v0.47.0） | GH-RELEASES | 无 |
  | `roborev summary` 命令 | GH-README | 无 |

- **Impact**: evidence policy 要求核心技术主张由 L1/L2 来源支撑。当前大量主张只有 source_id 引用而无实际 excerpt 内容，traceability 链条不完整。
- **Recommendation**: 逐条补充缺失来源的 excerpt，或将无法验证的主张降级置信度并标注为 evidence-gap。
- **Status**: open

---

## Medium Severity Issues

### ISSUE-005: 参考资料表格式偏离 plan.md 要求

- **Location**: `draft.md` 行 532-548（参考资料表）
- **Problem**: plan.md 完成标准第 11 项要求参考资料表使用 `[[source-type] description](url)` 格式。当前 draft 使用的是 `[[source-type] description](url)` 的变体（如 `[[github]RoboRev 仓库...](url)`），格式基本正确，但存在以下偏差：
  1. 部分 source-type 使用了复合形式如 `github-raw`，而 plan 中未定义此类型
  2. 缺少 L3 来源（官方博客/Issues/Discussions），plan 中规划的 L3 来源未出现在参考表中
  3. `[[本地 artifact]基线 artifact](knowledge/...)` 条目的 source-type 为"本地 artifact"，不是规范的 source-type
- **Impact**: 格式不完全统一，影响自动化解析和跨 change 的一致性。
- **Recommendation**: 统一 source-type 词表，使用 `github`、`github-raw`、`local` 等规范类型。如需新增类型，应在 plan 或 config 中定义。
- **Status**: open

### ISSUE-006: L3 来源（官方博客/Issues/Discussions）未探索

- **Location**: `plan.md` 来源规划 L3 段；`draft.md` 无 L3 引用
- **Problem**: plan.md 规划了 L3 来源（RoboRev 官方博客/文档、GitHub Issues/Discussions），验证状态为 `[未验证] 需搜索确认是否存在`。但 draft 全文没有任何 L3 引用，也没有在 `source-review.md` 中说明 L3 来源是否存在或为何不使用。
- **Impact**: 来源规划与实际执行之间存在 gap。虽然对 primitive 类型研究 L2 来源是主体，但 L3 来源的探索状态应该显式记录。
- **Recommendation**: 在 `source-review.md` 中增加 L3 来源探索结论：是否存在官方博客？GitHub Issues/Discussions 是否有相关内容？如果不存在或无价值，显式说明原因。
- **Status**: open

### ISSUE-007: 演进路线图时间线与版本日期缺乏来源验证

- **Location**: `draft.md` 行 284-314（演进路线图）
- **Problem**: 演进路线图包含大量精确日期（如 v0.40.0 对应 2026-03-03、v0.48.0 对应 2026-03-18、v0.49.0 对应 2026-03-24、v0.50.0 对应 2026-04-01、v0.51.0 对应 2026-04-09）。这些日期的直接证据来源是 GH-RELEASES，但 GH-RELEASES 的 excerpt 文件不存在，无法验证这些日期的准确性。
- **Impact**: 如果路线图上的日期有误，会直接影响三阶段划分的时间边界准确性。
- **Recommendation**: 补充 GH-RELEASES 的 excerpt 文件或至少提供各 release 的发布日期验证。
- **Status**: open

### ISSUE-008: 状态转换表中的 `auto_close_passing_reviews` 行为描述不精确

- **Location**: `draft.md` 行 447
- **Problem**: 状态转换表中 `completed` (Pass) 状态在 `auto_close_passing_reviews` enabled 时的转换结果标注为"PR 自动关闭"，但这是 Job 状态转换表，"PR 自动关闭"不是 Job 状态转换，而是外部系统行为。从状态机角度，Job 在 `completed` (Pass) 后应保持在 `completed` 状态，PR 关闭是副作用而非状态转换。
- **Impact**: 概念上不够精确，可能误导读者认为 Job 状态会因 PR 关闭而进一步变化。
- **Recommendation**: 将该行从状态转换表移至"能力边界"或"设计取舍"章节，或修改为"Job 保持在 completed 状态，同时触发 PR 自动关闭（副作用）"。
- **Status**: open

### ISSUE-009: source-review.md 的"待确认问题"表与 draft.md 不一致

- **Location**: `sources/source-review.md` 行 44-51 vs `draft.md` 行 518-530
- **Problem**: `source-review.md` 的待确认问题表只列出了 6 个已解决的问题（ACP、beads、沙箱、refine、CLI agent、PostgreSQL 支持），缺少 draft.md 中标注为"未解决"的 3 个问题：
  1. PostgreSQL 引入版本（未解决）
  2. ACP 完整协议规范（未解决）
  3. 早期私有开发（未解决）
  
  `source-review.md` 的"证据缺口"部分提到了这 3 个缺口，但未统一汇总到"待确认问题"表中。
- **Impact**: source-review.md 与 draft.md 之间的证据缺口状态不统一，影响 traceability L3 层级（artifact 核心结论可回指到来源集合）。
- **Recommendation**: 在 `source-review.md` 的"待确认问题"表中补充 3 个未解决问题，保持与 draft.md 一致。
- **Status**: open

### ISSUE-010: "大爆炸式初始架构"推断的证据支撑偏弱

- **Location**: `draft.md` 行 322（"初始架构可能在私有开发中完成，开源时一次性发布"）
- **Problem**: 该主张标注为 `【L2, GH-REPO-META + GH-COMMITS-EARLY】`，但实际证据只能证明"首次公开 commits 集中在 2026-01-09"。从"首次公开 commits 集中在一天"推断"初始架构可能在私有开发中完成"是一个推测性结论，应标注为不确定性而非确定性事实。`source-review.md` 中也将其列为证据缺口。
- **Impact**: 推断性结论被当作确定性事实表述，违反了 evidence policy 中"必须区分已上线能力、规划中能力、宣传性表述"的要求。
- **Recommendation**: 将该段表述修改为显式不确定性措辞，如"repo 创建于 2026-01-05，首次公开 commits 集中在 2026-01-09，其间开发活动无法确认（证据缺口）。"
- **Status**: open

---

## Low Severity Issues

### ISSUE-011: 术语"Kilo"与"Kiro"混用

- **Location**: `draft.md` 行 332（"Kilo（v0.38.0）"）vs 行 353（"kiro.go"）
- **Problem**: 阶段一描述中使用"Kilo"，agent 文件列表中使用"kiro.go"。从 go.mod 和 agent 目录来看，正确名称应为 "Kiro"（对应 `kiro.go`）。"Kilo"可能是笔误。
- **Impact**: 术语不一致，但不影响核心技术主张。
- **Recommendation**: 统一为 "Kiro"。
- **Status**: open

### ISSUE-012: 演进路线图 ASCII 格式与 plan 要求不完全匹配

- **Location**: `draft.md` 行 284-314
- **Problem**: plan.md 图表清单要求演进路线图采用 "ASCII Timeline" 格式，当前 draft 使用 ASCII 格式，符合要求。但图表清单中还提到需通过 skills 校验，而 ASCII 图不涉及 skill 生成。此处表述可更清晰。
- **Impact**: 轻微格式说明问题，不影响内容质量。
- **Recommendation**: 无需修改，保持 ASCII Timeline 即可。建议在图表决策清单中明确 ASCII timeline 不需要 diagram skill。
- **Status**: open

### ISSUE-013: 设计取舍表与能力边界表内容部分重复

- **Location**: `draft.md` 设计取舍表（行 451-462）与能力边界强项表（行 468-478）
- **Problem**: "Agent 接入方式"、"沙箱方案"、"Daemon 管理"、"API 标准化"、"触发机制"、"ACP 协议来源"等取舍项与能力边界强项表存在内容重叠。虽然两个表的视角不同（"取舍"侧重决策理由，"强项"侧重已确认能力），但读者可能产生重复感。
- **Impact**: 轻微的结构性冗余，不影响准确性。
- **Recommendation**: 保持现状即可，两个表的定位确实不同。如有空间可考虑精简。
- **Status**: open

### ISSUE-014: evidence_level 标注格式不统一

- **Location**: `draft.md` 全文
- **Problem**: draft 中存在两种证据等级标注格式：
  1. 段落末尾的内联标注：`【L2, GH-README】`
  2. 设计取舍/能力边界表中的单独列：`L2 (源码)`、`L2 (release notes + README)` 等
  
  两种格式中的证据描述部分不一致（source_id vs 描述性文字）。
- **Impact**: 格式不统一，影响自动化 traceability 验证。
- **Recommendation**: 统一使用 `【L2, source-id】` 内联格式，表格中可直接引用 source_id 而非描述性文字。
- **Status**: open

---

## Severity 分布

| 严重性 | 数量 | 问题 ID |
|--------|------|---------|
| High | 4 | ISSUE-001, ISSUE-002, ISSUE-003, ISSUE-004 |
| Medium | 6 | ISSUE-005, ISSUE-006, ISSUE-007, ISSUE-008, ISSUE-009, ISSUE-010 |
| Low | 4 | ISSUE-011, ISSUE-012, ISSUE-013, ISSUE-014 |

---

## Traceability 审计结果

### Claim → Source 映射完整性

| 检查项 | 结果 |
|--------|------|
| draft.md 中所有 【L2, ...】标注的 source_id 是否在 inbox.yaml 中注册？ | 大部分是。部分标注如 `GH-INTERNAL-DAEMON`、`GH-CMD-REFINE`、`GH-PACKAGING-SYSTEMD`、`CODER-ACP-SDK`、`GH-REPO-META`、`GH-CONFIG` 在 inbox.yaml 中存在 |
| 每个标注 source_id 是否有对应 excerpt 文件？ | 否。12 个 L2 来源中仅 4 个有 excerpt 文件 |
| 核心结论是否可回指到来源集合？ | 部分可以。source-review.md 中有对基线 artifact 的修正表，但具体段落级回指能力弱 |
| 证据等级标注是否符合 policy？ | 基本符合。L2 标注对应源码/release notes 级别，L4 标注对应本地 artifact |
| 不确定性是否显式记录？ | 是。draft.md 有独立的"不确定性"表和"待确认问题"表 |

### 映射覆盖度

- 有 excerpt 支撑的主张：约 30%（主要集中在 agent 架构、worktree 沙箱、config/beads、go.mod 依赖）
- 无 excerpt 支撑但标注了 source_id 的主张：约 70%（主要集中在版本日期、release notes 特性列表、daemon 细节、refine 命令细节、systemd 细节、OpenAPI 细节）

---

## 总体评审结论

### Verdict: **needs revision**

### 必须修复项（High Severity）

1. **ISSUE-001**: PlantUML 图表缺少 `diagrams/` 目录与 `diagram.puml` 文件，违反 diagram contract。需通过 skill 生成正式文件或降级为 ASCII/表格。
2. **ISSUE-002**: 大量核心主张（约 70% 的 L2 标注主张）缺少对应的 excerpt 文件支撑。需补充 `sources/excerpts/` 中的缺失 excerpt。
3. **ISSUE-003**: plan.md 核心问题 3（与 PR 级 review 工具的边界）未充分回答。需新增边界分析小节。
4. **ISSUE-004**: 具体版本日期、特性列表、命令行为等技术细节无 excerpt 来源验证。需逐条补充来源 excerpt 或降级置信度。

### 建议修复项（Medium Severity）

5. **ISSUE-005**: 参考资料表 source-type 词表需统一。
6. **ISSUE-006**: L3 来源探索状态需显式记录到 source-review.md。
7. **ISSUE-007**: 演进路线图日期需 GH-RELEASES excerpt 验证。
8. **ISSUE-008**: 状态转换表中 `auto_close_passing_reviews` 行为描述需精确化。
9. **ISSUE-009**: source-review.md 与 draft.md 的待确认问题表需对齐。
10. **ISSUE-010**: "大爆炸式初始架构"推断需改为显式不确定性措辞。

### 放行条件

- 所有 4 个 High severity 问题必须修复或降低为 Medium（通过显式标注不确定性）后，方可进入 `approved with minor fixes` 状态。
- Medium severity 问题可在 merge/apply 阶段前修复。
- Low severity 问题为建议性质，不阻塞 publish。
