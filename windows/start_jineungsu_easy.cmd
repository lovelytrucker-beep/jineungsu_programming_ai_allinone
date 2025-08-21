@echo off
title 지능수 프로그래밍 에이아이 - 원클릭 실행
chcp 65001 >nul

REM 0. 기준 폴더 이동
cd /d "%~dp0"
cd ..

REM 1. 가상환경 확인/생성
if not exist ".venv" (
  echo [가상환경 생성 중...]
  py -3 -m venv .venv
)

REM 2. 가상환경 활성화
call ".venv\Scripts\activate"

REM 3. 필수 패키지 설치/업데이트 (첫 실행만 조금 걸립니다)
echo [패키지 설치/업데이트...]
python -m pip install --upgrade pip
pip install -r requirements.txt

REM 4. OPENAI_API_KEY 확인
if "%OPENAI_API_KEY%"=="" (
  echo.
  echo [중요] OPENAI_API_KEY 가 설정되어 있지 않습니다.
  set /p KEY=여기에 OpenAI API 키를 붙여넣고 Enter: 
  if not "%KEY%"=="" (
    setx OPENAI_API_KEY "%KEY%" >nul
    set OPENAI_API_KEY=%KEY%
    echo 설정됨. 다음부터는 자동 인식됩니다.
  ) else (
    echo 키가 없어 실행을 계속할 수 없습니다. 창을 닫습니다.
    pause
    exit /b 1
  )
)

REM 5. 앱 실행
echo.
echo 브라우저가 뜨면 http://localhost:8501 입니다.
python -m streamlit run app.py
