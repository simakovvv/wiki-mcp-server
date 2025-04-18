# Wikipedia MCP Server

A GitMCP server for searching and analyzing Wikipedia articles using various AI models. The server provides real-time search capabilities with image support and article analysis.

## Server URL

`https://gitmcp.io/simakovvv/wiki-mcp-server`

## API Reference

### Search Articles

Search for Wikipedia articles with optional image support.

**Endpoint**: `/search`
**Method**: POST
**SSE**: Enabled (Server-Sent Events)

**Request Body**:
```json
{
  "topic": "string",         // Search query
  "max_results": 5,         // Optional: Number of results (default: 5)
  "include_images": true,   // Optional: Include images (default: false)
  "model": "gpt-3.5-turbo" // Optional: AI model to use
}
```

**Response Stream**:
1. Initial Response:
```json
{
  "status": "started"
}
```

2. Processing Updates (per article):
```json
{
  "status": "processing",
  "article": {
    "title": "Article Title",
    "url": "https://en.wikipedia.org/wiki/Article_Title",
    "snippet": "Article snippet text...",
    "relevance_score": 0.95,
    "images": [
      {
        "url": "https://upload.wikimedia.org/...",
        "caption": "Image description",
        "width": 800,
        "height": 600
      }
    ]
  }
}
```

3. Completion:
```json
{
  "status": "completed"
}
```

### Evaluate Article

Evaluate article relevance using AI models.

**Endpoint**: `/evaluate`
**Method**: POST
**SSE**: Disabled

**Request Body**:
```json
{
  "article": {
    "title": "string",
    "snippet": "string",
    "url": "string"
  },
  "model": "gpt-3.5-turbo" // Optional: AI model to use
}
```

**Response**:
```json
{
  "relevance": "Detailed relevance analysis...",
  "article": {
    "title": "Article Title",
    "snippet": "Article content...",
    "url": "Article URL"
  }
}
```

### Analyze Article

Perform detailed article analysis using AI models.

**Endpoint**: `/analyze`
**Method**: POST
**SSE**: Disabled

**Request Body**:
```json
{
  "article": {
    "title": "string",
    "snippet": "string",
    "url": "string"
  },
  "model": "gpt-3.5-turbo" // Optional: AI model to use
}
```

**Response**:
```json
{
  "analysis": "Detailed article analysis...",
  "article": {
    "title": "Article Title",
    "snippet": "Article content...",
    "url": "Article URL"
  }
}
```

### Server Statistics

Get server usage statistics.

**Endpoint**: `/stats`
**Method**: GET
**SSE**: Disabled

**Response**:
```json
{
  "total_requests": 100,
  "endpoints": {
    "search": 50,
    "evaluate": 30,
    "analyze": 20
  },
  "models": {
    "gpt-3.5-turbo": 80,
    "gpt-4": 15,
    "claude-2": 5
  },
  "errors": 2,
  "last_update": "2024-04-18T12:00:00Z"
}
```

## Integration with Chat Bots

### Available Commands

1. Search Articles:
```bash
@wiki-mcp-server search "your search query" --max-results 5 --include-images true --model gpt-3.5-turbo
```

2. Evaluate Article:
```bash
@wiki-mcp-server evaluate --article '{"title": "Article Title", "content": "Article content...", "url": "Article URL"}' --model gpt-3.5-turbo
```

3. Analyze Article:
```bash
@wiki-mcp-server analyze --article '{"title": "Article Title", "content": "Article content...", "url": "Article URL"}' --model gpt-3.5-turbo
```

4. Get Statistics:
```bash
@wiki-mcp-server stats
```

## Integration Examples

### Cursor
Update your `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "wiki-mcp-server": {
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
    "wiki-mcp-server": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://gitmcp.io/simakovvv/wiki-mcp-server"
      ]
    }
  }
}
```

### VSCode
Update your `.vscode/mcp.json`:
```json
{
  "servers": {
    "wiki-mcp-server": {
      "type": "sse",
      "url": "https://gitmcp.io/simakovvv/wiki-mcp-server"
    }
  }
}
```

## Available Models

The server supports the following AI models:
- gpt-3.5-turbo (default)
- gpt-4
- claude-2
- mistral-7b

## Environment Variables

Required environment variables:
```env
OPENROUTER_API_KEY=your_api_key_here
```

Optional configuration:
```env
SERVER_TIMEOUT=300        # Server timeout in seconds
KEEPALIVE_TIMEOUT=60     # Keep-alive timeout for SSE
MAX_CONNECTIONS=100      # Maximum concurrent connections
```

## Error Handling

All endpoints return standard HTTP status codes:
- 200: Success
- 400: Bad Request (invalid parameters)
- 401: Unauthorized (invalid API key)
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error
- 504: Gateway Timeout

Error responses include a detailed message:
```json
{
  "error": "Error description"
}
```

## Rate Limiting

- Default: 100 requests per minute
- Configurable via `RATE_LIMIT` environment variable
- Rate limit window: 60 seconds

## License

MIT License 