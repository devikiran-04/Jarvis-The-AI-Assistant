import os
import json
from typing import List, Dict, Any, Callable
from core.skill import Skill

class VisionSkill(Skill):
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")

    @property
    def name(self) -> str:
        return "vision_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "analyze_image",
                    "description": "Analyze and describe an image",
                    "parameters": {
                        "type": "object",
                        "properties": {"image_path": {"type": "string"}},
                        "required": ["image_path"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "analyze_image": self.analyze_image
        }

    def analyze_image(self, image_path: str) -> str:
        try:
            from groq import Groq
            import base64
            
            client = Groq(api_key=self.api_key)
            
            # Read and encode image
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            response = client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Describe this image in detail"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            
            description = response.choices[0].message.content
            return json.dumps({
                "status": "success",
                "description": description
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})