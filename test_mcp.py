import requests
import json
from typing import Dict, Any

class MCPTester:
    def __init__(self):
        self.base_url = "https://gitmcp.io/simakovvv/wiki-mcp-server"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def test_search(self) -> Dict[str, Any]:
        """Тестирует эндпоинт /search"""
        url = f"{self.base_url}/search"
        payload = {
            "topic": "king penguin species",
            "limit": 5,
            "model": "gpt-3.5-turbo"
        }
        response = requests.get(url, params=payload, headers=self.headers)
        print(f"Search Status Code: {response.status_code}")
        print(f"Search Headers: {response.headers}")
        print(f"Search Response: {response.text}")
        try:
            return response.json()
        except json.JSONDecodeError as e:
            return {"error": str(e), "raw_response": response.text}

    def test_evaluate(self) -> Dict[str, Any]:
        """Тестирует эндпоинт /evaluate"""
        url = f"{self.base_url}/evaluate"
        payload = {
            "article": {
                "title": "King Penguin",
                "snippet": "The king penguin is the second largest species of penguin.",
                "url": "https://en.wikipedia.org/wiki/King_penguin"
            },
            "model": "gpt-3.5-turbo"
        }
        response = requests.post(url, json=payload, headers=self.headers)
        print(f"Evaluate Status Code: {response.status_code}")
        print(f"Evaluate Headers: {response.headers}")
        print(f"Evaluate Response: {response.text}")
        try:
            return response.json()
        except json.JSONDecodeError as e:
            return {"error": str(e), "raw_response": response.text}

    def test_analyze(self) -> Dict[str, Any]:
        """Тестирует эндпоинт /analyze"""
        url = f"{self.base_url}/analyze"
        payload = {
            "article": {
                "title": "King Penguin",
                "snippet": "The king penguin is the second largest species of penguin.",
                "url": "https://en.wikipedia.org/wiki/King_penguin"
            },
            "model": "gpt-3.5-turbo"
        }
        response = requests.post(url, json=payload, headers=self.headers)
        print(f"Analyze Status Code: {response.status_code}")
        print(f"Analyze Headers: {response.headers}")
        print(f"Analyze Response: {response.text}")
        try:
            return response.json()
        except json.JSONDecodeError as e:
            return {"error": str(e), "raw_response": response.text}

    def test_stats(self) -> Dict[str, Any]:
        """Тестирует эндпоинт /stats"""
        url = f"{self.base_url}/stats"
        response = requests.get(url, headers=self.headers)
        print(f"Stats Status Code: {response.status_code}")
        print(f"Stats Headers: {response.headers}")
        print(f"Stats Response: {response.text}")
        try:
            return response.json()
        except json.JSONDecodeError as e:
            return {"error": str(e), "raw_response": response.text}

    def run_all_tests(self):
        """Запускает все тесты и выводит результаты"""
        print("Running Search Test...")
        search_result = self.test_search()
        print("\nSearch Result:", json.dumps(search_result, indent=2))

        print("\nRunning Evaluate Test...")
        evaluate_result = self.test_evaluate()
        print("\nEvaluate Result:", json.dumps(evaluate_result, indent=2))

        print("\nRunning Analyze Test...")
        analyze_result = self.test_analyze()
        print("\nAnalyze Result:", json.dumps(analyze_result, indent=2))

        print("\nRunning Stats Test...")
        stats_result = self.test_stats()
        print("\nStats Result:", json.dumps(stats_result, indent=2))

if __name__ == "__main__":
    tester = MCPTester()
    tester.run_all_tests() 