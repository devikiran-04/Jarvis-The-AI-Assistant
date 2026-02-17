import os
import json
import re
from groq import Groq
from core.registry import SkillRegistry

class JarvisEngine:
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model_name = "llama-3.3-70b-versatile"

        self.system_instruction = (
            "You are Jarvis, a helpful and precise AI assistant. "
            "Use the provided tools to answer the user's request. "
            "When using tools, output VALID JSON arguments only. "
            "Do NOT output the tool call as XML or with an equals sign. "
            "Just use the standard tool calling format provided by the API."
        )

    def run_conversation(self, user_prompt: str) -> str:
        messages = [
            {"role": "system", "content": self.system_instruction},
            {"role": "user", "content": user_prompt}
        ]

        try:
            tools_schema = self.registry.get_tools_schema()
            completion_kwargs = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": 200
            }

            if tools_schema:
                completion_kwargs["tools"] = tools_schema
                completion_kwargs["tool_choice"] = "auto"

            response = self.client.chat.completions.create(**completion_kwargs)
        except Exception as e:
            error_str = str(e)
            if "tool_use_failed" in error_str and "failed_generation" in error_str:
                try:
                    match = re.search(r'<tool_call>\s*(\w+)\s*\{([^}]+)\}\s*</tool_call>', error_str)
                    if match:
                        func_name = match.group(1)
                        func_args_str = match.group(2)
                        print(f"DEBUG: Recovered failed tool call: {func_name} with {func_args_str}")

                        function_to_call = self.registry.get_function(func_name)
                        if function_to_call:
                            try:
                                args = json.loads(func_args_str)
                                res = function_to_call(**args)
                                return str(res)
                            except Exception as exec_e:
                                return f"Error executing recovered tool: {exec_e}"
                except Exception as parse_e:
                    print(f"Failed to recover tool call: {parse_e}")

            print(f"Groq API Error: {e}")
            return "I am having trouble connecting to the brain, sir."

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            print("DEBUG: Executing Tool...")
            messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                print(f"DEBUG: AI attempting to call: {function_name}")

                function_to_call = self.registry.get_function(function_name)

                if not function_to_call:
                    res = "Error: Tool not found."
                    print(f"DEBUG: Tool {function_name} not found in registry.")
                else:
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                        print(f"DEBUG: Tool arguments: {function_args}")

                        if function_args is None:
                            function_args = {}

                        res = function_to_call(**function_args)
                        print(f"DEBUG: Tool Output: {str(res)[:100]}...")
                    except Exception as e:
                        res = f"Error executing tool: {e}"
                        print(f"DEBUG: Tool Execution Error: {e}")

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(res),
                })

            second_response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            return second_response.choices[0].message.content

        else:
            return response_message.content