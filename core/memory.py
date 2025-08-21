
from __future__ import annotations
from typing import List, Dict

class ConversationMemory:
    def __init__(self, max_messages: int = 30):
        self.max_messages = max_messages
        self.buffer: List[Dict[str,str]] = []

    def add(self, role: str, content: str):
        self.buffer.append({"role": role, "content": content})
        if len(self.buffer) > self.max_messages:
            self.buffer = self.buffer[-self.max_messages:]

    def get(self) -> List[Dict[str,str]]:
        return list(self.buffer)
