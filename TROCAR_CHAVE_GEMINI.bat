@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Execute INICIAR_WINDOWS.bat pelo menos uma vez antes.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" configurar_chave.py --trocar
echo Reinicie INICIAR_WINDOWS.bat para carregar a nova chave.
pause
