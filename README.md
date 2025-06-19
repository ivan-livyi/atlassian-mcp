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

- Python 3.8+
- Atlassian Cloud instance with both Jira and Confluence
- Atlassian API token

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your Atlassian API Token

1. Go to your Atlassian Cloud instance
2. Navigate to **Account Settings** → **Security** → **API tokens**
3. Click **Create API token**
4. Give it a name (e.g., "MCP Server") and create it
5. Copy the token (you won't be able to see it again)

### 3. Set Environment Variables

Create a `.env` file or set the following environment variables:

```bash
export ATLASSIAN_EMAIL="your.email@company.com"
export ATLASSIAN_TOKEN="your_api_token_here"
export ATLASSIAN_DOMAIN="your-company"  # e.g., "sixt-cloud" for sixt-cloud.atlassian.net
```

**Note**: The `ATLASSIAN_DOMAIN` should be the subdomain part of your Atlassian URL. For example, if your Atlassian is at `https://acme-corp.atlassian.net`, then `ATLASSIAN_DOMAIN` should be `acme-corp`.

### 4. Test the Setup

You can test that the server starts correctly:

```bash
source venv/bin/activate
ATLASSIAN_EMAIL=test@test.com ATLASSIAN_TOKEN=test ATLASSIAN_DOMAIN=test python atlassian_mcp.py &
# The server should start without errors. Use 'pkill -f atlassian_mcp.py' to stop it.
```

## Usage with Cursor

To use this MCP server with Cursor:

### 1. Configure Cursor Settings

Add the following to your Cursor settings (Settings → Extensions → MCP):

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "/Users/ivan/work/jira-mcp/venv/bin/python",
      "args": ["/Users/ivan/work/jira-mcp/atlassian_mcp.py"],
      "env": {
        "ATLASSIAN_EMAIL": "your.email@company.com",
        "ATLASSIAN_TOKEN": "your_api_token_here",
        "ATLASSIAN_DOMAIN": "your-company"
      }
    }
  }
}
```

**Important**: Use the full path to the Python executable in your virtual environment and the full path to your atlassian_mcp.py file.

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

## Query Examples

### JQL Query Examples

Here are some useful JQL queries you can use with the Jira search tool:

```sql
-- All open issues in a project
project = PEX AND status != Done

-- Issues assigned to you
assignee = currentUser()

-- Recently updated issues
updated >= -7d

-- High priority bugs
issuetype = Bug AND priority = High

-- Issues in specific sprint
sprint = "Sprint 42"

-- Issues without assignee
assignee is EMPTY

-- Issues created this week
created >= startOfWeek()

-- Combination example
project = PEX AND assignee = currentUser() AND status = "In Progress"
```

### CQL Query Examples

Here are some useful CQL queries you can use with the Confluence search tool:

```sql
-- All pages in a specific space
space = DEV

-- Pages with specific title
title ~ "documentation"

-- Recently updated pages
lastModified >= now("-7d")

-- Pages by specific author
creator = "john.doe"

-- Pages with specific content
text ~ "deployment"

-- Combination example
space = DEV AND title ~ "API" AND lastModified >= now("-30d")
```

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

### Authentication Issues
- Verify your `ATLASSIAN_EMAIL` is correct
- Ensure your `ATLASSIAN_TOKEN` is valid and hasn't expired
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