import webbrowser
import json
import requests
from typing import List, Dict, Any, Callable
from core.skill import Skill

class WebSkill(Skill):
    @property
    def name(self) -> str:
        return "web_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "google_search",
                    "description": "Search Google for a query",
                    "parameters": { "type": "object", "properties": { "search_term": {"type": "string"} }, "required": ["search_term"] }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "open_website",
                    "description": "Open a specific website URL",
                    "parameters": { "type": "object", "properties": { "url": {"type": "string"} }, "required": ["url"] }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_news_headlines",
                    "description": "Get latest news headlines",
                    "parameters": { "type": "object", "properties": { "category": {"type": "string", "enum": ["general", "business", "technology", "sports"]} }, "required": [] }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "youtube_search",
                    "description": "Search YouTube for videos",
                    "parameters": { "type": "object", "properties": { "query": {"type": "string"} }, "required": ["query"] }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "google_search": self.google_search,
            "open_website": self.open_website,
            "get_news_headlines": self.get_news_headlines,
            "youtube_search": self.youtube_search
        }

    def google_search(self, search_term):
        try:
            webbrowser.open(f"https://www.google.com/search?q={search_term}")
            return json.dumps({"status": "opened browser", "term": search_term})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def open_website(self, url):
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            webbrowser.open(url)
            return json.dumps({"status": "success", "url": url})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def get_news_headlines(self, category="general"):
        try:
            # Using a free news API (NewsAPI requires key, using RSS as fallback)
            webbrowser.open(f"https://news.google.com/search?q={category}")
            return json.dumps({"status": "success", "message": f"Opened {category} news"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def youtube_search(self, query):
        try:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            return json.dumps({"status": "success", "query": query})
        except Exception as e:
            return json.dumps({"error": str(e)})