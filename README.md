# agent-template

A [Copier](https://copier.readthedocs.io/) template for small, readable
ReAct + MCP agent projects.

Generated projects include:

- a text ReAct loop with a forgiving parser and bounded retries
- an MCP client and, optionally, a sample MCP server
- Ollama and/or OpenAI-compatible model adapters, plus a scripted fake
- JSONL traces, metrics, and a scripted test suite that runs without a model
- CLI commands for `doctor`, `tools`, `call`, `ask`, `repl`, and `serve`
- `AGENTS.md` and docs that explain the invariants

## Use it

```bash
uvx copier copy gh:ajay126z/agent-template my-agent
cd my-agent
uv sync --all-extras
uv run my-agent doctor
uv run my-agent ask "What is (17 * 3) + 9?"
```

Or from a local checkout:

```bash
uvx copier copy /path/to/agent-template my-agent
```

Non-interactive:

```bash
uvx copier copy --defaults --trust . /tmp/my-agent
```

## Questions

| Variable | Default | Meaning |
| --- | --- | --- |
| `project_name` | `My Agent` | Human-readable name. |
| `package_name` | derived | Python import name (snake_case). |
| `cli_name` | derived | Installed command name. |
| `description` | one-liner | Project description. |
| `author_name` / `author_email` | empty | Package metadata. |
| `env_prefix` | derived | Environment prefix, e.g. `MY_AGENT_`. |
| `llm_provider` | `both` | `ollama`, `openai`, or `both`. |
| `default_model` | per provider | Initial model name. |
| `include_mcp_server` | `true` | Bundle calculator + time tools. |
| `include_sessions` | `true` | JSONL Q/A sessions and session CLI. |
| `enable_tracing` | `true` | Write traces by default. |
| `python_version` | `3.12` | Minimum Python version. |
| `license` | `MIT` | MIT or Proprietary. |
| `run_uv_sync` | `false` | Run `uv sync` after generating. |

## Update a generated project

Generated projects keep their answers in `.copier-answers.yml`:

```bash
cd my-agent
uvx copier update --trust
```

Tag template releases (`v0.1.0`, `v0.2.0`, ...) so updates are reproducible.

## Develop the template

```bash
uv sync
uv run ruff check .
uv run pytest -q -m "not slow"   # render matrix, no installs
uv run pytest -q                 # also installs and tests generated projects
```

The fast suite renders several answer combinations into temporary directories
and checks that no Jinja markers or project-specific names leak through. The
slow suite runs `uv sync`, `ruff`, and `pytest` inside a generated project.

To smoke-test one default project by hand:

```bash
make render
```

## Layout

```text
agent-template/
  copier.yml              # questions, exclusions, tasks
  template/               # rendered into the new project
  tests/test_render.py    # render matrix
  tests/test_generated.py # slow end-to-end install/test
  docs/design.md          # why the template looks like this
```
