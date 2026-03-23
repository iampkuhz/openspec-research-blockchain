#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "用法: ./scripts/new_change.sh <domain|primitive|synthesis|decision> <change-name>" >&2
  exit 1
fi

change_type="$1"
change_name="$2"
change_dir="openspec/changes/${change_name}"
npx_cache_dir="${TMPDIR:-/tmp}/openspec-npm-cache"

case "$change_type" in
  domain|primitive|synthesis|decision) ;;
  *)
    echo "不支持的 change 类型: ${change_type}" >&2
    exit 1
    ;;
esac

create_change_with_openspec() {
  if [ -d "$change_dir" ]; then
    return 0
  fi

  if command -v openspec >/dev/null 2>&1; then
    openspec new change "$change_name" --schema blockchain-research >/dev/null 2>&1 || true
  fi

  if [ ! -d "$change_dir" ] && command -v npx >/dev/null 2>&1; then
    mkdir -p "$npx_cache_dir"
    npm_config_cache="$npx_cache_dir" npx @fission-ai/openspec@1.2.0 new change "$change_name" --schema blockchain-research >/dev/null 2>&1 || true
  fi

  mkdir -p "$change_dir"
}

create_change_with_openspec

write_file() {
  local file_path="$1"
  local content="$2"
  if [ ! -f "$file_path" ]; then
    printf "%s\n" "$content" > "$file_path"
  fi
}

write_file "${change_dir}/.openspec.yaml" $'schema: blockchain-research\ncreated: 2026-03-22'
write_file "${change_dir}/request.md" $'## 研究对象\n\n- 对象类型：\n- 研究路径：deep-dive / evolution / scenario / domain overview\n- 相关 domains：\n\n## 当前要回答的问题\n\n1. \n2. \n3. \n\n## 为什么现在要研究\n\n\n\n## 范围\n\n### 覆盖对象\n\n\n\n### 覆盖链/协议\n\n\n\n### 时间窗口\n\n\n\n## 非目标\n\n- \n\n## 已知输入\n\n- \n\n## 预期输出\n\n- \n'
write_file "${change_dir}/plan.md" $'## 研究对象\n\n- 对象类型：\n- 研究路径：\n- 相关 domains：\n\n## 问题拆解\n\n\n\n## 待确认问题\n\n\n\n## 交付范围\n\n\n\n## 研究深度\n\n\n\n## 来源规划\n\n### L1 来源（规范层）\n\n| 来源 | 类型 | 说明 |\n|------|------|------|\n|  | spec / EIP |  |\n\n### L2 来源（实现层）\n\n| 来源 | 类型 | 说明 |\n|------|------|------|\n|  | repo / docs |  |\n\n### L3 来源（生态层）\n\n| 来源 | 类型 | 说明 |\n|------|------|------|\n|  | blog / release |  |\n\n### L4 来源（解读层）\n\n| 来源 | 类型 | 说明 |\n|------|------|------|\n|  | analysis |  |\n\n## 证据缺口\n\n\n\n## 完成标准\n\n- [ ] draft.md 包含【参考资料】章节，每条来源均附可点击链接\n- [ ] 所有链接已通过工具验证存活，或明确标注 [未验证] 并说明原因\n\n## 排除范围\n\n\n'
write_file "${change_dir}/draft.md" $'<!-- 目录 -->\n- [概述](#概述)\n- [关键术语](#关键术语)\n- [分析正文](#分析正文)\n- [设计取舍](#设计取舍)\n- [边界与前提](#边界与前提)\n- [相关对象关系](#相关对象关系)\n- [结论](#结论)\n- [待确认问题](#待确认问题)\n- [参考资料](#参考资料)\n\n## 概述\n\n\n\n## 关键术语\n\n| 术语 | 定义 | 在本题中的作用 |\n|------|------|---------------|\n|  |  |  |\n\n## 分析正文\n\n\n\n## 设计取舍\n\n\n\n## 边界与前提\n\n\n\n## 相关对象关系\n\n\n\n## 结论\n\n\n\n## 待确认问题\n\n\n\n## 参考资料\n\n| 来源 | 说明 |\n|------|------|\n|  |  |\n'


if [ "$change_type" = "decision" ]; then
  write_file "${change_dir}/decision-criteria.md" $'# 决策标准\n\n## 场景定义\n\n## 硬条件\n\n| 标准 | 为什么是硬条件 | 如何验证 | 当前状态 |\n| --- | --- | --- | --- |\n|  |  |  | unknown |\n'
fi

echo "已创建研究改动包: ${change_dir}"
