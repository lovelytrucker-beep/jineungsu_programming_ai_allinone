
from __future__ import annotations
from typing import Dict, List
from core.providers import OpenAIProvider

class Agent:
    def __init__(self, name: str, system_prompt: str, provider: OpenAIProvider):
        self.name = name
        self.system_prompt = system_prompt
        self.provider = provider

    def run(self, user_message: str, model: str | None = None) -> str:
        messages: List[Dict[str,str]] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message},
        ]
        return self.provider.chat(model, messages)
