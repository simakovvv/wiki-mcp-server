# Wikipedia MCP Server

Server for searching and analyzing Wikipedia articles using AI models.

## API Reference

### Search Articles

**Endpoint**: `/search`
**Method**: POST
**Content-Type**: application/json

Request body:
```json
{
    "topic": "string",
    "limit": 5,  // optional, default: 5
    "model": "gpt-3.5-turbo"  // optional
}
```

Response is a Server-Sent Events (SSE) stream with the following event types:

1. Started event:
```json
{
    "status": "started"
}
```

2. Processing event (sent for each article):
```json
{
    "status": "processing",
    "article": {
        "title": "string",
        "url": "string",
        "snippet": "string",
        "relevance_score": float
    }
}
```

3. Completion event:
```json
{
    "status": "completed"
}
```

4. Error event (if something goes wrong):
```json
{
    "status": "error",
    "error": "error message"
}
```

### Evaluate Article

**Endpoint**: `/evaluate`
**Method**: POST
**Content-Type**: application/json

Request body:
```json
{
    "article": {
        "title": "string",
        "snippet": "string",
        "url": "string"
    },
    "model": "gpt-3.5-turbo"  // optional
}
```

Response:
```json
{
    "relevance": "string",
    "article": {
        "title": "string",
        "snippet": "string",
        "url": "string"
    }
}
```

### Analyze Article

**Endpoint**: `/analyze`
**Method**: POST
**Content-Type**: application/json

Request body:
```json
{
    "article": {
        "title": "string",
        "snippet": "string",
        "url": "string"
    },
    "model": "gpt-3.5-turbo"  // optional
}
```

Response:
```json
{
    "analysis": "string",
    "article": {
        "title": "string",
        "snippet": "string",
        "url": "string"
    }
}
```

### Server Statistics

**Endpoint**: `/stats`
**Method**: GET

Response:
```json
{
    "total_requests": int,
    "endpoints": {
        "search": int,
        "evaluate": int,
        "analyze": int
    },
    "models": {
        "gpt-3.5-turbo": int,
        "gpt-4": int,
        "claude-2": int,
        "mistral-7b": int
    },
    "errors": int,
    "last_update": timestamp
}
```

## Environment Variables

Required:
- `OPENROUTER_API_KEY`: API key for OpenRouter

Optional:
- `SERVER_TIMEOUT`: Server timeout in seconds (default: 300)
- `KEEPALIVE_TIMEOUT`: Keep-alive timeout in seconds (default: 60)
- `MAX_CONNECTIONS`: Maximum number of concurrent connections (default: 100)

## Running the Server

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export OPENROUTER_API_KEY=your_api_key
```

3. Run the server:
```bash
python wiki_mcp_server.py
```

The server will start on `http://localhost:8000`

## Integration Examples

### Python with SSE Client

```python
from sseclient import SSEClient
import json

def search_articles(topic, max_results=3):
    url = "http://localhost:8000/search"
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }
    payload = {
        "topic": topic,
        "limit": max_results,
        "model": "gpt-3.5-turbo"
    }
    
    try:
        response = requests.post(url, 
                               json=payload,
                               headers=headers, 
                               stream=True)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return
            
        client = SSEClient(response)
        for event in client.events():
            try:
                data = json.loads(event.data)
                print(f"Event: {data}")
            except json.JSONDecodeError as e:
                print(f"Error parsing event data: {e}")
                
    except Exception as e:
        print(f"Error: {e}")

# Example usage
search_articles("King penguin", 3)
```

### Curl Example

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"topic": "King penguin", "limit": 3}'
```

## Available Models

The server supports the following AI models:
- gpt-3.5-turbo (default)
- gpt-4
- claude-2
- mistral-7b

## License

MIT License 