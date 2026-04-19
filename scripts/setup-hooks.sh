#!/usr/bin/env bash
# 设置 git hooks：将 .githooks/ 下的 hook 文件 symlink 到 .git/hooks/
#
# 用法:
#   bash scripts/setup-hooks.sh
#
# 必须在仓库根目录运行，或作为 post-clone 脚本运行。

set -e

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
GITHOOKS="$REPO_ROOT/.githooks"
GIT_HOOKS="$REPO_ROOT/.git/hooks"

if [ ! -d "$GITHOOKS" ]; then
    echo "Error: .githooks/ directory not found at $GITHOOKS"
    exit 1
fi

if [ ! -d "$GIT_HOOKS" ]; then
    echo "Error: .git/hooks/ not found. Is $REPO_ROOT a git repository?"
    exit 1
fi

# 对 .githooks/ 下每个可执行文件，创建 symlink 到 .git/hooks/
for hook in "$GITHOOKS"/*; do
    hook_name=$(basename "$hook")
    target="$GIT_HOOKS/$hook_name"

    # 如果已有 symlink 且指向正确，跳过
    if [ -L "$target" ] && [ "$(readlink "$target")" = "$hook" ]; then
        echo "  $hook_name: already linked"
        continue
    fi

    # 如果已存在同名 hook（非 symlink），备份
    if [ -e "$target" ]; then
        backup="$target.bak.$(date +%s)"
        echo "  $hook_name: backing up existing hook to $backup"
        mv "$target" "$backup"
    fi

    ln -sf "$hook" "$target"
    chmod +x "$target"
    echo "  $hook_name: linked -> $hook"
done

echo "Git hooks setup complete."
