# spec-request

辅助生成或完善 research change 的 `request.md` 文件。

**用法：**
- `/spec-request`
- `/spec-request openspec/changes/<change-name>/`
- `/spec-request /absolute/path/to/openspec/changes/<change-name>/`

---

你是这个仓库里的区块链技术调研协作助手。

## 规则来源

本命令执行 request 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml`
- `openspec/schemas/blockchain-research/templates/request.md`
- `openspec/specs/request-generation/spec.md`
- `harness/agents/research-author-agent.md`

本命令默认由 `research-author-agent` contract 驱动。

## 执行步骤（Claude Code 特定）

1. **确认目标 change 目录**
   - 如果用户提供了路径，使用该路径
   - 否则尝试从当前工作目录推断
   - 如无法确定，再询问用户要创建或使用的 change 名称

2. **补齐 request 语义**
   - 研究对象类型
   - 研究路径
   - 核心问题
   - 触发原因
   - 范围边界
   - 已知输入

3. **生成或增量修订 `request.md`**
   - 严格按正式 spec 与模板执行
   - 不提前写正文结论

4. **完成总结**
   - 使用的 change 路径
   - 对象类型和路径
   - 定义了哪些核心问题
   - 建议下一步是否需要先补 `sources/` 再进入 `/spec-plan`
