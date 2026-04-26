#!/usr/bin/env python3
"""publish_targets — 检查 publish.md 和 change.yaml 中的 publish_targets。

触发方式：pre_publish
输入：change.yaml 所在目录路径
输出：校验通过返回 0，失败返回非 0 并写入 validation/publish_targets.md
"""

import os
import sys


def main():
    if len(sys.argv) > 1:
        change_dir = sys.argv[1]
    else:
        change_dir = os.getcwd()

    change_yaml_path = os.path.join(change_dir, "change.yaml")
    publish_path = os.path.join(change_dir, "publish.md")

    errors = []

    # 检查 publish.md 存在（当 change.yaml 声明了 publish_targets 时）
    # TODO: 解析 change.yaml 中的 publish_targets
    if not os.path.exists(publish_path):
        errors.append("publish.md not found")

    # 检查 publish_targets 中 to: 路径是否指向 knowledge/ 下
    # TODO: 校验 from/to 路径的合法性和 allowed_publish_targets 约束

    if errors:
        validation_dir = os.path.join(change_dir, "validation")
        os.makedirs(validation_dir, exist_ok=True)
        with open(os.path.join(validation_dir, "publish_targets.md"), "w") as fh:
            fh.write("# publish_targets 校验失败\n\n" + "\n".join(f"- {e}" for e in errors) + "\n")
        print(f"FAIL: {'; '.join(errors)}")
        sys.exit(1)

    print("PASS: publish_targets check passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
