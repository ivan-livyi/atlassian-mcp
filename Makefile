.DEFAULT_GOAL := help

CONTAINER_NAME = atlassian-mcp-server

.PHONY: help start stop restart status logs build clean

help: ## Show this help message
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

start: ## Start the MCP server container
	@echo "Starting Atlassian MCP server..."
	docker-compose up --build -d
	@echo "Container started successfully!"
	@echo "Container is ready for MCP connections"
	@echo "Use 'make logs' to view logs or 'make status' to check status"

stop: ## Stop the MCP server container
	@echo "Stopping Atlassian MCP server..."
	docker-compose down
	@echo "Container stopped"

restart: ## Restart the MCP server container
	@echo "Restarting Atlassian MCP server..."
	docker-compose down
	docker-compose up --build -d
	@echo "Container restarted successfully!"

status: ## Check container status
	@echo "Container status:"
	docker-compose ps

logs: ## View container logs
	docker-compose logs -f atlassian-mcp

build: ## Build the Docker image
	@echo "Building Docker image..."
	docker-compose build
	@echo "Build complete!"

clean: ## Remove containers and clean up Docker resources
	@echo "Cleaning up Docker resources..."
	docker-compose down --volumes --remove-orphans
	docker system prune -f
	@echo "Cleanup complete!" 