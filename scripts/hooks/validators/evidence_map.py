#!/usr/bin/env python3
"""evidence_map — 检查 source 到 artifact 的 evidence mapping。

触发方式：post_write
输入：evidence-map.md 文件路径
输出：校验通过返回 0，失败返回非 0 并写入 validation/evidence_map.md
"""

import os
import sys


def main():
    if len(sys.argv) < 2:
        print("SKIP: no file specified")
        sys.exit(0)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"FAIL: evidence-map.md not found at {filepath}")
        sys.exit(1)

    with open(filepath, "r") as fh:
        content = fh.read()

    # TODO: 检查 source → claim → artifact 的映射链
    if len(content.strip()) < 10:
        change_dir = find_change_dir(filepath)
        validation_dir = os.path.join(change_dir, "validation")
        os.makedirs(validation_dir, exist_ok=True)
        with open(os.path.join(validation_dir, "evidence_map.md"), "w") as fh:
            fh.write("# evidence_map 校验失败\n\nevidence-map.md 内容为空或不足。\n")
        print("FAIL: evidence-map.md content is empty or too short")
        sys.exit(1)

    print("PASS: evidence-map.md has content")
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
