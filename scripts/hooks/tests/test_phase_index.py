"""phase_index validator 测试"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
VALIDATOR = ROOT / "scripts" / "hooks" / "validators" / "phase_index.py"


def test_phase_index_valid():
    """当前 _phase_index.yaml 应通过验证。"""
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), ".", "governance"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Expected pass, got:\n{result.stdout}\n{result.stderr}"


def test_phase_index_reports_missing_spec():
    """当 spec 不存在时应报告错误。"""
    import yaml

    index_path = ROOT / "harness" / "rules" / "_phase_index.yaml"
    original = index_path.read_text()

    data = yaml.safe_load(original)
    # 临时注入一个不存在的 spec
    data["phases"]["request"]["depends"]["specs"].append("nonexistent-fake-spec")
    index_path.write_text(yaml.dump(data))

    try:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), ".", "governance"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, "Expected fail for nonexistent spec"
        assert "nonexistent-fake-spec" in result.stdout
    finally:
        index_path.write_text(original)
