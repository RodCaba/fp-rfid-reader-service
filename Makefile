.PHONY: help install install-dev clean lint format test test-cov type-check security pre-commit-install pre-commit-run grpc

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

clean: ## Clean up generated files and caches
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/

grpc: ## Generate gRPC code
	./generate_grpc.sh

lint: ## Run all linting checks
	flake8 src/ tests/
	pylint src/
	mypy src/

format: ## Format code with black and isort
	black .
	isort .

format-check: ## Check code formatting without making changes
	black --check --diff .
	isort --check-only --diff .

type-check: ## Run type checking with mypy
	mypy src/ --ignore-missing-imports

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing --cov-report=xml

test-unit: ## Run only unit tests
	pytest tests/ -v -m "not integration" --cov=src --cov-report=term-missing

test-integration: ## Run only integration tests
	pytest tests/integration/ -v

security: ## Run security checks
	bandit -r src/
	safety check

pre-commit-install: ## Install pre-commit hooks
	pre-commit install

pre-commit-run: ## Run pre-commit hooks on all files
	pre-commit run --all-files

ci: grpc lint format-check type-check test-cov security ## Run full CI pipeline locally

dev-setup: install-dev grpc pre-commit-install ## Set up development environment

fix: format lint ## Auto-fix formatting and linting issues where possible
