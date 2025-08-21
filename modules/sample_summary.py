
MODULE_NAME = "결과 요약 첨부 (샘플)"
def apply(outputs: dict, context: dict) -> dict:
    res = dict(outputs)
    if outputs:
        res["Summary"] = "에이전트 결과는 위 섹션을 펼쳐 확인하세요. (자동 첨부 요약)"
    return res
