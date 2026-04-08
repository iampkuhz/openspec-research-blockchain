# spec-artifact

把一个 research change 的稳定 `draft.md` 提炼为长期 artifact。

**用法：**
- `/spec-artifact`
- `/spec-artifact openspec/changes/<change-name>/`
- `/spec-artifact /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令执行 publish / artifact 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/specs/artifact-generation/spec.md`
- `openspec/specs/canonical-output-model/spec.md`
- `harness/agents/publish-agent.md`
- `harness/workflows/merge-workflow.md`

## 执行步骤（Claude Code 特定）

1. **确认目标 change 目录**
   - 路径解析规则与 `/spec-plan` 相同

2. **读取前置文件**
   - `request.md`
   - `plan.md`
   - `draft.md`
   - `review/review-summary.md`

3. **检查 publish gate**
   - review 结论必须允许继续
   - high severity 问题必须已处理

4. **执行 `publish-agent` contract**
   - 判断对象类型与目标路径
   - 提炼 durable 内容写入长期资产
   - update 场景下一并执行 impact scan

5. **完成总结**
   - 使用的 change 路径
   - 写入了哪些长期文件
   - 是否执行了 impact scan
   - 建议用户重点 review 哪些部分
