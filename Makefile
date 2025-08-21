.PHONY: lint format lint-fix quality test clean

# Code quality commands
lint:
	uv run ruff check .

format:
	uv run ruff format .

lint-fix:
	uv run ruff check --fix .

quality: lint
	uv run ruff format --check .

# Test commands
test:
	uv run python -m pytest tests/ -v

test-rag:
	uv run python tests/test_rag_knowledge.py

# Development setup
install:
	uv sync

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete

# Combined quality check
check: quality test

# File watching (requires fswatch: brew install fswatch)
watch:
	@echo "🔍 Starting file watcher..."
	@./scripts/watch-quality.sh

help:
	@echo "Available commands:"
	@echo "  lint      - Run ruff linter"
	@echo "  format    - Format code with ruff"
	@echo "  lint-fix  - Auto-fix linting issues"
	@echo "  quality   - Check code quality (lint + format check)"
	@echo "  test      - Run all tests"
	@echo "  test-rag  - Run RAG tests specifically"
	@echo "  check     - Run quality + tests"
	@echo "  watch     - Watch files and run ruff on changes"
	@echo "  install   - Install dependencies"
	@echo "  clean     - Clean up cache files"