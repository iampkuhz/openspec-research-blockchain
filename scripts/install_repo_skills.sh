#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
skills_src="${repo_root}/skills"
codex_home="${CODEX_HOME:-$HOME/.codex}"
skills_dst="${codex_home}/skills"

mkdir -p "${skills_dst}"

for skill_dir in "${skills_src}"/*; do
  [ -d "${skill_dir}" ] || continue
  skill_name="$(basename "${skill_dir}")"
  ln -sfn "${skill_dir}" "${skills_dst}/${skill_name}"
done

echo "已安装仓库内置 skills 到: ${skills_dst}"
