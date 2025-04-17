# Wikipedia Search MCP

This MCP server provides functionality for searching and analyzing Wikipedia articles using semantic similarity and LLM-based relevance evaluation.

## Features

- Search Wikipedia articles by topic
- Evaluate article relevance using OpenRouter's LLM
- Semantic similarity analysis using spaCy
- Batch processing of articles

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   export OPENROUTER_API_KEY=your_api_key_here
   ```

## Deployment on GitMCP

1. Create an account on [GitMCP](https://gitmcp.io/)
2. Fork this repository
3. Update the `OPENROUTER_API_KEY` in `mcp.json` with your actual API key
4. Push your changes to your fork
5. Follow the deployment instructions on GitMCP

## API Usage

The MCP server exposes the following endpoints:

- `POST /search`: Search for Wikipedia articles by topic
- `POST /evaluate`: Evaluate article relevance using LLM
- `POST /analyze`: Perform semantic analysis of articles

## License

MIT License 