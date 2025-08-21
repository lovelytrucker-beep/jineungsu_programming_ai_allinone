
from __future__ import annotations
import os
from typing import List, Dict, Optional

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

class OpenAIProvider:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=self.api_key) if (OpenAI and self.api_key) else None

    def chat(self, model: Optional[str], messages: List[Dict[str,str]], **kwargs) -> str:
        model_name = model or self.model
        if self.client is None:
            return "(더미 제공자) API 키가 없어 샘플 응답으로 대체합니다. 마지막 메시지: " + messages[-1].get("content","")[:200]
        try:
            resp = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=kwargs.get("temperature", 0.3),
                max_tokens=kwargs.get("max_tokens", 800),
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"(오류) 모델 호출 실패: {e}"
