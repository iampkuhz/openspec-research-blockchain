#!/usr/bin/env python3
"""source_pack — 检查 source metadata 和 source list。

触发方式：post_write
输入：source-pack.md 文件路径
输出：校验通过返回 0，失败返回非 0 并写入 validation/source_pack.md
"""

import os
import sys


def main():
    if len(sys.argv) < 2:
        print("SKIP: no file specified")
        sys.exit(0)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"FAIL: source-pack.md not found at {filepath}")
        sys.exit(1)

    with open(filepath, "r") as fh:
        content = fh.read()

    # TODO: 检查 source list 和 metadata 的最小结构
    if len(content.strip()) < 10:
        change_dir = find_change_dir(filepath)
        validation_dir = os.path.join(change_dir, "validation")
        os.makedirs(validation_dir, exist_ok=True)
        with open(os.path.join(validation_dir, "source_pack.md"), "w") as fh:
            fh.write("# source_pack 校验失败\n\nsource-pack.md 内容为空或不足。\n")
        print("FAIL: source-pack.md content is empty or too short")
        sys.exit(1)

    print("PASS: source-pack.md has content")
    sys.exit(0)


def find_change_dir(filepath):
    d = os.path.dirname(os.path.abspath(filepath))
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "change.yaml")):
            return d
        d = os.path.dirname(d)
    return os.path.dirname(filepath)


if __name__ == "__main__":
    main()
