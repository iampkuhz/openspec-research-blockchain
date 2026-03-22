---
name: request-brief
description: 用于为本仓库的 change packet 生成和修订 request.md 与 brief.md，适合新开一个 domain、primitive、synthesis、decision 研究时使用。
---

# 研究请求与研究简报

## 何时使用

- 新开一个 `openspec/changes/<change-name>/`
- 需要先把问题、范围、非目标、研究路径、research budget、依赖对象定清楚

## 目标

- 先收紧问题
- 再定义交付边界
- 不提前下结论

## 输出要求

- `request.md`
- `brief.md`

## 强约束

- 中文优先
- 英文术语优先保留
- 明确相关 domains，但不要把 domain 当成路径父级
- `request.md` 只定义问题，不给结论
- `brief.md` 只定义计划，不复写分析正文
