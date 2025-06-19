.DEFAULT_GOAL := help

VENV_DIR = venv
PYTHON = python3
PIP = $(VENV_DIR)/bin/pip
PYTHON_VENV = $(VENV_DIR)/bin/python

.PHONY: help install clean test run

help: ## Show this help message
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Set up Python virtual environment and install dependencies
	@echo "Creating Python virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt
	@echo "Installation complete!"
	@echo "To activate the virtual environment, run: source $(VENV_DIR)/bin/activate"

clean: ## Remove virtual environment and cache files
	rm -rf $(VENV_DIR)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "Cleanup complete!"

test: ## Test the MCP server startup
	@echo "Testing MCP server startup..."
	@if [ ! -d "$(VENV_DIR)" ]; then echo "Virtual environment not found. Run 'make install' first."; exit 1; fi
	ATLASSIAN_EMAIL=test@test.com ATLASSIAN_TOKEN=test ATLASSIAN_DOMAIN=test $(PYTHON_VENV) atlassian_mcp.py &
	@sleep 2
	@pkill -f atlassian_mcp.py || true
	@echo "Test complete!"

run: ## Run the MCP server (requires environment variables to be set)
	@if [ ! -d "$(VENV_DIR)" ]; then echo "Virtual environment not found. Run 'make install' first."; exit 1; fi
	@if [ -z "$$ATLASSIAN_EMAIL" ] || [ -z "$$ATLASSIAN_TOKEN" ] || [ -z "$$ATLASSIAN_DOMAIN" ]; then \
		echo "Please set ATLASSIAN_EMAIL, ATLASSIAN_TOKEN, and ATLASSIAN_DOMAIN environment variables"; \
		exit 1; \
	fi
	$(PYTHON_VENV) atlassian_mcp.py 