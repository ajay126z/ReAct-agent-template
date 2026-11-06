from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from copier import run_copy

TEMPLATE_ROOT = Path(__file__).resolve().parents[1]

COMBINATIONS: dict[str, dict[str, Any]] = {
    "default": {},
    "ollama": {"llm_provider": "ollama", "default_model": "qwen3.5:9b"},
    "openai": {"llm_provider": "openai", "default_model": "gpt-4o-mini"},
    "no_server": {"include_mcp_server": False},
    "no_sessions": {"include_sessions": False},
    "minimal": {"include_mcp_server": False, "include_sessions": False},
    "proprietary": {"license": "Proprietary"},
    "no_tracing": {"enable_tracing": False},
    "custom_names": {
        "project_name": "Research Bot",
        "package_name": "research_bot",
        "cli_name": "research-bot",
        "env_prefix": "RESEARCH_BOT_",
    },
}


def render(destination: Path, **data: Any) -> Path:
    run_copy(
        str(TEMPLATE_ROOT),
        destination,
        data=data,
        defaults=True,
        unsafe=True,
        quiet=True,
    )
    return destination


@pytest.fixture(params=COMBINATIONS.items(), ids=COMBINATIONS.keys())
def rendered(request: pytest.FixtureRequest, tmp_path: Path) -> tuple[Path, dict[str, Any]]:
    name, data = request.param
    base = tmp_path / name
    base.mkdir()
    return render(base / "generated", **data), data


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def package_name(data: dict[str, Any]) -> str:
    return data.get("package_name", "my_agent")


def cli_name(data: dict[str, Any]) -> str:
    return data.get("cli_name", "my-agent")


def test_all_text_files_are_fully_rendered(rendered: tuple[Path, dict[str, Any]]) -> None:
    project, _ = rendered
    offenders: list[str] = []
    for path in project.rglob("*"):
        if not path.is_file():
            continue
        text = read(path)
        if any(marker in text for marker in ("{{", "{%", "{#")):
            offenders.append(str(path.relative_to(project)))

    assert offenders == []


def test_common_files_exist(rendered: tuple[Path, dict[str, Any]]) -> None:
    project, data = rendered
    package = package_name(data)
    expected = [
        "pyproject.toml",
        "README.md",
        "AGENTS.md",
        ".env.example",
        ".gitignore",
        ".python-version",
        ".copier-answers.yml",
        "Makefile",
        "docs/architecture.md",
        f"src/{package}/cli.py",
        f"src/{package}/config.py",
        f"src/{package}/agent/react.py",
        f"src/{package}/agent/parser.py",
        f"src/{package}/agent/llm.py",
    ]
    missing = [name for name in expected if not (project / name).is_file()]
    assert missing == []


def test_optional_server_files_follow_the_flag(rendered: tuple[Path, dict[str, Any]]) -> None:
    project, data = rendered
    package = package_name(data)
    server_files = [
        project / "src" / package / "server.py",
        project / "src" / package / "tools.py",
        project / "tests" / "test_mcp_integration.py",
        project / "tests" / "test_tools.py",
        project / "docs" / "adding-tools.md",
    ]

    if data.get("include_mcp_server", True):
        missing = [str(path.relative_to(project)) for path in server_files if not path.is_file()]
        assert missing == []
    else:
        present = [str(path.relative_to(project)) for path in server_files if path.exists()]
        assert present == []


def test_optional_session_files_follow_the_flag(rendered: tuple[Path, dict[str, Any]]) -> None:
    project, data = rendered
    package = package_name(data)
    memory = project / "src" / package / "agent" / "memory.py"
    tests = project / "tests" / "test_memory.py"

    if data.get("include_sessions", True):
        assert memory.is_file()
        assert tests.is_file()
    else:
        assert not memory.exists()
        assert not tests.exists()


def test_license_follows_the_answer(rendered: tuple[Path, dict[str, Any]]) -> None:
    project, data = rendered
    license_file = project / "LICENSE"

    if data.get("license", "MIT") == "MIT":
        assert license_file.is_file()
        assert "MIT License" in read(license_file)
    else:
        assert not license_file.exists()


def test_trace_default_is_valid_python(rendered: tuple[Path, dict[str, Any]]) -> None:
    project, data = rendered
    package = package_name(data)
    config = read(project / "src" / package / "config.py")

    expected = "True" if data.get("enable_tracing", True) else "False"
    assert f"trace_enabled: bool = {expected}" in config
    assert "trace_enabled: bool = true" not in config
    assert "trace_enabled: bool = false" not in config


def test_provider_dependencies_and_cli_name(rendered: tuple[Path, dict[str, Any]]) -> None:
    project, data = rendered
    pyproject = read(project / "pyproject.toml")
    provider = data.get("llm_provider", "both")

    if provider in {"ollama", "both"}:
        assert '"ollama' in pyproject
    else:
        assert '"ollama' not in pyproject

    if provider in {"openai", "both"}:
        assert "httpx" in pyproject

    package = package_name(data)
    assert f'{cli_name(data)} = "{package}.cli:main"' in pyproject


def test_custom_names_flow_through_the_project(rendered: tuple[Path, dict[str, Any]]) -> None:
    project, data = rendered
    if data.get("package_name") != "research_bot":
        pytest.skip("custom-name assertions only apply to that combination")

    assert (project / "src" / "research_bot" / "cli.py").is_file()
    assert "RESEARCH_BOT_" in read(project / "src" / "research_bot" / "config.py")
    assert 'research-bot = "research_bot.cli:main"' in read(project / "pyproject.toml")
    assert "Research Bot" in read(project / "README.md")


def test_render_writes_answers_file(tmp_path: Path) -> None:
    project = render(tmp_path / "generated")
    answers = read(project / ".copier-answers.yml")

    assert "package_name: my_agent" in answers
    assert "llm_provider: both" in answers
