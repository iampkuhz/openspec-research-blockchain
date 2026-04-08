# spec-plan

为当前仓库中的一个 research change 生成或改写 `plan.md`。

**用法：**
- `/spec-plan`
- `/spec-plan openspec/changes/<change-name>/`
- `/spec-plan /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令执行 plan 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/schemas/blockchain-research/templates/plan.md`
- `openspec/specs/plan-generation/spec.md`
- `harness/agents/research-author-agent.md`
- `harness/agents/source-evidence-agent.md`

## 执行步骤（Claude Code 特定）

1. **确认目标 change 目录**
   - 如果用户提供了路径，就使用该路径
   - 否则优先尝试从当前工作目录推断
   - 如仍无法唯一判断，再简短询问用户

2. **读取前置文件**
   - `request.md`
   - `sources/source-review.md`（如已存在）
   - 现有 `plan.md`（如已存在）

3. **选择 active roles**
   - `research-author-agent`：负责 `plan.md`
   - `source-evidence-agent`：如来源规划明显缺口，先补 `sources/`

4. **生成或更新 `plan.md`**
   - 基于已有内容增量修订，而不是无差别重写
   - 不提前写分析正文
   - 显式写清研究深度、来源规划、图表范围、证据缺口、完成标准

5. **完成总结**
   - 使用的 change 路径
   - 更新了哪些 section
   - 是否还需要补 `sources/`
   - 建议用户重点 review 哪些部分
