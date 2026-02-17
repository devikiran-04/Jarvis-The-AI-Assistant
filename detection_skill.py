import os
import json
from typing import List, Dict, Any, Callable
from core.skill import Skill

class DetectionSkill(Skill):
    def __init__(self):
        self.model = None

    @property
    def name(self) -> str:
        return "detection_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "detect_objects",
                    "description": "Detect objects in an image or camera feed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "source": {"type": "string", "enum": ["camera", "image"]},
                            "image_path": {"type": "string"}
                        },
                        "required": ["source"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "detect_objects": self.detect_objects
        }

    def detect_objects(self, source: str = "camera", image_path: str = None) -> str:
        try:
            from ultralytics import YOLO
            import cv2
            from datetime import datetime
            
            # Load model if not loaded
            if self.model is None:
                self.model = YOLO("yolov8n.pt")
            
            if source == "camera":
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                cap.release()
                
                if not ret:
                    return json.dumps({"status": "error", "message": "Failed to capture from camera"})
                
                results = self.model(frame)
                
                # Save annotated image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"detection_{timestamp}.jpg"
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                filepath = os.path.join(desktop_path, filename)
                
                annotated_frame = results[0].plot()
                cv2.imwrite(filepath, annotated_frame)
                
                # Get detected objects
                detected = []
                for result in results:
                    for box in result.boxes:
                        detected.append({
                            "class": result.names[int(box.cls)],
                            "confidence": float(box.conf)
                        })
                
                return json.dumps({
                    "status": "success",
                    "detected_objects": detected,
                    "saved_to": filepath
                })
            
            elif source == "image" and image_path:
                results = self.model(image_path)
                detected = []
                for result in results:
                    for box in result.boxes:
                        detected.append({
                            "class": result.names[int(box.cls)],
                            "confidence": float(box.conf)
                        })
                
                return json.dumps({
                    "status": "success",
                    "detected_objects": detected
                })
            
            else:
                return json.dumps({"status": "error", "message": "Invalid source or missing image_path"})
                
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})