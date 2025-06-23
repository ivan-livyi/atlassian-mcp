# Atlassian Cloud MCP Server

A Model Context Protocol (MCP) server for integrating with Atlassian Cloud services. 
This server allows Cursor and other MCP-compatible AI assistants to read Jira tickets, search issues, get project information, and read Confluence pages.

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

- Python 3.8 or higher
- Atlassian Cloud instance with both Jira and Confluence
- Atlassian API token

## Installation

### 1. Clone and Set Up the Project

```bash
git clone https://github.com/ivan-livyi/atlassian-mcp
cd atlassian-mcp
make install
```

This will create a Python virtual environment and install all required dependencies.

### 2. Get Your Atlassian API Token

1. Go to your Atlassian Cloud instance
2. Navigate to **Account Settings** → **Security** → **API tokens**
3. Click **Create API token**
4. Give it a name (e.g., "MCP Server") and create it
5. Copy the token (you won't be able to see it again)

### 3. Configure Cursor

#### Option 1: Using Cursor Settings UI
1. Open Cursor
2. Go to **Settings** → **Extensions** → **MCP**
3. Add a new MCP server with the following configuration

#### Option 2: Manual Configuration
Add the following to your `~/.cursor/mcp.json` file, replacing the placeholder values with your actual paths and Atlassian credentials:

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "/absolute/path/to/your/atlassian-mcp/.venv/bin/python",
      "args": ["/absolute/path/to/your/atlassian-mcp/atlassian_mcp.py"],
      "env": {
        "ATLASSIAN_EMAIL": "your.email@company.com",
        "ATLASSIAN_TOKEN": "your_api_token_here",
        "ATLASSIAN_DOMAIN": "your-company"
      }
    }
  }
}
```

**Important Configuration Notes**:
- Replace `/absolute/path/to/your/atlassian-mcp/` with the full path to where you cloned this repository
- Replace the placeholder values in the `env` section with your actual Atlassian credentials
- The `ATLASSIAN_DOMAIN` should be the subdomain part of your Atlassian URL. For example, if your Atlassian is at `https://acme-corp.atlassian.net`, then `ATLASSIAN_DOMAIN` should be `acme-corp`

## Example Prompts

Here are some example prompts you can use with Cursor once the MCP server is configured:

### Jira Examples

- **"What is JIRA-123 about?"** - Get details about a specific ticket
- **"Show me all issues assigned to me"** - Find your current assignments  
- **"Find all high priority bugs in PROJECT project"** - Search for critical issues
- **"What open issues are there in PROJECT project?"** - See project status
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

- **"Tell me about the PROJECT project"** - Get project overview and details
- **"What spaces are available in Confluence?"** - Browse available documentation areas

## Troubleshooting

### Common Issues

1. **"Authentication failed"** - Check that your `ATLASSIAN_EMAIL`, `ATLASSIAN_TOKEN`, and `ATLASSIAN_DOMAIN` are correct
2. **"Command not found"** - Make sure you're using the absolute path to the Python executable in your virtual environment
3. **"Module not found"** - Run `make install` to ensure all dependencies are installed
4. **"Permission denied"** - Ensure the Python script has execute permissions: `chmod +x atlassian_mcp.py`

### Getting Help

If you encounter issues:
1. Check that your API token is valid and has the necessary permissions
2. Verify your Atlassian domain is correct (without `.atlassian.net`)
3. Test the connection using the `make test` command
4. Check Cursor's MCP logs for detailed error messages

## Development

### Project Structure

```
atlassian-mcp/
├── atlassian_mcp.py          # Main MCP server implementation
├── cursor-config-example.json # Example Cursor configuration
├── requirements.txt          # Python dependencies
├── Makefile                 # Development commands
└── README.md               # This file
```

### Available Make Commands

- `make setup` - Create Python virtual environment and install dependencies~~~~
- `make test` - Test server connection
- `make clean` - Remove virtual environment and clean up

## Security Notes

- **Never share your API token** - Keep it secure and private
- **Rotate tokens regularly** - Create new tokens periodically and delete old ones
- **Use minimal permissions** - Ensure your Atlassian user only has access to what's needed
- **Monitor usage** - Check your Atlassian audit logs for any unusual API activity

## Contributing

Feel free to submit issues and pull requests to improve this MCP server! Contributions are welcome to add new features, fix bugs, or improve documentation.