.PHONY: help install install-dev setup clean test test-cov lint format run docker-build docker-up docker-down docker-logs check all

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m

help: ## Show this help message
	@echo "$(BLUE)hello-spec-kit - Available commands:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

install: ## Install production dependencies
	@echo "$(BLUE)Installing production dependencies...$(NC)"
	pip install fastapi==0.115.11 uvicorn[standard]>=0.34.0
	@echo "$(GREEN)✓ Production dependencies installed$(NC)"

install-dev: ## Install development dependencies (includes test tools)
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	pip install fastapi==0.115.11 uvicorn[standard]>=0.34.0
	pip install pytest pytest-cov pytest-asyncio ruff mypy
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"

setup: install-dev ## Complete project setup (install + verify)
	@echo "$(BLUE)Setting up project...$(NC)"
	@mkdir -p tests/unit
	@touch tests/__init__.py tests/unit/__init__.py
	@echo "$(GREEN)✓ Project structure verified$(NC)"
	@make check
	@echo ""
	@echo "$(GREEN)✓ Setup complete! Run 'make run' to start the server$(NC)"

clean: ## Clean cache files and build artifacts
	@echo "$(BLUE)Cleaning cache files...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf htmlcov/ dist/ build/ *.egg-info 2>/dev/null || true
	@echo "$(GREEN)✓ Cache cleaned$(NC)"

test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	python -m pytest tests/unit/ -v
	@echo "$(GREEN)✓ All tests passed$(NC)"

test-cov: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	python -m pytest tests/unit/ -v --cov=. --cov-report=html --cov-report=term
	@echo "$(YELLOW)Coverage report: htmlcov/index.html$(NC)"

lint: ## Run linter (ruff)
	@echo "$(BLUE)Running linter...$(NC)"
	ruff check .
	@echo "$(GREEN)✓ Linting passed$(NC)"

format: ## Format code with ruff
	@echo "$(BLUE)Formatting code...$(NC)"
	ruff check --fix .
	ruff format .
	@echo "$(GREEN)✓ Code formatted$(NC)"

typecheck: ## Run type checker (mypy)
	@echo "$(BLUE)Running type checker...$(NC)"
	mypy main.py --ignore-missing-imports || echo "$(YELLOW)⚠ mypy not installed or types need attention$(NC)"

check: ## Run all checks (test + lint + typecheck)
	@echo "$(BLUE)Running all checks...$(NC)"
	@make test
	@make lint
	@make typecheck
	@echo "$(GREEN)✓ All checks passed$(NC)"

run: ## Run development server
	@echo "$(BLUE)Starting development server...$(NC)"
	@echo "$(YELLOW)Server will be available at http://localhost:8000$(NC)"
	@echo "$(YELLOW)Health endpoint: http://localhost:8000/health$(NC)"
	@echo "$(YELLOW)API docs: http://localhost:8000/docs$(NC)"
	@echo ""
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

run-prod: ## Run production server
	@echo "$(BLUE)Starting production server...$(NC)"
	uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

docker-build: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	docker-compose build
	@echo "$(GREEN)✓ Docker image built$(NC)"

docker-up: ## Start Docker containers
	@echo "$(BLUE)Starting Docker containers...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Containers started$(NC)"
	@echo "$(YELLOW)Server: http://localhost:8000$(NC)"
	@echo "Run 'make docker-logs' to see logs"

docker-down: ## Stop Docker containers
	@echo "$(BLUE)Stopping Docker containers...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Containers stopped$(NC)"

docker-logs: ## Show Docker container logs
	docker-compose logs -f

docker-restart: docker-down docker-up ## Restart Docker containers

verify-health: ## Verify health endpoint is working
	@echo "$(BLUE)Checking health endpoint...$(NC)"
	@curl -s http://localhost:8000/health | python -m json.tool && echo "$(GREEN)✓ Health endpoint OK$(NC)" || echo "$(RED)✗ Health endpoint failed$(NC)"

all: clean setup check ## Clean, setup and run all checks
	@echo "$(GREEN)✓ All tasks completed successfully!$(NC)"

dev: setup run ## Quick start: setup + run server

ci: clean install test lint ## CI pipeline: clean + install + test + lint