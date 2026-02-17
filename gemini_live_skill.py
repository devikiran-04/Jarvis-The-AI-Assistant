import os
import json
from typing import List, Dict, Any, Callable
from core.skill import Skill

class GeminiLiveSkill(Skill):
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")

    @property
    def name(self) -> str:
        return "gemini_live_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "ask_gemini",
                    "description": "Ask Google Gemini AI a question",
                    "parameters": {
                        "type": "object",
                        "properties": {"question": {"type": "string"}},
                        "required": ["question"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "gemini_creative",
                    "description": "Generate creative content with Gemini",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {"type": "string"},
                            "type": {"type": "string", "enum": ["story", "poem", "code", "idea"]}
                        },
                        "required": ["prompt", "type"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "ask_gemini": self.ask_gemini,
            "gemini_creative": self.gemini_creative
        }

    def ask_gemini(self, question: str) -> str:
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            response = model.generate_content(question)
            
            return json.dumps({
                "status": "success",
                "answer": response.text
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def gemini_creative(self, prompt: str, type: str) -> str:
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            creative_prompts = {
                "story": f"Write a creative story about: {prompt}",
                "poem": f"Write a poem about: {prompt}",
                "code": f"Generate code for: {prompt}",
                "idea": f"Generate creative ideas for: {prompt}"
            }
            
            full_prompt = creative_prompts.get(type, prompt)
            response = model.generate_content(full_prompt)
            
            return json.dumps({
                "status": "success",
                "type": type,
                "content": response.text
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})