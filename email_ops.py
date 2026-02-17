import os
import json
import imaplib
import email
from typing import List, Dict, Any, Callable
from core.skill import Skill

class EmailSkill(Skill):
    def __init__(self):
        self.email_address = os.environ.get("EMAIL_ADDRESS")
        self.email_password = os.environ.get("EMAIL_PASSWORD")
        self.imap_server = os.environ.get("EMAIL_IMAP_SERVER", "imap.gmail.com")

    @property
    def name(self) -> str:
        return "email_skill"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "check_unread_emails",
                    "description": "Check the number of unread emails in the inbox",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_recent_emails",
                    "description": "Get subject lines and senders of recent emails",
                    "parameters": {
                        "type": "object",
                        "properties": {"count": {"type": "integer"}},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_emails",
                    "description": "Search emails by subject or sender",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "folder": {"type": "string"}
                        },
                        "required": ["query"]
                    }
                }
            }
        ]

    def get_functions(self) -> Dict[str, Callable]:
        return {
            "check_unread_emails": self.check_unread_emails,
            "get_recent_emails": self.get_recent_emails,
            "search_emails": self.search_emails
        }

    def _connect_imap(self):
        if not self.email_address or not self.email_password:
            raise ValueError("Email credentials not configured")
        mail = imaplib.IMAP4_SSL(self.imap_server)
        mail.login(self.email_address, self.email_password)
        return mail

    def check_unread_emails(self) -> str:
        try:
            mail = self._connect_imap()
            mail.select('inbox')
            status, messages = mail.search(None, 'UNSEEN')
            
            if status == 'OK':
                unread_count = len(messages[0].split())
                mail.logout()
                return json.dumps({
                    "status": "success",
                    "unread_count": unread_count,
                    "message": f"You have {unread_count} unread email(s)"
                })
            mail.logout()
            return json.dumps({"status": "error", "message": "Failed to check emails"})
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def get_recent_emails(self, count: int = 5) -> str:
        try:
            mail = self._connect_imap()
            mail.select('inbox')
            status, messages = mail.search(None, 'ALL')
            
            if status != 'OK':
                mail.logout()
                return json.dumps({"status": "error", "message": "Failed to fetch emails"})

            email_ids = messages[0].split()
            recent_ids = email_ids[-count:] if len(email_ids) >= count else email_ids
            recent_ids = reversed(recent_ids)
            
            emails = []
            for email_id in recent_ids:
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                if status == 'OK':
                    email_body = msg_data[0][1]
                    message = email.message_from_bytes(email_body)
                    subject = message['subject']
                    sender = message['from']
                    emails.append({"from": sender, "subject": subject or "(No Subject)"})

            mail.close()
            mail.logout()
            return json.dumps({"status": "success", "emails": emails})
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def search_emails(self, query: str, folder: str = "inbox") -> str:
        try:
            mail = self._connect_imap()
            mail.select(folder)
            status, messages = mail.search(None, f'SUBJECT "{query}"')
            
            if status == 'OK':
                count = len(messages[0].split())
                mail.logout()
                return json.dumps({
                    "status": "success",
                    "found": count,
                    "message": f"Found {count} emails matching '{query}'"
                })
            mail.logout()
            return json.dumps({"status": "error", "message": "Search failed"})
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})