# Source Workflow

**用途**：来源收集、链接验证、证据映射与 evidence gap 盘点的阶段 workflow。

本文件服务于 research pipeline 中的 source capsule。它不同于 `source-reading-workflow.md`：后者是 `task_type=source_reading` 的完整研究类型；本文件是所有研究类型都可能调用的来源阶段执行手册。

---

## 输入

- `request.md`
- `plan.md`
- `openspec/specs/evidence-policy/spec.md`
- `harness/rules/research/source-quality-rules.md`
- `harness/rules/research/uncertainty-rules.md`
- `harness/rules/general/traceability-policy.md`

---

## 输出

必需输出：

- `sources/source-pack.md`
- `sources/evidence-map.md`

按需输出：

- `notes/<source-slug>.md`
- `claims/<claim-slug>.md`

默认不生成 `sources/source-review.md`。来源审查摘要、证据缺口、冲突与未决歧义应写入 `sources/source-pack.md` 或 `sources/evidence-map.md` 的对应章节。只有当既有 change 或 plan 明确要求兼容旧格式时，才可补充 `sources/source-review.md` 作为 supporting file。

---

## 执行步骤

1. **读取来源规划**
   - 从 `plan.md` 提取 source tiers、关键问题、已知输入和 evidence gap。
   - 对二次研究，既有 artifact 只能作为 baseline，不得替代回源验证。

2. **建立 source pack**
   - 每个 source 记录 `source_id`、标题、URL 或本地路径、tier、验证状态、访问时间和备注。
   - 高确定性技术主张优先寻找 L1 / L2 来源。

3. **验证可访问性**
   - 记录 HTTP 状态、工具错误、认证限制、Cloudflare / anti-bot 阻塞、404 或内容不匹配。
   - 链接不可访问时必须记录失败原因和替代来源尝试。

4. **生成 evidence map**
   - 映射 source → claim / note / draft section。
   - 显式记录 coverage、conflicts、evidence gaps、unresolved ambiguities。

5. **按需生成 notes / claims**
   - 值得独立消化、复用或审查的 source 生成 `notes/*.md`。
   - 对 draft 有支撑价值的关键可验证主张生成 `claims/*.md`。

6. **返回 handoff**
   - 返回 sources 目录路径、完成状态和 blocker。
   - 不继续写 `plan.md`、`draft.md`、`review.md` 或 `knowledge/**`。

---

## 禁止事项

- 不要给出最终研究 verdict。
- 不要将低强度来源包装成高确定性证据。
- 不要平滑处理冲突或缺口。
- 不要为了补齐结论而扩写研究范围。
- 不要调用其他 subagent。
