@echo off
setlocal
cd /d "%~dp0"
title TechBid AI - Execucao local

echo ================================================
echo TECHBID AI - PRIMEIRA INSTALACAO E EXECUCAO
echo ================================================
echo.
if not exist ".venv\Scripts\python.exe" (
    echo [1/4] Criando ambiente virtual Python...
    where py >nul 2>nul
    if not errorlevel 1 (
        py -3 -m venv .venv
    ) else (
        python -m venv .venv
    )
    if errorlevel 1 goto :fail
)

if not exist ".venv\Scripts\python.exe" goto :fail

echo [2/4] Configurando chave Gemini (somente na primeira vez)...
".venv\Scripts\python.exe" configurar_chave.py
if errorlevel 1 goto :fail

echo [3/4] Verificando bibliotecas (Internet necessaria na primeira vez)...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :fail

echo.
echo [4/4] Iniciando servidor TechBid AI...
echo.
echo SITE: http://127.0.0.1:8000
echo API:  http://127.0.0.1:8000/docs
echo.
echo Deixe esta janela aberta enquanto usa o aplicativo.
echo Para encerrar, pressione CTRL+C.
echo.
REM Sem --reload para evitar falhas do reloader no Windows/OneDrive.
".venv\Scripts\python.exe" -m uvicorn techbid.api:app --host 127.0.0.1 --port 8000
if errorlevel 1 goto :fail
endlocal
exit /b 0

:fail
echo.
echo [ERRO] A inicializacao nao foi concluida. Veja a mensagem acima.
pause
endlocal
exit /b 1
