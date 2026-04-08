#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "用法: ./scripts/openspec/new_change.sh <domain|primitive|synthesis|decision> <change-name>" >&2
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
write_file_from_template() {
  local file_path="$1"
  local template_path="$2"
  if [ ! -f "$file_path" ]; then
    cp "$template_path" "$file_path"
  fi
}

write_file_from_template "${change_dir}/request.md" "openspec/schemas/blockchain-research/templates/request.md"
write_file_from_template "${change_dir}/plan.md" "openspec/schemas/blockchain-research/templates/plan.md"
write_file_from_template "${change_dir}/draft.md" "openspec/schemas/blockchain-research/templates/draft.md"


if [ "$change_type" = "decision" ]; then
  write_file_from_template "${change_dir}/decision-criteria.md" "openspec/schemas/blockchain-research/templates/decision-criteria.md"
fi

echo "已创建研究改动包: ${change_dir}"
