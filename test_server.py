import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Server URL
BASE_URL = "http://localhost:8000"

# Get API key from environment
API_KEY = os.getenv("OPENROUTER_API_KEY")

def test_search():
    """Test the search endpoint"""
    print("Testing /search endpoint...")
    response = requests.post(
        f"{BASE_URL}/search",
        json={
            "topic": "виды королевских пингвинов",
            "limit": 5,
            "include_images": True
        }
    )
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_evaluate():
    """Test the evaluate endpoint with API key"""
    print("\nTesting /evaluate endpoint...")
    article = {
        "title": "King Penguin",
        "snippet": "The king penguin (Aptenodytes patagonicus) is the second largest species of penguin, smaller, but somewhat similar in appearance to the emperor penguin.",
        "url": "https://en.wikipedia.org/wiki/King_penguin"
    }
    response = requests.post(
        f"{BASE_URL}/evaluate",
        json={
            "article": article,
            "topic": "виды королевских пингвинов",
            "api_key": API_KEY
        }
    )
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_analyze():
    """Test the analyze endpoint"""
    print("\nTesting /analyze endpoint...")
    articles = [
        {
            "title": "King Penguin",
            "snippet": "The king penguin (Aptenodytes patagonicus) is the second largest species of penguin...",
            "url": "https://en.wikipedia.org/wiki/King_penguin"
        },
        {
            "title": "Emperor Penguin",
            "snippet": "The emperor penguin (Aptenodytes forsteri) is the tallest and heaviest of all living penguin species...",
            "url": "https://en.wikipedia.org/wiki/Emperor_penguin"
        }
    ]
    response = requests.post(
        f"{BASE_URL}/analyze",
        json={
            "articles": articles,
            "topic": "виды королевских пингвинов"
        }
    )
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("Starting server tests...")
    test_search()
    test_evaluate()
    test_analyze() 