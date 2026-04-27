#!/usr/bin/env bash
set -euo pipefail

# 生成 .claude/skills 平铺 symlink 暴露层
# 用法：
#   bash scripts/maintenance/install_repo_skills.sh --dry-run
#   bash scripts/maintenance/install_repo_skills.sh --write

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

skills_src="${REPO_ROOT}/skills"
skills_dst="${REPO_ROOT}/.claude/skills"

MODE="${1:---dry-run}"
if [[ "${MODE}" != "--dry-run" && "${MODE}" != "--write" ]]; then
  echo "用法: $0 [--dry-run|--write]"
  exit 1
fi

# 命名前缀映射
prefix_for() {
  case "$1" in
    openspec-flow) echo "openspec" ;;
    research-authoring) echo "research" ;;
    knowledge-publishing) echo "publish" ;;
    governance) echo "governance" ;;
    diagrams) echo "diagram" ;;
    maintenance) echo "maintenance" ;;
    *) echo "$1" ;;
  esac
}

declare -a errors=()
declare -a actions=()

# 清理旧 .claude/skills 下的 category 子目录（保留 README.md 和 _ 前缀文件）
if [[ -d "${skills_dst}" ]]; then
  for item in "${skills_dst}"/*; do
    [ -e "${item}" ] || continue
    base="$(basename "${item}")"
    [[ "${base}" == "README.md" ]] && continue
    [[ "${base}" == _* ]] && continue
    if [[ "${MODE}" == "--write" ]]; then
      rm -rf "${item}"
      actions+=("removed: ${base}")
    else
      actions+=("[dry-run] would remove: ${base}")
    fi
  done
fi

# 遍历 skills/<category>/<skill>/SKILL.md
repo_count=0
for category_dir in "${skills_src}"/*/; do
  [ -d "${category_dir}" ] || continue
  category="$(basename "${category_dir}")"
  prefix="$(prefix_for "${category}")"

  for skill_dir in "${category_dir}"*/; do
    [ -d "${skill_dir}" ] || continue
    skill="$(basename "${skill_dir}")"
    skill_md="${skill_dir}SKILL.md"

    if [[ ! -f "${skill_md}" ]]; then
      errors+=("missing SKILL.md: ${skill_dir}")
      continue
    fi

    repo_count=$((repo_count + 1))

    # 从 frontmatter 读取 exposed name
    fm_name=$(head -5 "${skill_md}" | grep '^name:' | head -1 | sed 's/^name: *//' | tr -d '"' | tr -d "'" | xargs)
    if [[ -z "${fm_name}" ]]; then
      errors+=("missing frontmatter name: ${skill_dir}")
      continue
    fi
    exposed_name="${fm_name}"
    link_path="${skills_dst}/${exposed_name}"
    # 相对路径从 .claude/skills/ 到 skills/<category>/<skill>
    target="../../skills/${category}/${skill}"

    if [[ "${MODE}" == "--write" ]]; then
      if [[ -L "${link_path}" || -e "${link_path}" ]]; then
        rm -f "${link_path}"
      fi
      ln -s "${target}" "${link_path}"
      actions+=("linked: ${exposed_name} -> ${target}")
    else
      actions+=("[dry-run] would link: ${exposed_name} -> ${target}")
    fi
  done
done

echo "=== install_repo_skills.sh (${MODE}) ==="
echo ""
echo "Actions:"
for a in "${actions[@]}"; do
  echo "  ${a}"
done

echo ""
echo "Repo active skills: ${repo_count}"
echo "Exposed skills: ${#actions[@]}"

if [[ ${#errors[@]} -gt 0 ]]; then
  echo ""
  echo "ERRORS:"
  for e in "${errors[@]}"; do
    echo "  ${e}"
  done
  exit 1
fi

echo ""
echo "OK"
