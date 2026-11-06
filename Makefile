.PHONY: sync lint format test check test-render test-full render

sync:
	uv sync

lint:
	uv run ruff check .

format:
	uv run ruff format .

test:
	uv run pytest -q

test-render:
	uv run pytest -q -m "not slow"

test-full:
	uv run pytest -q

check:
	uv run ruff check . && uv run pytest -q -m "not slow"

render:
	rm -rf /tmp/react-agent-template-smoke
	uv run copier copy --defaults --trust . /tmp/react-agent-template-smoke
	cd /tmp/react-agent-template-smoke && uv sync --all-extras && uv run pytest -q -m "not integration"
