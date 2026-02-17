import os
import json
from typing import List, Dict, Any, Callable
from core.skill import Skill

class CameraSkill(Skill):
    @property
    def name(self) -> str:
        return "camera_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "take_photo",
                    "description": "Take a photo using the webcam",
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
                    "name": "start_camera",
                    "description": "Start camera for live view",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "take_photo": self.take_photo,
            "start_camera": self.start_camera
        }

    def take_photo(self, filename: str = None) -> str:
        try:
            import cv2
            from datetime import datetime
            
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            
            if ret:
                if not filename:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"photo_{timestamp}.jpg"
                
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                filepath = os.path.join(desktop_path, filename)
                cv2.imwrite(filepath, frame)
                cap.release()
                
                return json.dumps({
                    "status": "success",
                    "message": f"Photo saved as {filename}",
                    "path": filepath
                })
            else:
                cap.release()
                return json.dumps({"status": "error", "message": "Failed to capture photo"})
                
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def start_camera(self) -> str:
        try:
            import cv2
            
            cap = cv2.VideoCapture(0)
            cv2.namedWindow("JARVIS Camera - Press Q to quit")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                cv2.imshow("JARVIS Camera - Press Q to quit", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
            return json.dumps({"status": "success", "message": "Camera closed"})
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})