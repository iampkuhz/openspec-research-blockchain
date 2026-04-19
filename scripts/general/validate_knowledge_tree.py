#!/usr/bin/env python3
"""
校验 knowledge/ 目录结构是否符合 canonical 模型。

职责：
- 校验 knowledge/ 目录结构是否符合 canonical 模型
- 校验 analysis/synthesis/ 下是否错误出现二级分类目录
- 校验每个 primitive topic 目录里必须有 artifact.md
- 校验每个 decision topic 目录里必须有 artifact.md
- 校验 registry 文件存在且格式正确
- 校验不存在未注册 domain_id 的目录
- 校验不存在空 topic 目录

用法:
    python scripts/general/validate_knowledge_tree.py [knowledge/]
"""

import sys
from pathlib import Path
import yaml


def load_domains(registry_path: Path) -> set:
    """从 domains.yaml 加载已注册的 domain_id 集合"""
    if not registry_path.exists():
        return set()
    content = yaml.safe_load(registry_path.read_text())
    if not content or "domains" not in content:
        return set()
    return {d["id"] for d in content["domains"] if isinstance(d, dict) and "id" in d}


def validate_tree(knowledge_root: Path) -> list:
    """校验 knowledge 目录树，返回 errors 列表"""
    errors = []
    analysis_root = knowledge_root / "analysis"
    decisions_root = knowledge_root / "decisions"

    # 1. 校验 registry 文件存在
    registry_path = analysis_root / "_registry" / "domains.yaml"
    if not registry_path.exists():
        errors.append(f"Missing registry file: {registry_path}")
        domains = set()
    else:
        domains = load_domains(registry_path)
        if not domains:
            errors.append(f"Registry file is empty or invalid: {registry_path}")

    # 2. 校验 primitives 目录
    primitives_root = analysis_root / "primitives"
    if primitives_root.exists():
        for domain_dir in sorted(primitives_root.iterdir()):
            if not domain_dir.is_dir():
                continue
            if domain_dir.name.startswith("_") or domain_dir.name == ".":
                continue
            domain_id = domain_dir.name
            if domains and domain_id not in domains:
                errors.append(f"Unregistered domain_id in primitives: {domain_id} (add to domains.yaml)")
            for topic_dir in sorted(domain_dir.iterdir()):
                if not topic_dir.is_dir():
                    continue
                artifact = topic_dir / "artifact.md"
                if not artifact.exists():
                    errors.append(f"Missing artifact.md in: {topic_dir.relative_to(knowledge_root)}")

    # 3. 校验 synthesis 目录（扁平化，不应有二级分类）
    synthesis_root = analysis_root / "synthesis"
    if synthesis_root.exists():
        for item in sorted(synthesis_root.iterdir()):
            if not item.is_dir():
                continue
            # 检查是否有二级目录（错误）
            subdirs = [d for d in item.iterdir() if d.is_dir()]
            if subdirs:
                errors.append(
                    f"synthesis/ 下不应有二级分类目录: {item.relative_to(synthesis_root)} "
                    f"包含子目录 {[d.name for d in subdirs]}；synthesis 应扁平化"
                )
            artifact = item / "artifact.md"
            if not artifact.exists():
                errors.append(f"Missing artifact.md in: {item.relative_to(knowledge_root)}")

    # 4. 校验 decisions 目录
    if decisions_root.exists():
        for domain_dir in sorted(decisions_root.iterdir()):
            if not domain_dir.is_dir():
                continue
            if domain_dir.name == "README.md" or domain_dir.name.startswith("."):
                continue
            domain_id = domain_dir.name
            if domains and domain_id not in domains:
                errors.append(f"Unregistered domain_id in decisions: {domain_id} (add to domains.yaml)")
            for topic_dir in sorted(domain_dir.iterdir()):
                if not topic_dir.is_dir():
                    continue
                artifact = topic_dir / "artifact.md"
                if not artifact.exists():
                    errors.append(f"Missing artifact.md in: {topic_dir.relative_to(knowledge_root)}")
                # verdict.md 是 decision 的交付物
                verdict = topic_dir / "verdict.md"
                if not verdict.exists():
                    errors.append(f"Missing verdict.md in: {topic_dir.relative_to(knowledge_root)}")

    # 5. 检查不应存在的旧目录结构
    old_domains = analysis_root / "domains"
    if old_domains.exists():
        errors.append(
            f"Legacy directory 'analysis/domains/' found; "
            f"domain 不再作为独立 object_type，请迁移内容到 synthesis/ 或 primitives/"
        )

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_knowledge_tree.py [knowledge/]")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Path not found: {target}")
        sys.exit(1)

    # 找到 knowledge root
    if target.name == "knowledge":
        knowledge_root = target
    elif target.parent.name == "knowledge":
        knowledge_root = target.parent
    else:
        knowledge_root = None
        for p in [target] + list(target.parents):
            if p.name == "knowledge":
                knowledge_root = p
                break
        if not knowledge_root:
            print("Could not find knowledge/ root from given path")
            sys.exit(1)

    errors = validate_tree(knowledge_root)

    if errors:
        print(f"Found {len(errors)} directory structure issues:\n")
        for e in errors:
            print(f"  [error] {e}")
        sys.exit(1)
    else:
        print("Knowledge tree structure looks good!")
        sys.exit(0)


if __name__ == "__main__":
    main()
