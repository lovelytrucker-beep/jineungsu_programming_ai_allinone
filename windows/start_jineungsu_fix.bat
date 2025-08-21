@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 프로젝트 루트로 이동
cd /d "%~dp0\.."

REM Python 실행기 선택
set "PY_CMD="
where py >nul 2>&1 && set "PY_CMD=py -3"
if not defined PY_CMD (
  where python >nul 2>&1 && set "PY_CMD=python"
)
if not defined PY_CMD (
  echo [지능수] Python이 보이지 않습니다. python.org 에서 3.x(64bit) 설치 후 다시 실행하세요.
  pause
  exit /b 1
)

REM 가상환경 생성(없을 때만)
if not exist ".venv\Scripts\python.exe" (
  echo [지능수] 가상환경 생성 중...
  %PY_CMD% -m venv .venv || (echo [지능수] venv 생성 실패 & pause & exit /b 1)
)

REM 가상환경 활성화
call .\.venv\Scripts\activate.bat

REM 의존성 설치/업데이트
python -m pip install --upgrade pip
pip install -r requirements.txt

REM 앱 실행
echo [지능수] 앱 시작 → http://localhost:8501
python -m streamlit run app.py
endlocal
