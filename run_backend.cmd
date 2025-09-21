@echo off
REM run_backend.cmd
REM Creates a fresh venv named .venv_run, installs requirements, attempts to install ultralytics,
REM and starts the FastAPI server with uvicorn on port 8000.

setlocal enabledelayedexpansion
echo === MediTrust_Ai: run_backend helper ===

REM Find a usable Python executable
where python >nul 2>&1
if %errorlevel%==0 (
  set "PY=python"
) else (
  where py >nul 2>&1
  if %errorlevel%==0 (
    set "PY=py -3"
  ) else (
    echo ERROR: No Python found on PATH. Install Python 3.10+ from https://www.python.org and retry.
    pause
    exit /b 1
  )
)

echo Using Python: %PY%

REM Use a dedicated venv so we don't overwrite existing .venv or .venv_new
if exist ".venv_run\Scripts\python.exe" (
  echo Using existing .venv_run virtual environment
) else (
  echo Creating virtual environment at .venv_run ...
  %PY% -m venv .venv_run
  if %errorlevel% neq 0 (
    echo Failed to create virtual environment. Try running this script from an elevated prompt.
    pause
    exit /b 1
  )
)

echo Upgrading pip in .venv_run
.venv_run\Scripts\python.exe -m pip install --upgrade pip setuptools wheel

echo Installing Python requirements (this may take a few minutes)...
.venv_run\Scripts\python.exe -m pip install -r requirements.txt
if %errorlevel% neq 0 (
  echo WARNING: pip install returned a non-zero exit code. Check messages above.
  echo You can try re-running the command in an elevated Administrator prompt.
)

echo Installing ultralytics (optional, required for model inference). This may be slow.
.venv_run\Scripts\python.exe -m pip install ultralytics || (
  echo NOTE: ultralytics install failed or was skipped. Detection model inference will be disabled.
)

echo Starting FastAPI server via uvicorn on port 8000
echo If you need the server on port 3000 for the frontend, re-run this script with --port 3000 after editing.
.venv_run\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000

endlocal
