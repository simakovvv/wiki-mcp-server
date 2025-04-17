import requests
import json
from typing import Dict, Any

class MCPTester:
    def __init__(self, base_url: str = "https://gitmcp.io/simakovvv/wiki-mcp-server"):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def test_search(self) -> Dict[str, Any]:
        """Test the search endpoint"""
        payload = {
            "topic": "king penguin species",
            "limit": 5,
            "include_images": True,
            "model": "gpt-3.5-turbo"
        }
        response = requests.post(
            f"{self.base_url}/api/v1/search",
            headers=self.headers,
            json=payload
        )
        return response.json()

    def test_evaluate(self) -> Dict[str, Any]:
        """Test the evaluate endpoint"""
        payload = {
            "article": {
                "title": "King Penguin",
                "snippet": "The king penguin (Aptenodytes patagonicus) is the second largest species of penguin...",
                "url": "https://en.wikipedia.org/wiki/King_penguin"
            },
            "topic": "king penguin species",
            "model": "gpt-3.5-turbo"
        }
        response = requests.post(
            f"{self.base_url}/api/v1/evaluate",
            headers=self.headers,
            json=payload
        )
        return response.json()

    def test_analyze(self) -> Dict[str, Any]:
        """Test the analyze endpoint"""
        payload = {
            "articles": [
                {
                    "title": "King Penguin",
                    "snippet": "The king penguin (Aptenodytes patagonicus) is the second largest species of penguin...",
                    "url": "https://en.wikipedia.org/wiki/King_penguin"
                }
            ],
            "topic": "king penguin species",
            "model": "gpt-3.5-turbo"
        }
        response = requests.post(
            f"{self.base_url}/api/v1/analyze",
            headers=self.headers,
            json=payload
        )
        return response.json()

    def test_stats(self) -> Dict[str, Any]:
        """Test the stats endpoint"""
        response = requests.get(
            f"{self.base_url}/api/v1/stats",
            headers=self.headers
        )
        return response.json()

    def run_all_tests(self):
        """Run all tests and print results"""
        print("Running MCP Server Tests...\n")
        
        print("1. Testing Search Endpoint:")
        search_result = self.test_search()
        print(json.dumps(search_result, indent=2))
        
        print("\n2. Testing Evaluate Endpoint:")
        evaluate_result = self.test_evaluate()
        print(json.dumps(evaluate_result, indent=2))
        
        print("\n3. Testing Analyze Endpoint:")
        analyze_result = self.test_analyze()
        print(json.dumps(analyze_result, indent=2))
        
        print("\n4. Testing Stats Endpoint:")
        stats_result = self.test_stats()
        print(json.dumps(stats_result, indent=2))

if __name__ == "__main__":
    tester = MCPTester()
    tester.run_all_tests() 