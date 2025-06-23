.DEFAULT_GOAL := help

.PHONY: help setup install run test clean

help: ## Show this help message
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Set up Python virtual environment and install dependencies
	@echo "🔍 Checking Python installation..."
	@if ! command -v python3 >/dev/null 2>&1; then \
		echo "\033[31m❌ Python 3 is not installed!\033[0m"; \
		echo "\033[33m📋 To install Python on macOS, run:\033[0m"; \
		echo "   \033[36mbrew install python\033[0m"; \
		echo ""; \
		echo "\033[33m💡 If you don't have Homebrew installed, first run:\033[0m"; \
		echo "   \033[36m/bin/bash -c \"\$$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"\033[0m"; \
		echo ""; \
		echo "\033[33m🔄 After installing Python, run 'make install' again\033[0m"; \
		exit 1; \
	fi
	@echo "🔍 Checking Python version..."
	@PYTHON_VERSION=$$(python3 -c "import sys; print('{}.{}'.format(sys.version_info.major, sys.version_info.minor))"); \
	if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then \
		echo "\033[31m❌ Python version $$PYTHON_VERSION is too old. Required: 3.8 or higher\033[0m"; \
		echo "\033[33m📋 To update Python on macOS, run:\033[0m"; \
		echo "   \033[36mbrew install python\033[0m"; \
		echo "   \033[36m# or for a specific version:\033[0m"; \
		echo "   \033[36mbrew install python@3.11\033[0m"; \
		echo ""; \
		echo "\033[33m💡 If you installed a specific version, you might need to use:\033[0m"; \
		echo "   \033[36mpython3.11 -m venv .venv\033[0m (instead of python3)"; \
		echo ""; \
		echo "\033[33m🔄 After updating Python, run 'make install' again\033[0m"; \
		exit 1; \
	else \
		echo "\033[32m✅ Python $$PYTHON_VERSION meets requirements (3.8+)\033[0m"; \
	fi
	@echo "🚀 Setting up Python virtual environment..."
	python3 -m venv .venv
	./.venv/bin/pip install --upgrade pip
	@echo "\033[32m✅ Virtual environment created!\033[0m"
	@echo "📦 Installing dependencies..."
	./.venv/bin/pip install -r requirements.txt
	@echo "\033[32m✅ Dependencies installed successfully!\033[0m"
	@echo "\033[36m🔗 Server is ready for MCP connections\033[0m"

test: ## Test the MCP server connection
	@echo "🧪 Testing MCP server..."
	@echo "ATLASSIAN_EMAIL=test@example.com ATLASSIAN_TOKEN=dummy ATLASSIAN_DOMAIN=test ./.venv/bin/python atlassian_mcp.py"
	@echo "\033[36m💡 Press Ctrl+C to stop the test\033[0m"

clean: ## Remove virtual environment and clean up
	@echo "🧹 Cleaning up..."
	rm -rf .venv
	rm -rf __pycache__
	rm -rf *.pyc
	@echo "\033[32m✅ Cleanup complete!\033[0m" 