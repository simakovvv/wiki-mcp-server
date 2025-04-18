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

## Testing the Server

After integrating the server with your chat bot, you can test it using the following commands:

### 1. Search Test
```bash
@wiki-mcp-server search "king penguin species" --max-results 5 --include-images true --model gpt-3.5-turbo
```
This will search for articles about king penguin species and include images in the results.

### 2. Evaluate Test
```bash
@wiki-mcp-server evaluate --article '{"title": "King Penguin", "content": "King penguins are large penguins...", "url": "https://en.wikipedia.org/wiki/King_penguin"}' --model gpt-3.5-turbo
```
This will evaluate the relevance of the provided article.

### 3. Analyze Test
```bash
@wiki-mcp-server analyze --article '{"title": "King Penguin", "content": "King penguins are large penguins...", "url": "https://en.wikipedia.org/wiki/King_penguin"}' --model gpt-3.5-turbo
```
This will perform a detailed analysis of the provided article.

### 4. Stats Test
```bash
@wiki-mcp-server stats
```
This will retrieve server usage statistics.

### Expected Responses

1. **Search Response**:
```json
{
  "articles": [
    {
      "title": "King Penguin",
      "url": "https://en.wikipedia.org/wiki/King_penguin",
      "summary": "The king penguin is the second largest species of penguin...",
      "relevance_score": 0.95,
      "images": [
        {
          "url": "https://upload.wikimedia.org/...",
          "caption": "King penguins in their natural habitat"
        }
      ]
    }
  ]
}
```

2. **Evaluate Response**:
```json
{
  "relevance_score": 0.95,
  "key_points": [
    "King penguins are the second largest penguin species",
    "They inhabit sub-Antarctic islands",
    "They have a unique breeding cycle"
  ],
  "confidence": 0.9
}
```

3. **Analyze Response**:
```json
{
  "summary": "Detailed analysis of the King Penguin article...",
  "key_insights": [
    "Physical characteristics",
    "Habitat and distribution",
    "Behavior and ecology"
  ],
  "confidence": 0.92
}
```

4. **Stats Response**:
```json
{
  "total_requests": 100,
  "endpoint_usage": {
    "search": 50,
    "evaluate": 30,
    "analyze": 20
  },
  "model_usage": {
    "gpt-3.5-turbo": 80,
    "gpt-4": 15,
    "claude-2": 5
  },
  "errors": 2,
  "last_updated": "2024-04-18T12:00:00Z"
}
```

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