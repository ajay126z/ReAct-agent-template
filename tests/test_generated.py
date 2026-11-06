from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from copier import run_copy

TEMPLATE_ROOT = Path(__file__).resolve().parents[1]

pytestmark = pytest.mark.slow


@pytest.fixture(scope="module")
def generated_project(tmp_path_factory: pytest.TempPathFactory) -> Path:
    destination = tmp_path_factory.mktemp("generated") / "my-agent"
    run_copy(
        str(TEMPLATE_ROOT),
        destination,
        data={},
        defaults=True,
        unsafe=True,
        quiet=True,
    )
    subprocess.run(
        ["uv", "sync", "--all-extras"],
        cwd=destination,
        check=True,
        capture_output=True,
        text=True,
    )
    return destination


def run(project: Path, *command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["uv", "run", *command],
        cwd=project,
        check=True,
        capture_output=True,
        text=True,
    )


def test_generated_project_lints(generated_project: Path) -> None:
    run(generated_project, "ruff", "check", ".")


def test_generated_project_is_formatted(generated_project: Path) -> None:
    run(generated_project, "ruff", "format", "--check", "src", "tests")


def test_generated_project_tests_pass(generated_project: Path) -> None:
    result = run(generated_project, "pytest", "-q")
    assert "passed" in result.stdout
