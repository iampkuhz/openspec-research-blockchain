#!/usr/bin/env python3
"""required_files — 检查 change.yaml 声明的 required files 是否存在。

触发方式：post_write
输入：change.yaml 所在目录路径
输出：校验通过返回 0，失败返回非 0 并写入 validation/required_files.md
"""

import os
import sys


def main():
    change_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    change_yaml_path = os.path.join(change_dir, "change.yaml")

    # TODO: 解析 change.yaml 获取 base schema 的 required_files 列表
    required = ["change.yaml", "request.md", "plan.md"]

    missing = [f for f in required if not os.path.exists(os.path.join(change_dir, f))]

    if missing:
        validation_dir = os.path.join(change_dir, "validation")
        os.makedirs(validation_dir, exist_ok=True)
        with open(os.path.join(validation_dir, "required_files.md"), "w") as fh:
            fh.write(f"# required_files 校验失败\n\n缺失文件：{', '.join(missing)}\n")
        print(f"FAIL: missing required files: {', '.join(missing)}")
        sys.exit(1)

    print("PASS: all required files present")
    sys.exit(0)


if __name__ == "__main__":
    main()
