import os
import json
from typing import List, Dict, Any, Callable
from core.skill import Skill

class MemorySkill(Skill):
    def __init__(self):
        self.memory_file = os.path.expanduser("~/.jarvis_memory.json")
        self._ensure_memory_file()

    @property
    def name(self) -> str:
        return "memory_skill"

    def _ensure_memory_file(self):
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f:
                json.dump({}, f)

    def _load_memory(self) -> dict:
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except:
            return {}

    def _save_memory(self, memory: dict):
        with open(self.memory_file, 'w') as f:
            json.dump(memory, f, indent=2)

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "remember_fact",
                    "description": "Store information in persistent memory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "key": {"type": "string"},
                            "value": {"type": "string"}
                        },
                        "required": ["key", "value"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "retrieve_memory",
                    "description": "Retrieve stored information",
                    "parameters": {
                        "type": "object",
                        "properties": {"item_name": {"type": "string"}},
                        "required": ["item_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_all_memories",
                    "description": "List all stored memories",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "forget_fact",
                    "description": "Delete a specific memory",
                    "parameters": {
                        "type": "object",
                        "properties": {"key": {"type": "string"}},
                        "required": ["key"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "remember_fact": self.remember_fact,
            "retrieve_memory": self.retrieve_memory,
            "list_all_memories": self.list_all_memories,
            "forget_fact": self.forget_fact
        }

    def remember_fact(self, key: str, value: str) -> str:
        try:
            memory = self._load_memory()
            memory[key] = value
            self._save_memory(memory)
            return json.dumps({"status": "success", "message": f"I will remember that {key} is {value}"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def retrieve_memory(self, item_name: str) -> str:
        try:
            memory = self._load_memory()
            if item_name in memory:
                return json.dumps({"status": "success", "value": memory[item_name]})
            else:
                return json.dumps({"status": "not_found", "message": f"I don't remember '{item_name}'"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def list_all_memories(self) -> str:
        try:
            memory = self._load_memory()
            return json.dumps({"status": "success", "memories": memory, "count": len(memory)})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def forget_fact(self, key: str) -> str:
        try:
            memory = self._load_memory()
            if key in memory:
                del memory[key]
                self._save_memory(memory)
                return json.dumps({"status": "success", "message": f"Forgotten '{key}'"})
            else:
                return json.dumps({"status": "not_found", "message": f"No memory of '{key}'"})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})