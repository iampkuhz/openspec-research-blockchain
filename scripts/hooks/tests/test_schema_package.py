"""schema_package validator 测试"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
VALIDATOR = ROOT / "scripts" / "hooks" / "validators" / "schema_package.py"


def test_schema_package_valid():
    """当前 schema.yaml 应通过验证。"""
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), ".", "governance"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Expected pass, got:\n{result.stdout}\n{result.stderr}"


def test_schema_package_catches_bad_profile():
    """当 profile 引用不存在的 artifact 时应报告错误。"""
    import yaml

    profile_path = ROOT / "openspec" / "schemas" / "blockchain-research" / "profiles" / "primitive.schema.yaml"
    original = profile_path.read_text()

    data = yaml.safe_load(original)
    # 临时注入一个不存在的 artifact id
    data["x_required_artifacts"].append("nonexistent_artifact_id")
    profile_path.write_text(yaml.dump(data))

    try:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), ".", "governance"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, "Expected fail for nonexistent artifact in profile"
        assert "nonexistent_artifact_id" in result.stdout
    finally:
        profile_path.write_text(original)
