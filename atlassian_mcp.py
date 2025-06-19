#!/usr/bin/env python3
"""
Atlassian Cloud MCP Server

A Model Context Protocol server for interacting with Atlassian Cloud services.
Provides tools to read Jira tickets and Confluence pages.
"""

import os
import json
import asyncio
import base64
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
import aiohttp
from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.server.stdio
import mcp.types as types


class AtlassianClient:
    """Atlassian Cloud API client for Jira and Confluence"""
    
    def __init__(self, email: str, token: str, domain: str):
        self.email = email
        self.token = token
        self.domain = domain
        self.jira_base_url = f"https://{domain}.atlassian.net/rest/api/3"
        self.confluence_base_url = f"https://{domain}.atlassian.net/wiki/rest/api"
        
        # Create basic auth header
        credentials = f"{email}:{token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    # Jira Methods
    async def get_jira_issue(self, issue_key: str) -> Dict[str, Any]:
        """Get a specific Jira issue by key"""
        url = f"{self.jira_base_url}/issue/{issue_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    raise Exception(f"Issue {issue_key} not found")
                elif response.status == 401:
                    raise Exception("Authentication failed. Check your ATLASSIAN_EMAIL and ATLASSIAN_TOKEN")
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get issue {issue_key}: {response.status} - {error_text}")
    
    async def search_jira_issues(self, jql: str, max_results: int = 50) -> Dict[str, Any]:
        """Search for issues using JQL"""
        url = f"{self.jira_base_url}/search"
        
        payload = {
            "jql": jql,
            "maxResults": max_results,
            "fields": ["summary", "status", "assignee", "reporter", "created", "updated", "priority", "issuetype"]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 400:
                    error_text = await response.text()
                    raise Exception(f"Invalid JQL query: {error_text}")
                elif response.status == 401:
                    raise Exception("Authentication failed. Check your ATLASSIAN_EMAIL and ATLASSIAN_TOKEN")
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to search issues: {response.status} - {error_text}")
    
    async def get_jira_project_info(self, project_key: str) -> Dict[str, Any]:
        """Get information about a Jira project"""
        url = f"{self.jira_base_url}/project/{project_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    raise Exception(f"Project {project_key} not found")
                elif response.status == 401:
                    raise Exception("Authentication failed. Check your ATLASSIAN_EMAIL and ATLASSIAN_TOKEN")
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get project {project_key}: {response.status} - {error_text}")
    
    # Confluence Methods
    async def get_confluence_page(self, page_id: str) -> Dict[str, Any]:
        """Get a specific Confluence page by ID"""
        url = f"{self.confluence_base_url}/content/{page_id}"
        
        # Expand body.storage to get the full content
        params = {
            "expand": "body.storage,version,space,ancestors"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    raise Exception(f"Confluence page {page_id} not found")
                elif response.status == 401:
                    raise Exception("Authentication failed. Check your ATLASSIAN_EMAIL and ATLASSIAN_TOKEN")
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get page {page_id}: {response.status} - {error_text}")
    
    async def search_confluence_pages(self, query: str, max_results: int = 25) -> Dict[str, Any]:
        """Search for Confluence pages using CQL (Confluence Query Language)"""
        url = f"{self.confluence_base_url}/content/search"
        
        params = {
            "cql": query,
            "limit": max_results,
            "expand": "space,version"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 400:
                    error_text = await response.text()
                    raise Exception(f"Invalid CQL query: {error_text}")
                elif response.status == 401:
                    raise Exception("Authentication failed. Check your ATLASSIAN_EMAIL and ATLASSIAN_TOKEN")
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to search pages: {response.status} - {error_text}")
    
    async def get_confluence_space(self, space_key: str) -> Dict[str, Any]:
        """Get information about a Confluence space"""
        url = f"{self.confluence_base_url}/space/{space_key}"
        
        params = {
            "expand": "description.plain,homepage"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    raise Exception(f"Confluence space {space_key} not found")
                elif response.status == 401:
                    raise Exception("Authentication failed. Check your ATLASSIAN_EMAIL and ATLASSIAN_TOKEN")
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get space {space_key}: {response.status} - {error_text}")


def format_jira_issue_response(issue_data: Dict[str, Any]) -> str:
    """Format Jira issue data for readable response"""
    fields = issue_data.get("fields", {})
    
    # Extract key information
    key = issue_data.get("key", "Unknown")
    summary = fields.get("summary", "No summary")
    status = fields.get("status", {}).get("name", "Unknown")
    issue_type = fields.get("issuetype", {}).get("name", "Unknown")
    priority = fields.get("priority", {}).get("name", "Unknown")
    
    # Assignee and reporter
    assignee = fields.get("assignee")
    assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
    
    reporter = fields.get("reporter")
    reporter_name = reporter.get("displayName", "Unknown") if reporter else "Unknown"
    
    # Dates
    created = fields.get("created", "Unknown")
    updated = fields.get("updated", "Unknown")
    
    # Description
    description = fields.get("description", {})
    desc_text = "No description"
    if description and description.get("content"):
        # Simple text extraction from Atlassian Document Format
        desc_text = extract_text_from_adf(description)
    
    # Get the base URL from the self field
    self_url = issue_data.get("self", "")
    if self_url:
        base_url = self_url.split("/rest/")[0]
        issue_url = f"{base_url}/browse/{key}"
    else:
        issue_url = f"https://unknown.atlassian.net/browse/{key}"
    
    response = f"""**Jira Issue: {key}**

**Summary:** {summary}
**Status:** {status}
**Type:** {issue_type}
**Priority:** {priority}
**Assignee:** {assignee_name}
**Reporter:** {reporter_name}
**Created:** {created}
**Updated:** {updated}

**Description:**
{desc_text}

**Issue URL:** {issue_url}
"""
    
    return response


def format_confluence_page_response(page_data: Dict[str, Any]) -> str:
    """Format Confluence page data for readable response"""
    page_id = page_data.get("id", "Unknown")
    title = page_data.get("title", "No title")
    space_name = page_data.get("space", {}).get("name", "Unknown")
    space_key = page_data.get("space", {}).get("key", "Unknown")
    
    # Version info
    version = page_data.get("version", {})
    version_number = version.get("number", "Unknown")
    last_updated = version.get("when", "Unknown")
    updated_by = version.get("by", {}).get("displayName", "Unknown")
    
    # Content
    body = page_data.get("body", {}).get("storage", {})
    content = body.get("value", "No content")
    
    # Clean up HTML content for better readability
    content = clean_confluence_html(content)
    
    # Get the page URL
    base_url = page_data.get("_links", {}).get("base", "")
    web_ui = page_data.get("_links", {}).get("webui", "")
    if base_url and web_ui:
        page_url = f"{base_url}{web_ui}"
    else:
        page_url = f"https://unknown.atlassian.net/wiki/spaces/{space_key}/pages/{page_id}"
    
    response = f"""**Confluence Page: {title}**

**Space:** {space_name} ({space_key})
**Page ID:** {page_id}
**Version:** {version_number}
**Last Updated:** {last_updated} by {updated_by}

**Content:**
{content}

**Page URL:** {page_url}
"""
    
    return response


def clean_confluence_html(html_content: str) -> str:
    """Clean up Confluence HTML content for better readability"""
    import re
    
    # Remove common HTML tags but keep the content
    html_content = re.sub(r'<ac:structured-macro[^>]*>.*?</ac:structured-macro>', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<ac:parameter[^>]*>.*?</ac:parameter>', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'</?p>', '\n\n', html_content)
    html_content = re.sub(r'</?div[^>]*>', '\n', html_content)
    html_content = re.sub(r'</?span[^>]*>', '', html_content)
    html_content = re.sub(r'<br\s*/?>', '\n', html_content)
    html_content = re.sub(r'</?strong>', '**', html_content)
    html_content = re.sub(r'</?em>', '*', html_content)
    html_content = re.sub(r'</?h[1-6][^>]*>', '\n## ', html_content)
    html_content = re.sub(r'</?ul>', '\n', html_content)
    html_content = re.sub(r'</?ol>', '\n', html_content)
    html_content = re.sub(r'<li>', '• ', html_content)
    html_content = re.sub(r'</li>', '\n', html_content)
    html_content = re.sub(r'<[^>]+>', '', html_content)  # Remove any remaining HTML tags
    
    # Clean up excessive whitespace
    html_content = re.sub(r'\n\s*\n\s*\n', '\n\n', html_content)
    html_content = html_content.strip()
    
    return html_content


def extract_text_from_adf(adf_content: Dict[str, Any]) -> str:
    """Extract plain text from Atlassian Document Format"""
    def extract_text(node):
        if isinstance(node, dict):
            if node.get("type") == "text":
                return node.get("text", "")
            elif "content" in node:
                return "".join(extract_text(child) for child in node["content"])
            else:
                return ""
        elif isinstance(node, list):
            return "".join(extract_text(item) for item in node)
        else:
            return str(node) if node else ""
    
    return extract_text(adf_content).strip()


def format_jira_search_results(search_data: Dict[str, Any]) -> str:
    """Format Jira search results for readable response"""
    issues = search_data.get("issues", [])
    total = search_data.get("total", 0)
    
    if not issues:
        return "No issues found matching the search criteria."
    
    response = f"**Found {len(issues)} of {total} Jira issues:**\n\n"
    
    for issue in issues:
        fields = issue.get("fields", {})
        key = issue.get("key", "Unknown")
        summary = fields.get("summary", "No summary")
        status = fields.get("status", {}).get("name", "Unknown")
        assignee = fields.get("assignee")
        assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
        
        response += f"• **{key}**: {summary}\n"
        response += f"  Status: {status} | Assignee: {assignee_name}\n\n"
    
    return response


def format_confluence_search_results(search_data: Dict[str, Any]) -> str:
    """Format Confluence search results for readable response"""
    results = search_data.get("results", [])
    
    if not results:
        return "No Confluence pages found matching the search criteria."
    
    response = f"**Found {len(results)} Confluence pages:**\n\n"
    
    for page in results:
        page_id = page.get("id", "Unknown")
        title = page.get("title", "No title")
        space_name = page.get("space", {}).get("name", "Unknown")
        space_key = page.get("space", {}).get("key", "Unknown")
        
        response += f"• **{title}** (ID: {page_id})\n"
        response += f"  Space: {space_name} ({space_key})\n\n"
    
    return response


# Initialize the MCP server
server = Server("atlassian-mcp")

# Global Atlassian client instance
atlassian_client: Optional[AtlassianClient] = None


def initialize_atlassian_client():
    """Initialize the Atlassian client with environment variables"""
    global atlassian_client
    
    email = os.getenv("ATLASSIAN_EMAIL")
    token = os.getenv("ATLASSIAN_TOKEN")
    domain = os.getenv("ATLASSIAN_DOMAIN")
    
    if not email:
        raise ValueError("ATLASSIAN_EMAIL environment variable is required")
    if not token:
        raise ValueError("ATLASSIAN_TOKEN environment variable is required")
    if not domain:
        raise ValueError("ATLASSIAN_DOMAIN environment variable is required (e.g., 'sixt-cloud')")
    
    atlassian_client = AtlassianClient(email, token, domain)


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools"""
    return [
        # Jira tools
        Tool(
            name="get_jira_issue",
            description="Get detailed information about a specific Jira issue by its key (e.g., PEX-2288)",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {
                        "type": "string",
                        "description": "The Jira issue key (e.g., PEX-2288, PROJ-123)"
                    }
                },
                "required": ["issue_key"]
            }
        ),
        Tool(
            name="search_jira_issues",
            description="Search for Jira issues using JQL (Jira Query Language)",
            inputSchema={
                "type": "object",
                "properties": {
                    "jql": {
                        "type": "string",
                        "description": "JQL query string (e.g., 'project = PEX AND status = \"In Progress\"')"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 50)",
                        "default": 50
                    }
                },
                "required": ["jql"]
            }
        ),
        Tool(
            name="get_jira_project",
            description="Get information about a Jira project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_key": {
                        "type": "string",
                        "description": "The project key (e.g., PEX, PROJ)"
                    }
                },
                "required": ["project_key"]
            }
        ),
        # Confluence tools
        Tool(
            name="get_confluence_page",
            description="Get detailed information and content from a specific Confluence page by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_id": {
                        "type": "string",
                        "description": "The Confluence page ID (e.g., '123456789')"
                    }
                },
                "required": ["page_id"]
            }
        ),
        Tool(
            name="search_confluence_pages",
            description="Search for Confluence pages using CQL (Confluence Query Language)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "CQL query string (e.g., 'space = DEV AND title ~ \"documentation\"')"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 25)",
                        "default": 25
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_confluence_space",
            description="Get information about a Confluence space",
            inputSchema={
                "type": "object",
                "properties": {
                    "space_key": {
                        "type": "string",
                        "description": "The Confluence space key (e.g., DEV, PROJ)"
                    }
                },
                "required": ["space_key"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls"""
    global atlassian_client
    
    if atlassian_client is None:
        try:
            initialize_atlassian_client()
        except ValueError as e:
            return [types.TextContent(type="text", text=f"Configuration error: {str(e)}")]
    
    try:
        # Jira tools
        if name == "get_jira_issue":
            issue_key = arguments.get("issue_key")
            if not issue_key:
                return [types.TextContent(type="text", text="Error: issue_key is required")]
            
            issue_data = await atlassian_client.get_jira_issue(issue_key)
            formatted_response = format_jira_issue_response(issue_data)
            return [types.TextContent(type="text", text=formatted_response)]
        
        elif name == "search_jira_issues":
            jql = arguments.get("jql")
            max_results = arguments.get("max_results", 50)
            
            if not jql:
                return [types.TextContent(type="text", text="Error: jql query is required")]
            
            search_data = await atlassian_client.search_jira_issues(jql, max_results)
            formatted_response = format_jira_search_results(search_data)
            return [types.TextContent(type="text", text=formatted_response)]
        
        elif name == "get_jira_project":
            project_key = arguments.get("project_key")
            if not project_key:
                return [types.TextContent(type="text", text="Error: project_key is required")]
            
            project_data = await atlassian_client.get_jira_project_info(project_key)
            
            response = f"""**Jira Project: {project_data.get('key', 'Unknown')}**

**Name:** {project_data.get('name', 'Unknown')}
**Description:** {project_data.get('description', 'No description')}
**Project Type:** {project_data.get('projectTypeKey', 'Unknown')}
**Lead:** {project_data.get('lead', {}).get('displayName', 'Unknown')}
**URL:** {project_data.get('self', 'Unknown')}
"""
            return [types.TextContent(type="text", text=response)]
        
        # Confluence tools
        elif name == "get_confluence_page":
            page_id = arguments.get("page_id")
            if not page_id:
                return [types.TextContent(type="text", text="Error: page_id is required")]
            
            page_data = await atlassian_client.get_confluence_page(page_id)
            formatted_response = format_confluence_page_response(page_data)
            return [types.TextContent(type="text", text=formatted_response)]
        
        elif name == "search_confluence_pages":
            query = arguments.get("query")
            max_results = arguments.get("max_results", 25)
            
            if not query:
                return [types.TextContent(type="text", text="Error: query is required")]
            
            search_data = await atlassian_client.search_confluence_pages(query, max_results)
            formatted_response = format_confluence_search_results(search_data)
            return [types.TextContent(type="text", text=formatted_response)]
        
        elif name == "get_confluence_space":
            space_key = arguments.get("space_key")
            if not space_key:
                return [types.TextContent(type="text", text="Error: space_key is required")]
            
            space_data = await atlassian_client.get_confluence_space(space_key)
            
            description = space_data.get("description", {})
            desc_text = "No description"
            if description and description.get("plain"):
                desc_text = description["plain"].get("value", "No description")
            
            homepage = space_data.get("homepage", {})
            homepage_title = homepage.get("title", "No homepage") if homepage else "No homepage"
            
            response = f"""**Confluence Space: {space_data.get('key', 'Unknown')}**

**Name:** {space_data.get('name', 'Unknown')}
**Description:** {desc_text}
**Type:** {space_data.get('type', 'Unknown')}
**Homepage:** {homepage_title}
**URL:** {space_data.get('_links', {}).get('webui', 'Unknown')}
"""
            return [types.TextContent(type="text", text=response)]
        
        else:
            return [types.TextContent(type="text", text=f"Error: Unknown tool '{name}'")]
    
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Main function to run the MCP server"""
    # Use stdio transport
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main()) 