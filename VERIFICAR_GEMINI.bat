@echo off
setlocal
cd /d "%~dp0"
title TechBid AI - Diagnostico da chave Gemini
if not exist ".venv\Scripts\python.exe" (
    echo [ERRO] Primeiro execute INICIAR_WINDOWS.bat para instalar as dependencias.
    pause
    exit /b 1
)
echo ================================================
echo  TECHBID AI - VERIFICAR CONEXAO GEMINI
 echo ================================================
echo O teste faz chamadas reais ao Google e pode consumir quota.
echo A chave nao sera exibida.
echo.
".venv\Scripts\python.exe" -m techbid.gemini_check --completo
if errorlevel 1 (
    echo.
    echo [ATENCAO] Ao menos uma etapa falhou. Veja mensagem acima.
) else (
    echo.
    echo [OK] Conexao e extracao estruturada funcionando.
)
echo.
pause
endlocal
