---
name: build-request
description: 用于生成或完善 research change 的 request.md；适合研究意图已萌芽、需要明确研究目标与范围边界时使用。
---

# 生成研究请求

## 规则来源

本 skill 执行 request 阶段规则，正式规则来自：

- `openspec/schemas/blockchain-research/schema.yaml` —— change 整体结构
- `openspec/schemas/blockchain-research/templates/request.md` —— request 模板
- `openspec/specs/request-generation/spec.md` —— request 阶段规范（入口）
- 相关上位规范（见 `request-generation/spec.md` 中"与上位规范的关系"）

本 skill 不复制上位规范正文，仅负责 Qoder 的触发入口、使用时机与输入输出。

若 `request-generation/spec.md` 与其引用的上位规范存在差异，以相关上位规范为准。

## 何时使用（Qoder 特定）

- 研究意图已萌芽，需要明确研究目标与范围边界
- change 目录已创建，需要生成 `request.md` 作为研究起点
- 已有初步研究想法，需要系统化整理为正式请求

## 输入输出（Qoder 特定）

**输入：**
- 目标 change 目录路径
- 用户提供的研究背景、触发原因、初步想法

**输出：**
- `request.md`（写入目标 change 目录下）

## 上下文不足时的补问规则

如用户未提供足够上下文，需要先补齐以下信息：

1. **研究对象类型**：primitive / synthesis / domain / decision
2. **研究路径**：deep-dive / evolution / scenario / domain overview
3. **核心问题**：3-5 个开放性问题
4. **触发原因**：为什么现在要研究这个
5. **范围边界**：覆盖对象、协议、时间窗口、非目标
6. **已知输入**：手上已有的资料、已有研究成果
