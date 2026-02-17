import os
import json
from typing import List, Dict, Any, Callable
from core.skill import Skill

class WhatsAppSkill(Skill):
    @property
    def name(self) -> str:
        return "whatsapp_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "send_whatsapp_message",
                    "description": "Send a WhatsApp message (opens web.whatsapp.com)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "phone_number": {"type": "string"},
                            "message": {"type": "string"}
                        },
                        "required": ["phone_number", "message"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "send_whatsapp_to_contact",
                    "description": "Send WhatsApp to saved contact",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "contact_name": {"type": "string"},
                            "message": {"type": "string"}
                        },
                        "required": ["contact_name", "message"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "send_whatsapp_message": self.send_whatsapp_message,
            "send_whatsapp_to_contact": self.send_whatsapp_to_contact
        }

    def send_whatsapp_message(self, phone_number: str, message: str) -> str:
        try:
            import pywhatkit
            import webbrowser
            import time
            
            # Remove any non-numeric characters
            phone_number = ''.join(filter(str.isdigit, phone_number))
            
            # Open WhatsApp web with message
            webbrowser.open(f"https://web.whatsapp.com/send?phone={phone_number}&text={message}")
            
            return json.dumps({
                "status": "success",
                "message": f"Opening WhatsApp for {phone_number}",
                "note": "Please scan QR code if not logged in"
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def send_whatsapp_to_contact(self, contact_name: str, message: str) -> str:
        try:
            # This would need a contacts database integration
            # For now, just open WhatsApp web
            import webbrowser
            
            webbrowser.open("https://web.whatsapp.com")
            
            return json.dumps({
                "status": "success",
                "message": f"Opening WhatsApp. Please find {contact_name} manually.",
                "note": "Contact lookup requires phone number database"
            })
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})