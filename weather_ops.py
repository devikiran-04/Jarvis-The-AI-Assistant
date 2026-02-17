import os
import json
import requests
from typing import List, Dict, Any, Callable
from core.skill import Skill

class WeatherSkill(Skill):
    def __init__(self):
        self.api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        self.default_city = os.environ.get("DEFAULT_CITY", "Mumbai")

    @property
    def name(self) -> str:
        return "weather_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get current weather information for a specified city or pincode",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {"type": "string", "description": "Name of the city or pincode"},
                            "pincode": {"type": "string", "description": "Pincode (optional)"}
                        },
                        "required": ["city"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_forecast",
                    "description": "Get 5-day weather forecast",
                    "parameters": {
                        "type": "object",
                        "properties": {"city": {"type": "string"}},
                        "required": ["city"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "get_weather": self.get_weather,
            "get_forecast": self.get_forecast
        }

    def get_weather(self, city: str, pincode: str = None) -> str:
        if not self.api_key:
            return json.dumps({"status": "error", "message": "API key not configured"})

        try:
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {"appid": self.api_key, "units": "metric"}

            if pincode:
                params["zip"] = f"{pincode},in"
            elif city.strip().isdigit():
                params["zip"] = f"{city},in"
            else:
                params["q"] = city

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                weather_info = {
                    "city": data["name"],
                    "temperature": f"{data['main']['temp']:.1f}°C",
                    "feels_like": f"{data['main']['feels_like']:.1f}°C",
                    "conditions": data["weather"][0]["description"].title(),
                    "humidity": f"{data['main']['humidity']}%",
                    "wind_speed": f"{data['wind']['speed']} m/s"
                }
                return json.dumps({"status": "success", **weather_info})
            else:
                return json.dumps({"status": "error", "message": f"API error: {response.status_code}"})

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def get_forecast(self, city: str) -> str:
        if not self.api_key:
            return json.dumps({"status": "error", "message": "API key not configured"})

        try:
            url = "http://api.openweathermap.org/data/2.5/forecast"
            params = {"appid": self.api_key, "q": city, "units": "metric"}
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                forecast_list = []
                for item in data["list"][:5]:  # Next 5 intervals
                    forecast_list.append({
                        "time": item["dt_txt"],
                        "temp": f"{item['main']['temp']:.1f}°C",
                        "description": item["weather"][0]["description"]
                    })
                return json.dumps({"status": "success", "forecast": forecast_list})
            else:
                return json.dumps({"status": "error", "message": f"API error: {response.status_code}"})
                
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})