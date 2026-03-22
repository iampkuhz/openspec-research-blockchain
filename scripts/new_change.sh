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
write_file "${change_dir}/request.md" $'# 研究请求\n\n## 研究对象\n\n- 对象类型：\n- 研究对象：\n\n## 当前要回答的问题\n\n- \n\n## 为什么现在要研究\n\n- \n\n## 范围\n\n- \n\n## 非目标\n\n- \n\n## 已知输入\n\n- \n\n## 预期输出\n\n- \n'
write_file "${change_dir}/plan.md" $'# 研究计划\n\n## 基本信息\n\n- 对象类型：\n- 研究路径：\n- 当前状态：draft\n\n## 当前问题拆解\n\n- \n\n## 后续确认问题\n\n- \n\n## 交付边界\n\n- \n\n## 研究预算\n\n- 当前预算：\n\n## 来源规划\n\n### L1 来源\n\n| 来源 | 类型 | 状态 | 为什么重要 | 备注 |\n| --- | --- | --- | --- | --- |\n|  | spec / EIP / whitepaper | pending |  |  |\n\n### L2 来源\n\n| 来源 | 类型 | 状态 | 为什么重要 | 备注 |\n| --- | --- | --- | --- | --- |\n|  | docs / repo / SDK / API | pending |  |  |\n\n## 证据缺口\n\n- \n\n## 未决歧义\n\n- \n\n## 完成标准\n\n- \n\n## 暂不处理\n\n- \n'
write_file "${change_dir}/draft.md" $'# 研究草稿\n\n## 关键术语\n\n- 术语：\n  - 一句话定义：\n  - 在本题中的作用：\n\n## 分析入口\n\n## 机制拆解\n\n## 设计原因\n\n## 边界与前提\n\n## 与相邻对象的关系\n\n## 当前可确认结论\n\n## 当前不能确认的部分\n\n## 后续补证\n'

if [ "$change_type" = "domain" ] || [ "$change_type" = "synthesis" ] || [ "$change_type" = "decision" ]; then
  write_file "${change_dir}/dependencies.md" $'# 依赖关系\n\n| 依赖对象 | 层级 | 预算 | 强度 | 抽取内容 | 为什么这个深度足够 | 不重复什么 |\n| --- | --- | --- | --- | --- | --- | --- |\n|  |  |  |  |  |  |  |\n'
fi

if [ "$change_type" = "synthesis" ] || [ "$change_type" = "decision" ]; then
  write_file "${change_dir}/evidence-matrix.md" $'# 证据矩阵\n\n| 主张 | 证据等级 | 置信度 | 缺口 |\n| --- | --- | --- | --- |\n|  |  |  |  |\n'
fi

if [ "$change_type" = "decision" ]; then
  write_file "${change_dir}/decision-criteria.md" $'# 决策标准\n\n## 场景定义\n\n## 硬条件\n\n| 标准 | 为什么是硬条件 | 如何验证 | 当前状态 |\n| --- | --- | --- | --- |\n|  |  |  | unknown |\n'
fi

echo "已创建研究改动包: ${change_dir}"
