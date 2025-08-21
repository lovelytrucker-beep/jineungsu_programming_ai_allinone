
@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0\.."
where py >nul 2>&1 && (set "PY=py -3") || (set "PY=python")
where %PY% >nul 2>&1 || (echo [지능수] Python이 필요합니다. python.org에서 3.11 64bit 설치 후 재시도하세요.& pause & exit /b 1)
if not exist ".venv" (
  echo [지능수] 가상환경 생성...
  %PY% -m venv .venv || (echo 가상환경 생성 실패 & pause & exit /b 1)
)
call .\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo [지능수] 앱을 시작합니다 → http://localhost:8501
python -m streamlit run app.py
endlocal
