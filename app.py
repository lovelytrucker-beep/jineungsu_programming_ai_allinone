
import os, threading, json, time, socket, pyperclip
import streamlit as st
from dotenv import load_dotenv

from core.providers import OpenAIProvider
from core.orchestrator import Orchestrator
from core import module_loader

load_dotenv()
st.set_page_config(page_title="지능수 프로그래밍 에이아이", page_icon="🤖", layout="wide")
st.title("🤖 지능수 프로그래밍 에이아이 — v18-2")

with st.sidebar:
    st.subheader("설정")
    api_key = st.text_input("OpenAI API 키", type="password", value=os.getenv("OPENAI_API_KEY",""))
    model = st.text_input("모델 이름", value=os.getenv("OPENAI_MODEL","gpt-4o-mini"))
    st.caption("정책: **호출 불가 AI는 보류**, 사용 가능한 것만 협업합니다.")
    st.markdown("---")
    st.subheader("반자동 협업")
    enable_clipwatch = st.checkbox("클립보드 감시(옵션)", value=False, help="복사된 텍스트를 자동 수집합니다.")
    clip_interval = st.number_input("감시 주기(초)", min_value=1, max_value=60, value=5)
    st.markdown("---")
    st.subheader("활성화할 에이전트")
    use_planner = st.checkbox("Planner (설계)", value=True)
    use_coder = st.checkbox("Coder (코딩)", value=True)
    use_reviewer = st.checkbox("Reviewer (리뷰)", value=True)
    use_tester = st.checkbox("Tester (테스트)", value=True)
    use_translator = st.checkbox("Translator (번역)", value=True)
    st.markdown("---")
    st.subheader("모듈 관리 (핫 로드)")
    if st.button("모듈 재로딩"): st.session_state["_mods"] = module_loader.load_all(); st.success("모듈 로드 완료")
    if "_mods" not in st.session_state: st.session_state["_mods"] = module_loader.load_all()
    enabled_mods = {}
    for lm in st.session_state["_mods"]:
        label = f"✔ {lm.name}" if not lm.error else f"⚠ {lm.name} (에러)"
        enabled_mods[lm.name] = st.checkbox(label, value=(lm.error is None))
        if lm.error: st.code(lm.error[:500])
    up_mod = st.file_uploader("모듈(.py) 업로드", type=["py"])
    if up_mod is not None:
        import pathlib
        p = pathlib.Path(__file__).parent / "modules" / up_mod.name
        p.write_bytes(up_mod.getvalue())
        st.success(f"업로드 완료: {up_mod.name}. [모듈 재로딩]을 눌러주세요.")

from pathlib import Path
prompts_dir = Path(__file__).parent / "prompts"
prompts = {
    "system": (prompts_dir / "system_ko.md").read_text(encoding="utf-8"),
    "planner": (prompts_dir / "planner.md").read_text(encoding="utf-8"),
    "coder": (prompts_dir / "coder.md").read_text(encoding="utf-8"),
    "reviewer": (prompts_dir / "reviewer.md").read_text(encoding="utf-8"),
    "tester": (prompts_dir / "tester.md").read_text(encoding="utf-8"),
    "translator": (prompts_dir / "translator.md").read_text(encoding="utf-8"),
}

if api_key: os.environ["OPENAI_API_KEY"] = api_key
provider = OpenAIProvider(api_key=api_key)
orch = Orchestrator(provider=provider, prompts=prompts)

# ---- Mobile Inbox (Flask) ----
from flask import Flask, request
INBOX_FILE = "mobile_inbox.jsonl"
CLIPBOARD_INBOX_FILE = "clipboard_inbox.jsonl"
_flask = Flask(__name__)
_last_clip = ""

def append_inbox(item: dict):
    try:
        with open(INBOX_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(item, ensure_ascii=False)+"\n")
    except Exception as e: print("Inbox write error:", e)

def append_clipboard(txt: str):
    try:
        with open(CLIPBOARD_INBOX_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": int(time.time()), "source":"clipboard", "text": txt}, ensure_ascii=False)+"\n")
    except Exception as e: print("Clipboard write error:", e)

@_flask.post("/ingest")
def ingest():
    data = request.get_json(silent=True) or {}
    text = data.get("text","")
    source = data.get("source","wrtn")
    meta = {k:v for k,v in data.items() if k not in ["text","source"]}
    if not text: return {"ok": False, "error":"text is required"}, 400
    item = {"ts": int(time.time()), "source": source, "text": text, "meta": meta}
    append_inbox(item)
    return {"ok": True}

def run_flask():
    def _run():
        try: _flask.run(host="0.0.0.0", port=8787, debug=False, use_reloader=False)
        except Exception as e: print("Flask server error:", e)
    import threading; th = threading.Thread(target=_run, daemon=True); th.start()

if "flask_started" not in st.session_state:
    run_flask(); st.session_state.flask_started = True

# ---- Clipboard watcher ----
def _clip_loop(interval: int = 5):
    global _last_clip
    while True:
        try:
            txt = pyperclip.paste()
            if isinstance(txt, str) and txt.strip() and txt != _last_clip:
                _last_clip = txt; append_clipboard(txt)
        except Exception: pass
        time.sleep(interval)

if enable_clipwatch and "clip_started" not in st.session_state:
    import threading; th = threading.Thread(target=_clip_loop, args=(int(clip_interval),), daemon=True); th.start()
    st.session_state.clip_started = True

with st.expander("📲 모바일 인박스 (HTTP POST 수신)", expanded=False):
    st.markdown("휴대폰에서 공유(Share) → **POST http://<이PC IP>:8787/ingest** 로 보낼 수 있습니다.")
    try:
        import socket; ip = socket.gethostbyname(socket.gethostname()); st.code(f"http://{ip}:8787/ingest")
    except Exception: st.code("http://<이PC IP>:8787/ingest")
    if os.path.exists(INBOX_FILE):
        lines = [json.loads(l) for l in open(INBOX_FILE,"r",encoding="utf-8") if l.strip()]
        for it in reversed(lines[-50:]):
            with st.container(border=True):
                st.caption(f"{it.get('source','?')} • {it.get('ts','')}")
                st.write(it.get("text",""))
                if st.button("이 내용으로 새 대화에 사용", key=f"mb_{it.get('ts','')}"):
                    st.session_state.history.append(("user", it.get("text",""))); st.rerun()
    else:
        st.info("아직 수신 없음. 휴대폰에서 한 번 공유해 보세요.")

with st.expander("📋 클립보드 파이프라인", expanded=False):
    if st.button("지금 클립보드 붙여넣기 → 인박스 추가"):
        try:
            t = pyperclip.paste()
            if isinstance(t, str) and t.strip(): append_clipboard(t); st.success("추가되었습니다.")
            else: st.warning("클립보드에 텍스트가 없습니다.")
        except Exception as e: st.error(f"클립보드 접근 실패: {e}")
    if os.path.exists(CLIPBOARD_INBOX_FILE):
        lines = [json.loads(l) for l in open(CLIPBOARD_INBOX_FILE,"r",encoding="utf-8") if l.strip()]
        for it in reversed(lines[-50:]):
            with st.container(border=True):
                st.caption(f"clipboard • {it.get('ts','')}")
                st.write(it.get("text",""))
                if st.button("이 내용으로 새 대화에 사용", key=f"cp_{it.get('ts','')}"):
                    st.session_state.history.append(("user", it.get("text",""))); st.rerun()
    else:
        st.info("아직 수집된 항목이 없습니다.")

with st.expander("🧩 Wrtn 파이프라인 (프롬프트 초안 생성·복사)", expanded=False):
    st.markdown("에이전트 결과를 자동 수집해 Wrtn에 붙여넣을 **한국어 프롬프트 초안**을 생성합니다.")
    c1, c2, c3 = st.columns(3)
    if st.button("템플릿: 요약/정리"): st.session_state["wrtn_goal_tpl"] = "아래 컨텍스트를 핵심 위주로 한국어 요약·정리해 주세요. 누락된 테스트 케이스 보완 제안 포함."
    if c2.button("템플릿: 코드 품질 향상"): st.session_state["wrtn_goal_tpl"] = "안전/성능/가독성 관점에서 개선사항과 수정 예시 코드를 한국어로 제안해 주세요."
    if c3.button("템플릿: 한국어 문서화"): st.session_state["wrtn_goal_tpl"] = "개요/설치/사용법/예제/테스트/주의점을 포함한 한국어 개발자 문서로 정리해 주세요."
    default_goal = st.session_state.get("wrtn_goal_tpl", "아래 계획과 코드/리뷰를 한국어로 읽기 쉽게 정리하고, 누락된 예외 케이스를 보완해 주세요.")
    goal = st.text_area("요청 목적", value=default_goal)
    ctx = []
    if "last_outputs" in st.session_state:
        for k in ["Planner","Coder","Reviewer","Tester"]:
            if k in st.session_state["last_outputs"]: ctx.append(f"[{k}]\n"+st.session_state["last_outputs"][k])
    base = "\n\n".join(ctx) if ctx else "아직 실행된 에이전트 결과가 없습니다."
    st.text_area("컨텍스트(자동 수집)", value=base, height=220)
    composed = f"""다음 컨텍스트를 기반으로 작업해 주세요.

[요청 목적]
{goal}

[컨텍스트]
{base}

[출력 형식]
- 한국어 요약
- 보완 제안 (번호 목록)
- 최종 정리본 (문단/목차 형태)
"""
    st.code(composed, language="markdown")

with st.expander("🛠 프롬프트 라이브 편집 (재시작 없이 저장)", expanded=False):
    from pathlib import Path
    pdir = Path(__file__).parent / "prompts"
    for fn in ["system_ko.md","planner.md","coder.md","reviewer.md","tester.md","translator.md"]:
        p = pdir / fn
        try: txt = p.read_text(encoding="utf-8")
        except Exception as e: st.error(f"{fn} 읽기 실패: {e}"); continue
        new_txt = st.text_area(fn, value=txt, height=160)
        if st.button(f"{fn} 저장"): 
            try: p.write_text(new_txt, encoding="utf-8"); st.success(f"{fn} 저장 완료")
            except Exception as e: st.error(f"{fn} 저장 실패: {e}")

# ---- Chat UI ----
if "history" not in st.session_state: st.session_state.history = []
for role, content in st.session_state.history:
    with st.chat_message(role): st.markdown(content)

user_input = st.chat_input("무엇을 만들까요? (예: 'FastAPI로 간단한 TODO API 만들어줘')")
if user_input:
    st.session_state.history.append(("user", user_input))
    with st.chat_message("user"): st.markdown(user_input)
    enabled = {"planner":use_planner,"coder":use_coder,"reviewer":use_reviewer,"tester":use_tester,"translator":use_translator}
    with st.chat_message("assistant"):
        with st.spinner("에이전트들이 협업 중..."):
            outputs = orch.run(user_input, enabled=enabled, model=model)
            st.session_state["last_outputs"] = outputs

        # apply modules
        mods = [m for m in st.session_state.get("_mods",[]) if enabled_mods.get(m.name,False) and m.error is None]
        if mods:
            outputs = module_loader.apply_modules(mods, outputs, {"user_input": user_input})

        if outputs:
            summary = " · ".join([f"{k}: 완료" for k in outputs.keys()])
            st.markdown(f"**에이전트 요약:** {summary}")
            for name, text in outputs.items():
                with st.expander(f"{name} 결과 보기", expanded=(name=="Coder")):
                    st.markdown(text)
    st.session_state.history.append(("assistant", "에이전트 실행 완료"))
