import sys
import json
import requests
import re
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from datetime import datetime
import uuid
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
import asyncio
from starlette.background import BackgroundTask

# Load environment variables
load_dotenv()

# Initialize NLTK and spaCy
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt_tab')
nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()

# Configuration
MAX_ARTICLES_PER_PHRASE = 5
REQUEST_DELAY = 1
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
SERVER_TIMEOUT = int(os.getenv("SERVER_TIMEOUT", "300"))
KEEPALIVE_TIMEOUT = int(os.getenv("KEEPALIVE_TIMEOUT", "60"))
MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS", "100"))

app = FastAPI(
    title="Wikipedia MCP Server",
    description="MCP server for searching and analyzing Wikipedia articles",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add timeout middleware
@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    try:
        return await asyncio.wait_for(call_next(request), timeout=SERVER_TIMEOUT)
    except asyncio.TimeoutError:
        return JSONResponse(
            status_code=504,
            content={"detail": "Request timeout"}
        )

# Keep-alive middleware
@app.middleware("http")
async def add_keep_alive(request: Request, call_next):
    response = await call_next(request)
    if request.url.path == "/search":
        response.headers["Connection"] = "keep-alive"
        response.headers["Keep-Alive"] = f"timeout={KEEPALIVE_TIMEOUT}"
    return response

# Models
class Article(BaseModel):
    title: str
    snippet: str
    url: str

class SearchRequest(BaseModel):
    topic: str
    limit: int = 5
    model: str = "gpt-3.5-turbo"

class EvaluateRequest(BaseModel):
    article: Article
    model: str = "gpt-3.5-turbo"

class AnalyzeRequest(BaseModel):
    article: Article
    model: str = "gpt-3.5-turbo"

# Statistics
STATS_FILE = "server_stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {
        "total_requests": 0,
        "endpoints": {},
        "models": {},
        "errors": 0,
        "last_update": time.time()
    }

def save_stats(stats):
    stats["last_update"] = time.time()
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

def update_stats(endpoint, model, error=False):
    stats = load_stats()
    stats["total_requests"] += 1
    
    if endpoint not in stats["endpoints"]:
        stats["endpoints"][endpoint] = 0
    stats["endpoints"][endpoint] += 1
    
    if model not in stats["models"]:
        stats["models"][model] = 0
    stats["models"][model] += 1
    
    if error:
        stats["errors"] += 1
    
    save_stats(stats)

class WikipediaMCPServer:
    def __init__(self):
        self.tools = {
            "search_articles": {
                "name": "search_articles",
                "description": "Search for Wikipedia articles by phrase",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search phrase"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            },
            "get_article": {
                "name": "get_article",
                "description": "Get Wikipedia article by title",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Article title"
                        }
                    },
                    "required": ["title"]
                }
            },
            "evaluate_relevance": {
                "name": "evaluate_relevance",
                "description": "Evaluate article relevance to a search phrase",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "article_title": {
                            "type": "string",
                            "description": "Article title"
                        },
                        "article_snippet": {
                            "type": "string",
                            "description": "Article snippet"
                        },
                        "search_phrase": {
                            "type": "string",
                            "description": "Search phrase"
                        }
                    },
                    "required": ["article_title", "article_snippet", "search_phrase"]
                }
            }
        }
        
        self.resources = {
            "article": {
                "pattern": "wiki://{title}",
                "description": "Access Wikipedia article by title"
            },
            "search": {
                "pattern": "wiki://search/{query}",
                "description": "Search Wikipedia articles"
            }
        }

    def handle_request(self, request):
        """
        Handle MCP request
        """
        try:
            if request["type"] == "get_tools":
                return self.get_tools()
            elif request["type"] == "get_resources":
                return self.get_resources()
            elif request["type"] == "call_tool":
                return self.call_tool(request["name"], request["parameters"])
            elif request["type"] == "get_resource":
                return self.get_resource(request["url"])
            else:
                return {"error": f"Unknown request type: {request['type']}"}
        except Exception as e:
            return {"error": str(e)}

    def get_tools(self):
        """
        Return available tools
        """
        return {"tools": list(self.tools.values())}

    def get_resources(self):
        """
        Return available resources
        """
        return {"resources": list(self.resources.values())}

    def call_tool(self, name, parameters):
        """
        Call specific tool with parameters
        """
        if name == "search_articles":
            return self.search_articles(**parameters)
        elif name == "get_article":
            return self.get_article(**parameters)
        elif name == "evaluate_relevance":
            return self.evaluate_relevance(**parameters)
        else:
            return {"error": f"Unknown tool: {name}"}

    def get_resource(self, url):
        """
        Get resource by URL
        """
        if url.startswith("wiki://"):
            path = url[7:]
            if path.startswith("search/"):
                query = path[7:]
                return self.search_articles(query=query)
            else:
                return self.get_article(title=path)
        return {"error": f"Invalid resource URL: {url}"}

    def search_articles(self, query, limit=5):
        """
        Search Wikipedia articles
        """
        url = "https://en.wikipedia.org/w/api.php"
        
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
            "format": "json",
            "srprop": "snippet|titlesnippet|categorysnippet",
            "srwhat": "nearmatch",
            "srnamespace": 0,
            "srredirects": "exclude"
        }
        
        time.sleep(REQUEST_DELAY)
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get("query", {}).get("search", [])
        
        return [
            {
                "title": article.get("title", ""),
                "url": f"https://en.wikipedia.org/wiki/{article.get('title', '').replace(' ', '_')}",
                "snippet": article.get("snippet", ""),
                "relevance_score": self.evaluate_relevance_llm(article, query)
            }
            for article in results
        ]

    def get_article(self, title):
        """
        Get Wikipedia article by title
        """
        url = "https://en.wikipedia.org/w/api.php"
        
        params = {
            "action": "query",
            "prop": "extracts|info",
            "titles": title,
            "format": "json",
            "explaintext": True,
            "inprop": "url"
        }
        
        time.sleep(REQUEST_DELAY)
        response = requests.get(url, params=params)
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        
        if not pages:
            return {"error": "Article not found"}
        
        page = list(pages.values())[0]
        return {
            "title": page.get("title", ""),
            "url": page.get("fullurl", ""),
            "extract": page.get("extract", ""),
            "lastmodified": page.get("touched", "")
        }

    def evaluate_relevance(self, article_title, article_snippet, search_phrase):
        """
        Evaluate article relevance
        """
        return {
            "score": self.evaluate_relevance_llm(
                {"title": article_title, "snippet": article_snippet},
                search_phrase
            )
        }

    def evaluate_relevance_llm(self, article, search_phrase):
        """
        Evaluate article relevance using OpenRouter
        """
        article_title = article.get("title", "")
        article_snippet = article.get("snippet", "")
        
        prompt = f"""
        You are an expert evaluator tasked with precisely assessing the relevance of a Wikipedia article to a given search phrase.

        ### Search Phrase:
        {search_phrase}

        ### Wikipedia Article:
        - **Title:** {article_title}
        - **Snippet:** {article_snippet}

        ### Strict Evaluation Criteria:
        - SCORE 0.9-1.0: Article is exactly about the search phrase, highly specific, and directly matches.
        - SCORE 0.7-0.8: Article strongly related but broader or less specific.
        - SCORE 0.4-0.6: Moderately related, mentions key concepts briefly.
        - SCORE 0.1-0.3: Loosely related, minimal relevance.
        - SCORE 0.0: Not relevant or off-topic.

        ### Your Task:
        Provide the exact numeric SCORE according to the criteria above, followed by a concise REASON (one sentence).

        ### Output (strictly follow this format):
        SCORE: [0.0-1.0]
        REASON: [one concise sentence]
        """
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "mistralai/mistral-7b-instruct",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            
            content = response.json()["choices"][0]["message"]["content"]
            score_match = re.search(r"SCORE:\s*([0-9.]+)", content)
            if score_match:
                return float(score_match.group(1))
            return 0.0
                
        except Exception as e:
            print(f"Error evaluating relevance: {str(e)}")
            return 0.0

@app.get("/search")
async def search(topic: str, limit: int = 5, model: str = "gpt-3.5-turbo"):
    async def generate():
        try:
            # Send initial response
            yield "data: " + json.dumps({"status": "started"}) + "\n\n"
            await asyncio.sleep(0.1)  # Small delay for connection establishment
            
            # Keep-alive ping
            async def send_ping():
                while True:
                    await asyncio.sleep(KEEPALIVE_TIMEOUT / 2)
                    yield "data: " + json.dumps({"status": "ping"}) + "\n\n"
            
            # Start keep-alive task
            asyncio.create_task(send_ping())
            
            # Process search
            update_stats("search", model)
            server = WikipediaMCPServer()
            articles = await server.search_articles(topic, limit)
            
            # Send results
            for article in articles:
                yield "data: " + json.dumps({"status": "processing", "article": article}) + "\n\n"
                await asyncio.sleep(0.1)  # Prevent flooding
            
            # Send completion
            yield "data: " + json.dumps({"status": "completed"}) + "\n\n"
            
        except Exception as e:
            update_stats("search", model, error=True)
            yield "data: " + json.dumps({"status": "error", "message": str(e)}) + "\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Transfer-Encoding": "chunked"
        }
    )

@app.post("/evaluate")
async def evaluate(request: EvaluateRequest):
    try:
        update_stats("evaluate", request.model)
        
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        prompt = f"Evaluate the relevance of this article to the topic: {request.article.title}\n\n{request.article.snippet}"
        data = {
            "model": request.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to evaluate article")
        
        return {
            "relevance": response.json()["choices"][0]["message"]["content"],
            "article": request.article
        }
        
    except Exception as e:
        update_stats("evaluate", request.model, error=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        update_stats("analyze", request.model)
        
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        prompt = f"Analyze this article and provide key insights: {request.article.title}\n\n{request.article.snippet}"
        data = {
            "model": request.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to analyze article")
        
        return {
            "analysis": response.json()["choices"][0]["message"]["content"],
            "article": request.article
        }
        
    except Exception as e:
        update_stats("analyze", request.model, error=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def stats():
    return load_stats()

def main():
    """
    Main function to run the MCP server
    """
    server = WikipediaMCPServer()
    
    # Read from stdin and write to stdout
    while True:
        try:
            # Read request
            line = sys.stdin.readline()
            if not line:
                break
                
            request = json.loads(line)
            
            # Process request
            response = server.handle_request(request)
            
            # Write response
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            
        except Exception as e:
            sys.stderr.write(f"Error: {str(e)}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 