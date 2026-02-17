import os
import json
from typing import List, Dict, Any, Callable
from core.skill import Skill

class TextSkill(Skill):
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")

    @property
    def name(self) -> str:
        return "text_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "summarize_file",
                    "description": "Read and summarize a text file",
                    "parameters": {
                        "type": "object",
                        "properties": {"filepath": {"type": "string"}},
                        "required": ["filepath"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file_content",
                    "description": "Read raw content of a text file",
                    "parameters": {
                        "type": "object",
                        "properties": {"filepath": {"type": "string"}},
                        "required": ["filepath"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "summarize_file": self.summarize_file,
            "read_file_content": self.read_file_content
        }

    def read_file_content(self, filepath: str) -> str:
        try:
            filepath = os.path.expanduser(filepath)
            if not os.path.exists(filepath):
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", filepath)
                if os.path.exists(desktop_path):
                    filepath = desktop_path

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            return json.dumps({"status": "success", "content": content})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def summarize_file(self, filepath: str) -> str:
        read_result = json.loads(self.read_file_content(filepath))
        if read_result["status"] == "error":
            return json.dumps(read_result)

        content = read_result["content"]
        if len(content) < 100:
            return json.dumps({"status": "success", "summary": content})

        try:
            from groq import Groq
            client = Groq(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Summarize text concisely in 2-3 sentences."},
                    {"role": "user", "content": f"Summarize: {content[:4000]}"}
                ],
                max_tokens=150
            )
            
            summary = response.choices[0].message.content
            return json.dumps({"status": "success", "summary": summary})
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})