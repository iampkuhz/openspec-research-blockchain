#!/usr/bin/env python3
"""yaml_loader — 统一 YAML 加载逻辑。

职责：
1. 安全加载 YAML
2. 返回明确错误
3. 保持所有脚本使用同一套 YAML 加载逻辑
"""

import yaml


def load_yaml(path: str) -> dict:
    """安全加载 YAML 文件，返回 dict。

    Raises:
        FileNotFoundError: 文件不存在
        yaml.YAMLError: YAML 解析失败
        ValueError: YAML 根节点不是 dict
    """
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"YAML root at {path} is not a mapping, got {type(data).__name__}")

    return data


def load_yaml_safe(path: str) -> tuple[dict | None, str | None]:
    """安全加载 YAML 文件，返回 (data, error) 元组。

    不抛出异常，而是返回 error 字符串。
    """
    try:
        data = load_yaml(path)
        return data, None
    except FileNotFoundError:
        return None, f"File not found: {path}"
    except yaml.YAMLError as e:
        return None, f"YAML parse error at {path}: {e}"
    except ValueError as e:
        return None, str(e)
