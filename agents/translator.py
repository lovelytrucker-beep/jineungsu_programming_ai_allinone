from __future__ import annotations
from agents.base_agent import Agent
from core.providers import OpenAIProvider

def build(provider: OpenAIProvider, system_prompt: str) -> Agent:
    return Agent(name="Translator", system_prompt=system_prompt, provider=provider)