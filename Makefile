.DEFAULT_GOAL := help

.PHONY: help setup install run test clean

help: ## Show this help message
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Set up Python virtual environment and install dependencies
	@echo "🚀 Setting up Python virtual environment..."
	python3 -m venv .venv
	./venv/bin/pip install --upgrade pip
	@echo "\033[32m✅ Virtual environment created!\033[0m"
	@echo "📦 Installing dependencies..."
	./venv/bin/pip install -r requirements.txt
	@echo "\033[32m✅ Dependencies installed successfully!\033[0m"
	@echo "\033[36m🔗 Server is ready for MCP connections\033[0m"

test: ## Test the MCP server connection
	@echo "🧪 Testing MCP server..."
	@echo "ATLASSIAN_EMAIL=test@example.com ATLASSIAN_TOKEN=dummy ATLASSIAN_DOMAIN=test ./venv/bin/python atlassian_mcp.py"
	@echo "\033[36m💡 Press Ctrl+C to stop the test\033[0m"

clean: ## Remove virtual environment and clean up
	@echo "🧹 Cleaning up..."
	rm -rf venv
	rm -rf __pycache__
	rm -rf *.pyc
	@echo "\033[32m✅ Cleanup complete!\033[0m" 