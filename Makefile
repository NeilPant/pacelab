.PHONY: sync check lint format types test serve

sync:
	uv sync --locked

check: lint types test

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check --fix .

types:
	uv run mypy

test:
	uv run pytest -q

serve:
	uv run pacelab-server
