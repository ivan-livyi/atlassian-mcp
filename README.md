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

### 1. Start the Container

```bash
make start
```

The container will run in the background and be ready to accept MCP connections. Environment variables will be provided by Cursor through the MCP configuration.

### 2. Managing the Container

Available commands:

```bash
make start     # Start the MCP server container
make stop      # Stop the MCP server container
make restart   # Restart the container
make status    # Check container status
make logs      # View container logs
```

### 2. Get Your Atlassian API Token

1. Go to your Atlassian Cloud instance
2. Navigate to **Account Settings** → **Security** → **API tokens**
3. Click **Create API token**
4. Give it a name (e.g., "MCP Server") and create it
5. Copy the token (you won't be able to see it again)

## Usage with Cursor

To use this MCP server with Cursor:

### 1. Start the Container

Make sure your Docker container is running first:

```bash
make start
```

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

**Important**: 
- The Docker container must be running before Cursor can connect to it
- Replace the placeholder values in the `env` section with your actual Atlassian credentials
- The `ATLASSIAN_DOMAIN` should be the subdomain part of your Atlassian URL. For example, if your Atlassian is at `https://acme-corp.atlassian.net`, then `ATLASSIAN_DOMAIN` should be `acme-corp`
- Environment variables are now configured directly in the Cursor MCP settings (not in a separate .env file)

### 2. Available Tools

Once configured, you'll have access to these tools in Cursor:

#### Jira Tools

##### `get_jira_issue`
Get detailed information about a specific issue.

**Example**: "Get details for ticket PEX-2288"

##### `search_jira_issues` 
Search for issues using JQL.

**Example**: "Find all open issues assigned to me"
- JQL: `assignee = currentUser() AND status != Done`

**Example**: "Find high priority bugs in the PEX project"
- JQL: `project = PEX AND issuetype = Bug AND priority = High`

##### `get_jira_project`
Get information about a project.

**Example**: "Tell me about the PEX project"

#### Confluence Tools

##### `get_confluence_page`
Get detailed information and content from a specific page.

**Example**: "Get the content of page 123456789"

##### `search_confluence_pages`
Search for pages using CQL.

**Example**: "Find all documentation pages in the DEV space"
- CQL: `space = DEV AND title ~ "documentation"`

**Example**: "Find pages updated recently"
- CQL: `lastModified >= now("-7d")`

##### `get_confluence_space`
Get information about a Confluence space.

**Example**: "Tell me about the DEV space"

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

## API Authentication

The server uses HTTP Basic Authentication with your email and API token. The authentication format matches the curl examples:

```bash
# Jira API
curl -u "your.email@company.com:YOUR_API_TOKEN" \
  -H "Accept: application/json" \
  "https://your-domain.atlassian.net/rest/api/3/issue/TICKET-123"

# Confluence API
curl -u "your.email@company.com:YOUR_API_TOKEN" \
  -H "Accept: application/json" \
  "https://your-domain.atlassian.net/wiki/rest/api/content/123456789"
```

## Troubleshooting

### Docker Issues

#### Container Won't Start
```bash
# Check if Docker is running
docker ps

# View container logs
docker-compose logs atlassian-mcp

# Rebuild the container
docker-compose down
docker-compose up --build
```

#### Cursor Can't Connect to Docker Container
```bash
# Ensure container is running
docker-compose ps

# Container should show as "Up"
# If not, check logs:
docker-compose logs atlassian-mcp

# Test container manually
docker exec -it atlassian-mcp-server python atlassian_mcp.py
```

#### Environment Variables Not Working
- Check that your Cursor MCP configuration includes the `env` section with your credentials
- Ensure the environment variables in your Cursor config are properly formatted as JSON
- Verify that the container is running before Cursor tries to connect

### Authentication Issues
- Verify your `ATLASSIAN_EMAIL` is correct in the Cursor MCP configuration
- Ensure your `ATLASSIAN_TOKEN` is valid and hasn't expired
- Check that all environment variables are properly set in the `env` section of your Cursor MCP config
- Check that your `ATLASSIAN_DOMAIN` matches your Atlassian instance

### Permission Issues
- Make sure your Atlassian user has permission to view the projects/issues/pages you're trying to access
- Some organizations restrict API access
- Confluence pages may have specific space permissions

### Connection Issues
- Verify your Atlassian instance URL is accessible
- Check if your organization uses any special authentication or VPN requirements
- Ensure both Jira and Confluence are enabled for your instance

### Page ID vs Page Title
- Confluence pages are accessed by their numeric ID, not their title
- You can find the page ID in the URL when viewing a page, or by searching first

## Future Enhancements

Planned features for future versions:

### Jira
- 📝 **Create Issues**: Add new tickets to Jira
- ✏️ **Update Issues**: Modify existing tickets
- 🔄 **Transition Issues**: Change issue status (e.g., mark as Done)
- 💬 **Comments**: Add and read comments on issues
- 📎 **Attachments**: Handle file attachments

### Confluence
- 📝 **Create Pages**: Add new pages to Confluence
- ✏️ **Update Pages**: Modify existing page content
- 💬 **Comments**: Add and read page comments
- 📎 **Attachments**: Handle file attachments
- 🔍 **Advanced Search**: More sophisticated content search

### General
- 🏷️ **Labels and Components**: Manage metadata
- 📊 **Analytics**: Usage statistics and insights
- 🔄 **Sync**: Cross-platform content synchronization

## Security Notes

- Never commit your API token to version control
- Use environment variables or secure secret management
- API tokens should be rotated regularly
- Consider using application-specific tokens with minimal required permissions
- Be aware of rate limits on Atlassian APIs

## Contributing

Feel free to submit issues and pull requests to improve this MCP server! 