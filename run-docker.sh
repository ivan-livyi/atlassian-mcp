#!/bin/bash

if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your Atlassian credentials before running again."
    exit 1
fi

echo "Building and starting Atlassian MCP server..."
docker-compose up --build -d

echo "Container is running. To view logs:"
echo "docker-compose logs -f atlassian-mcp"
echo ""
echo "To stop the container:"
echo "docker-compose down" 