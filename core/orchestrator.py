
from __future__ import annotations
from typing import Dict, Any
from core.providers import OpenAIProvider
from agents import planner as planner_mod, coder as coder_mod, reviewer as reviewer_mod, tester as tester_mod, translator as translator_mod

class Orchestrator:
    def __init__(self, provider: OpenAIProvider, prompts: Dict[str,str]):
        self.provider = provider
        self.prompts = prompts

    def run(self, user_message: str, enabled: Dict[str,bool], model: str | None = None) -> Dict[str,str]:
        outputs: Dict[str,str] = {}

        if enabled.get("planner"):
            planner = planner_mod.build(self.provider, self.prompts.get("planner",""))
            outputs["Planner"] = planner.run(user_message, model=model)
            user_for_code = f"요청: {user_message}\n\n참고 계획:\n{outputs['Planner']}"
        else:
            user_for_code = user_message

        if enabled.get("coder"):
            coder = coder_mod.build(self.provider, self.prompts.get("coder",""))
            outputs["Coder"] = coder.run(user_for_code, model=model)

        if enabled.get("reviewer") and "Coder" in outputs:
            reviewer = reviewer_mod.build(self.provider, self.prompts.get("reviewer",""))
            outputs["Reviewer"] = reviewer.run(outputs["Coder"], model=model)

        if enabled.get("tester"):
            tester = tester_mod.build(self.provider, self.prompts.get("tester",""))
            base = outputs.get("Coder", user_message)
            test_msg = f"요청: {user_message}\n\n대상 코드 또는 설명:\n{base}"
            outputs["Tester"] = tester.run(test_msg, model=model)

        if enabled.get("translator"):
            translator = translator_mod.build(self.provider, self.prompts.get("translator",""))
            agg = []
            for k in ["Planner","Coder","Reviewer","Tester"]:
                if k in outputs: agg.append(f"[{k}]\n"+outputs[k])
            src = "\n\n".join(agg) if agg else user_message
            outputs["Translator"] = translator.run(src, model=model)

        return outputs
