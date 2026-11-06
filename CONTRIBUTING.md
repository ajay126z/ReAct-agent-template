# Contributing to the template

## Ground rules

- Every answer combination must render, lint, and test.
- Keep the generated project small enough to read in one sitting.
- Do not add a second way to do the same thing (two CLI frameworks, two tracer
  implementations, two config systems).
- When you change generated behavior, update the generated `README.md`,
  `AGENTS.md`, and docs in the same change.

## Workflow

```bash
uv sync
uv run ruff check .
uv run ruff format tests
uv run pytest -q -m "not slow"
uv run pytest -q            # includes installing generated projects
```

## Adding a Copier question

1. Add the question to `copier.yml` with a sane default.
2. Use it in a Jinja block at the narrowest scope.
3. If it removes files, add a templated `_exclude` entry.
4. Add at least one render combination to `tests/test_render.py`.
5. Update the variable table in `README.md`.

## Adding a generated feature

1. Implement it in `template/` and add a test under `template/tests/`.
2. Render a project with `make render` and run its suite.
3. Add any new files or flags to the fast render assertions.
4. Update the generated docs.

## Releasing

Tag with semantic versioning. Generated projects can then run
`copier update --trust` and review the diff. If a change needs manual
migration, add a `_migrations` entry in `copier.yml` and document it.
