#!/usr/bin/env python3
"""work_product — 检查 staging work-product 的结构。

触发方式：post_write
输入：work-products/*.md 文件路径
输出：校验通过返回 0，失败返回非 0 并写入 validation/work_product.md
"""

import os
import sys


def main():
    if len(sys.argv) < 2:
        print("SKIP: no file specified")
        sys.exit(0)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"FAIL: work-product not found at {filepath}")
        sys.exit(1)

    with open(filepath, "r") as fh:
        content = fh.read()

    # TODO: 检查 work-product 的最小结构（标题、正文、来源引用）
    if len(content.strip()) < 10:
        change_dir = find_change_dir(filepath)
        validation_dir = os.path.join(change_dir, "validation")
        os.makedirs(validation_dir, exist_ok=True)
        with open(os.path.join(validation_dir, "work_product.md"), "w") as fh:
            fh.write(f"# work_product 校验失败 ({os.path.basename(filepath)})\n\ncontent is empty or too short.\n")
        print(f"FAIL: {os.path.basename(filepath)} content is empty or too short")
        sys.exit(1)

    print(f"PASS: {os.path.basename(filepath)} has content")
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
