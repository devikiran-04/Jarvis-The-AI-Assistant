import os
import json
from typing import List, Dict, Any, Callable
from core.skill import Skill

class ScreenshotSkill(Skill):
    @property
    def name(self) -> str:
        return "screenshot_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "take_screenshot",
                    "description": "Take a screenshot and save it",
                    "parameters": {
                        "type": "object",
                        "properties": {"filename": {"type": "string"}},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "take_region_screenshot",
                    "description": "Take screenshot of a specific screen region",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "integer"},
                            "y": {"type": "integer"},
                            "width": {"type": "integer"},
                            "height": {"type": "integer"}
                        },
                        "required": ["x", "y", "width", "height"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "take_screenshot": self.take_screenshot,
            "take_region_screenshot": self.take_region_screenshot
        }

    def take_screenshot(self, filename: str = None) -> str:
        try:
            import pyautogui
            from datetime import datetime
            
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            filepath = os.path.join(desktop_path, filename)
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            
            return json.dumps({
                "status": "success",
                "message": f"Screenshot saved to Desktop as {filename}",
                "path": filepath
            })
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def take_region_screenshot(self, x: int, y: int, width: int, height: int) -> str:
        try:
            import pyautogui
            from datetime import datetime
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_region_{timestamp}.png"
            
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            filepath = os.path.join(desktop_path, filename)
            
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            screenshot.save(filepath)
            
            return json.dumps({
                "status": "success",
                "message": f"Region screenshot saved",
                "path": filepath
            })
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})