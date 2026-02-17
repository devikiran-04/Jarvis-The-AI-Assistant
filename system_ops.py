import os
import json
from typing import List, Dict, Any, Callable
from core.skill import Skill

class SystemSkill(Skill):
    @property
    def name(self) -> str:
        return "system_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "set_volume",
                    "description": "Set system volume (0-100)",
                    "parameters": { "type": "object", "properties": { "level": {"type": "integer"} }, "required": ["level"] }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "open_app",
                    "description": "Open an application on the computer",
                    "parameters": { "type": "object", "properties": { "app_name": {"type": "string"} }, "required": ["app_name"] }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "shutdown_system",
                    "description": "Shutdown the computer",
                    "parameters": { "type": "object", "properties": {}, "required": [] }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "restart_system",
                    "description": "Restart the computer",
                    "parameters": { "type": "object", "properties": {}, "required": [] }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "sleep_system",
                    "description": "Put computer to sleep",
                    "parameters": { "type": "object", "properties": {}, "required": [] }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_battery_status",
                    "description": "Get battery percentage and charging status",
                    "parameters": { "type": "object", "properties": {}, "required": [] }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "set_volume": self.set_volume,
            "open_app": self.open_app,
            "shutdown_system": self.shutdown_system,
            "restart_system": self.restart_system,
            "sleep_system": self.sleep_system,
            "get_battery_status": self.get_battery_status
        }

    def set_volume(self, level):
        try:
            os.system(f"osascript -e 'set volume output volume {level}'")
            return json.dumps({"status": "success", "level": level})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def open_app(self, app_name):
        try:
            os.system(f"open -a '{app_name}'")
            return json.dumps({"status": "success", "app": app_name})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def shutdown_system(self):
        try:
            os.system("osascript -e 'tell app \"System Events\" to shut down'")
            return json.dumps({"status": "success", "message": "Shutting down system"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def restart_system(self):
        try:
            os.system("osascript -e 'tell app \"System Events\" to restart'")
            return json.dumps({"status": "success", "message": "Restarting system"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def sleep_system(self):
        try:
            os.system("osascript -e 'tell app \"System Events\" to sleep'")
            return json.dumps({"status": "success", "message": "Putting system to sleep"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def get_battery_status(self):
        try:
            result = os.popen("pmset -g batt").read()
            return json.dumps({"status": "success", "battery_info": result})
        except Exception as e:
            return json.dumps({"error": str(e)})