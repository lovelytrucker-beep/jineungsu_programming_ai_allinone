
$ErrorActionPreference = "Stop"
function Get-ISCC {
  $candidates = @("C:\Program Files (x86)\Inno Setup 6\ISCC.exe","C:\Program Files\Inno Setup 6\ISCC.exe")
  foreach($p in $candidates){ if(Test-Path $p){ return $p } }
  return $null
}
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path $here
if(-not (Test-Path "..\jineungsu_ai\app.py")){ throw "경로 오류: ..\jineungsu_ai\app.py 없음" }
$iscc = Get-ISCC
if(-not $iscc){ throw "Inno Setup(ISCC.exe) 미설치. https://jrsoftware.org 에서 설치 후 다시 실행" }
Remove-Item ".\Output" -Recurse -Force -ErrorAction SilentlyContinue | Out-Null
New-Item -ItemType Directory -Path ".\Output" | Out-Null
& "$iscc" ".\JineungsuAI.iss" /O"Output"
if($LASTEXITCODE -ne 0){ throw "컴파일 실패" }
Write-Host "완료: $here\Output\JineungsuAI_Setup.exe"
