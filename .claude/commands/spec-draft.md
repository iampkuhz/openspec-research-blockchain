# spec-draft

为当前仓库中的一个 research change 生成或改写 `draft.md`。

**用法：**
- `/spec-draft`
- `/spec-draft openspec/changes/<change-name>/`
- `/spec-draft /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令执行 draft 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/schemas/blockchain-research/templates/draft.md`
- `openspec/specs/draft-generation/spec.md`
- `openspec/specs/diagram-policy/spec.md`
- `harness/agents/research-author-agent.md`
- `harness/agents/diagram-agent.md`

## 执行步骤（Claude Code 特定）

1. **确认目标 change 目录**
   - 路径解析规则与 `/spec-plan` 相同

2. **读取前置文件**
   - `request.md`
   - `plan.md`
   - `sources/`
   - 现有 `draft.md`（如有）
   - 现有 `diagrams/` 目录（如有）

3. **选择 active roles**
   - `research-author-agent`：负责正文与 bounded conclusions
   - `diagram-agent`：primitive / mechanism-heavy / 明确需要图表时启用

4. **先执行图表决策树**
   - 实体分类
   - 四个判定问题
   - 图表清单表
   - 覆盖缺口检查

5. **生成或更新 `draft.md`**
   - 先写术语表，再写分析正文
   - 必须区分 live / planned / promotional
   - 不确定性必须显式写出

6. **diagram contract 校验**
   - PlantUML 只能通过用户级 skill 生成
   - 写完 `draft.md` 后必须执行 diagram contract 校验脚本

7. **完成总结**
   - 使用的 change 路径
   - 更新了哪些 section
   - 是否启用了 `diagram-agent`
   - diagram contract 校验结果
