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
- `harness/workflows/merge-workflow.md`

本命令由 @publish-agent contract 驱动。

7. **完成总结**
   - 使用的 change 路径
   - 写入了哪些长期文件
   - 是否执行了 impact scan
   - 建议用户重点 review 哪些部分
   - 冰箱清单（如有）
