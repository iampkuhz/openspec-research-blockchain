#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
skills_src="${repo_root}/skills"
codex_home="${CODEX_HOME:-$HOME/.codex}"
skills_dst="${codex_home}/skills"
qoder_user_skills_dst="${HOME}/.qoder/skills"
qoder_project_skills_dst="${repo_root}/.qoder/skills"

mkdir -p "${skills_dst}"
mkdir -p "${qoder_user_skills_dst}"
mkdir -p "${qoder_project_skills_dst}"

for skill_dir in "${skills_src}"/*; do
  [ -d "${skill_dir}" ] || continue
  skill_name="$(basename "${skill_dir}")"
  ln -sfn "${skill_dir}" "${skills_dst}/${skill_name}"
  ln -sfn "${skill_dir}" "${qoder_user_skills_dst}/${skill_name}"
  ln -sfn "${skill_dir}" "${qoder_project_skills_dst}/${skill_name}"
done

echo "已安装仓库内置 skills 到:"
echo "- Codex: ${skills_dst}"
echo "- Qoder user: ${qoder_user_skills_dst}"
echo "- Qoder project: ${qoder_project_skills_dst}"
