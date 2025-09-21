
@echo off
setlocal
cd /d "%~dp0"
echo ==========================================
echo Resume YOLO training helper (auto-find latest last.pt)
echo Working directory: %CD%
echo ==========================================

set MEDIYAML=%CD%\meditrust.yaml

rem Try to find the most recent last.pt under C:\Users\rasto\runs (recursive)
set MODEL=
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "Get-ChildItem -Path 'C:\Users\rasto\runs' -Filter 'last.pt' -Recurse -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty FullName"`) do (
  set MODEL=%%A
)

rem Fallback: check common locations if powershell returned nothing
if not defined MODEL (
  if exist "C:\Users\rasto\runs\train\exp\weights\last.pt" set MODEL=C:\Users\rasto\runs\train\exp\weights\last.pt
)
if not defined MODEL (
  if exist "%CD%\runs\last.pt" set MODEL=%CD%\runs\last.pt
)

if not defined MODEL (
  echo.
  echo ERROR: No checkpoint found under C:\Users\rasto\runs or in project runs folder.
  echo Please run the PowerShell listing command in README_RESUME.md to find the exact path, or copy the checkpoint into "%CD%\runs\last.pt"
  echo.
  pause
  exit /b 1
)

echo Found checkpoint: %MODEL%
rem Prefer venv yolo.exe if available. Use label-based flow to avoid parser issues.
if exist ".venv_new\Scripts\yolo.exe" (
  echo Using venv yolo.exe at .venv_new\Scripts\yolo.exe
  echo Attempting to resume via venv yolo.exe...
  call ".venv_new\Scripts\yolo.exe" detect train resume model="%MODEL%" data="%MEDIYAML%" epochs=50 imgsz=640 device=cpu
  if errorlevel 1 goto FALLBACK_VENV
  goto RESUME_DONE
)

echo venv yolo.exe not found, trying python -m ultralytics
echo Attempting to resume via python -m ultralytics...
call python -m ultralytics detect train resume model="%MODEL%" data="%MEDIYAML%" epochs=50 imgsz=640 device=cpu
if errorlevel 1 goto FALLBACK_PY
goto RESUME_DONE

:FALLBACK_VENV
echo.
echo Resume via venv yolo.exe failed. Starting a new training run from the checkpoint instead (train model=...)
call ".venv_new\Scripts\yolo.exe" detect train model="%MODEL%" data="%MEDIYAML%" epochs=100 imgsz=640 device=cpu
goto RESUME_DONE

:FALLBACK_PY
echo.
echo Resume via python -m ultralytics failed. Starting a new training run from the checkpoint instead (train model=...)
call python -m ultralytics detect train model="%MODEL%" data="%MEDIYAML%" epochs=100 imgsz=640 device=cpu

:RESUME_DONE

echo Resume command finished (check output above).
pause
endlocal
