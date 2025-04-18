# Wikipedia Search MCP Server

A GitMCP server for searching and analyzing Wikipedia articles. This server provides a powerful interface for searching, evaluating, and analyzing Wikipedia content through various AI models.

## MCP Server URL

`https://gitmcp.io/simakovvv/wiki-mcp-server`

## Integration Examples

### Cursor
Update your `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "wiki-mcp-server Docs": {
      "url": "https://gitmcp.io/simakovvv/wiki-mcp-server"
    }
  }
}
```

### Claude Desktop
Update your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "wiki-mcp-server Docs": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://gitmcp.io/simakovvv/wiki-mcp-server"
      ]
    }
  }
}
```

### Windsurf
Update your `~/.codeium/windsurf/mcp_config.json`:
```json
{
  "mcpServers": {
    "wiki-mcp-server Docs": {
      "serverUrl": "https://gitmcp.io/simakovvv/wiki-mcp-server"
    }
  }
}
```

### VSCode
Update your `.vscode/mcp.json`:
```json
{
  "servers": {
    "wiki-mcp-server Docs": {
      "type": "sse",
      "url": "https://gitmcp.io/simakovvv/wiki-mcp-server"
    }
  }
}
```

### Cline
Update your `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`:
```json
{
  "mcpServers": {
    "wiki-mcp-server Docs": {
      "url": "https://gitmcp.io/simakovvv/wiki-mcp-server",
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Highlight AI
1. Open Highlight AI and click the plugins icon (@ symbol) in the sidebar
2. Click **Installed Plugins** at the top of the sidebar
3. Select **Custom Plugin**
4. Click **Add a plugin using a custom SSE URL**
5. Enter plugin name: `wiki-mcp-server Docs`
6. Enter SSE URL: `https://gitmcp.io/simakovvv/wiki-mcp-server`

## API Endpoints

### Search Articles
- **Endpoint**: `/search`
- **Method**: POST
- **SSE**: Enabled
- **Input**:
  ```json
  {
    "topic": "string",
    "max_results": "integer",
    "include_images": "boolean",
    "model": "string"
  }
  ```
- **Output**: Stream of search results with article metadata

### Evaluate Article
- **Endpoint**: `/evaluate`
- **Method**: POST
- **SSE**: Disabled
- **Input**:
  ```json
  {
    "article": {
      "title": "string",
      "content": "string",
      "url": "string"
    },
    "model": "string"
  }
  ```
- **Output**: Article evaluation with relevance score and key points

### Analyze Article
- **Endpoint**: `/analyze`
- **Method**: POST
- **SSE**: Disabled
- **Input**:
  ```json
  {
    "article": {
      "title": "string",
      "content": "string",
      "url": "string"
    },
    "model": "string"
  }
  ```
- **Output**: Detailed article analysis with summary and key insights

### Get Statistics
- **Endpoint**: `/stats`
- **Method**: GET
- **SSE**: Disabled
- **Output**: Server usage statistics and performance metrics

## Available Models

The server supports the following AI models:
- gpt-3.5-turbo (default)
- gpt-4
- claude-2
- mistral-7b

## Environment Variables

Create a `.env` file with the following variables:
```env
OPENROUTER_API_KEY=your_api_key_here
HOST=0.0.0.0
PORT=8000
DEBUG=false
LOG_LEVEL=INFO
LOG_FILE=server.log
CACHE_TTL=3600
MAX_CACHE_SIZE=1000
RATE_LIMIT=100
RATE_LIMIT_WINDOW=60
```

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## License

MIT License 