import json
from datetime import datetime
from typing import List, Dict, Any, Callable
from core.skill import Skill

class DateTimeSkill(Skill):
    @property
    def name(self) -> str:
        return "datetime_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_current_datetime",
                    "description": "Get the current date and time",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_current_time",
                    "description": "Get only the current time",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_current_date",
                    "description": "Get only the current date",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "set_timer",
                    "description": "Set a timer for specified minutes",
                    "parameters": {
                        "type": "object",
                        "properties": {"minutes": {"type": "integer"}},
                        "required": ["minutes"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "get_current_datetime": self.get_current_datetime,
            "get_current_time": self.get_current_time,
            "get_current_date": self.get_current_date,
            "set_timer": self.set_timer
        }

    def get_current_datetime(self) -> str:
        now = datetime.now()
        formatted = now.strftime("%A, %B %d, %Y at %I:%M %p")
        return json.dumps({"datetime": formatted, "timezone": "Local"})

    def get_current_time(self) -> str:
        now = datetime.now()
        return json.dumps({"time": now.strftime("%I:%M %p")})

    def get_current_date(self) -> str:
        now = datetime.now()
        return json.dumps({"date": now.strftime("%A, %B %d, %Y")})

    def set_timer(self, minutes: int) -> str:
        import threading
        import os
        
        def timer_callback():
            os.system(f'say "Timer for {minutes} minutes is up"')
        
        threading.Timer(minutes * 60, timer_callback).start()
        return json.dumps({
            "status": "success",
            "message": f"Timer set for {minutes} minutes"
        })