
# 지능수 프로그래밍 에이아이 (All-in-One, 한국어)

멀티 에이전트(Planner/Coder/Reviewer/Tester/Translator)로 **설계→코딩→리뷰→테스트→한국어화**를 도와주는 Streamlit 앱입니다.
**📲 모바일 인박스**, **📋 클립보드 파이프라인**, **🧩 Wrtn 파이프라인**, **모듈 핫리로드(18-2)** 포함.

## 빠른 실행 (Windows)
- `windows/start_jineungsu.bat` 더블클릭 (Python 설치 필요)
- Python 없이 설치형이 필요하면: `installer/build_installer.ps1` 실행 → `Output/JineungsuAI_Setup.exe` 생성

## 빠른 실행 (공통)
```
pip install -r requirements.txt
streamlit run app.py
```

## 포트
- UI: http://localhost:8501
- 모바일 인박스: http://<PC-IP>:8787/ingest  (POST JSON: {"source":"wrtn","text":"내용"})
