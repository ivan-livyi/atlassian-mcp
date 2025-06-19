# Atlassian Cloud MCP Server

A Model Context Protocol (MCP) server for integrating with Atlassian Cloud services. This server allows Cursor and other MCP-compatible AI assistants to read Jira tickets, search issues, get project information, and read Confluence pages.

## Features

### Jira
- 🎫 **Get Jira Issues**: Retrieve detailed information about specific Jira tickets
- 🔍 **Search Issues**: Use JQL (Jira Query Language) to find issues
- 📊 **Project Information**: Get details about Jira projects

### Confluence
- 📄 **Get Confluence Pages**: Retrieve detailed page content by page ID
- 🔍 **Search Pages**: Use CQL (Confluence Query Language) to find pages
- 🏠 **Space Information**: Get details about Confluence spaces

### General
- 🔐 **Secure Authentication**: Uses API tokens for secure access
- 📝 **Rich Formatting**: Displays information in a readable format
- 🎯 **Unified API**: Single server for both Jira and Confluence

## Prerequisites

- Docker and Docker Compose
- Atlassian Cloud instance with both Jira and Confluence
- Atlassian API token

## Setup

### 1. Get Your Atlassian API Token

1. Go to your Atlassian Cloud instance
2. Navigate to **Account Settings** → **Security** → **API tokens**
3. Click **Create API token**
4. Give it a name (e.g., "MCP Server") and create it
5. Copy the token (you won't be able to see it again)

### 2. Configure Cursor

Add the following to your Cursor settings (Settings → Extensions → MCP), replacing the placeholder values with your actual Atlassian credentials:

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "docker",
      "args": [
        "exec", 
        "-i",
        "-e", "ATLASSIAN_EMAIL",
        "-e", "ATLASSIAN_TOKEN", 
        "-e", "ATLASSIAN_DOMAIN",
        "atlassian-mcp-server", 
        "python", 
        "atlassian_mcp.py"
      ],
      "env": {
        "ATLASSIAN_EMAIL": "your.email@company.com",
        "ATLASSIAN_TOKEN": "your_api_token_here",
        "ATLASSIAN_DOMAIN": "your-company"
      }
    }
  }
}
```

### 3. Start the Container

```bash
make run
```

The container will run in the background and be ready to accept MCP connections.

**Important**: 
- The Docker container must be running before Cursor can connect to it
- Replace the placeholder values in the `env` section with your actual Atlassian credentials
- The `ATLASSIAN_DOMAIN` should be the subdomain part of your Atlassian URL. For example, if your Atlassian is at `https://acme-corp.atlassian.net`, then `ATLASSIAN_DOMAIN` should be `acme-corp`
- Environment variables are now configured directly in the Cursor MCP settings (not in a separate .env file)



## Example Prompts

Here are some example prompts you can use with Cursor once the MCP server is configured:

### Jira Examples

- **"What is JIRA-123 about?"** - Get details about a specific ticket
- **"Show me all issues assigned to me"** - Find your current assignments
- **"Find all high priority bugs in the PEX project"** - Search for critical issues
- **"What open issues are there in the ACME project?"** - See project status
- **"Show me issues created this week"** - Track recent work
- **"Find all unassigned tickets"** - Discover work that needs owners
- **"What's the status of issues in Sprint 42?"** - Check sprint progress
- **"Show me all bugs reported by john.doe"** - Track issues from specific users

### Confluence Examples

- **"Find documentation about API deployment"** - Search for specific content
- **"Show me all pages in the DEV space"** - Browse team documentation
- **"What's on the homepage of the ENGINEERING space?"** - Get space overview  
- **"Find pages updated in the last week"** - See recent documentation changes
- **"Search for pages containing 'database migration'"** - Find technical docs
- **"Show me all pages created by sarah.smith"** - Find author's contributions
- **"What documentation exists about authentication?"** - Search by topic

### Project Information

- **"Tell me about the PEX project"** - Get project overview and details
- **"What spaces are available in Confluence?"** - Browse available documentation areas

## Security Notes

- **Never share your API token** - Keep it secure and private
- **Rotate tokens regularly** - Create new tokens periodically and delete old ones
- **Use minimal permissions** - Ensure your Atlassian user only has access to what's needed
- **Monitor usage** - Check your Atlassian audit logs for any unusual API activity

## Contributing

Feel free to submit issues and pull requests to improve this MCP server! Contributions are welcome to add new features, fix bugs, or improve documentation.