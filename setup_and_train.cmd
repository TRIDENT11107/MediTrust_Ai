@echo off
setlocal
cd /d "%~dp0"
echo Running setup_and_train from %CD%

echo Checking Python versions...
py -3.11 --version >nul 2>&1 && (
  echo Found Python 3.11, using it for better compatibility...
  set PYTHON_CMD=py -3.11
) || (
  where python >nul 2>&1 || (
    echo Python not found on PATH. Install Python 3.8+ and retry.
    pause
    exit /b 1
  )
  echo Using default python...
  set PYTHON_CMD=python
)

echo Removing any existing .venv_new to start fresh...
if exist ".venv_new" rmdir /s /q .venv_new

echo Creating virtual environment .venv_new...
%PYTHON_CMD% -m venv .venv_new || goto error

echo Activating virtual environment...
call .venv_new\Scripts\activate.bat || goto error

echo Upgrading pip and packaging tools...
python -m pip install --upgrade pip setuptools wheel || goto error

echo Installing numpy first (fixing common compatibility issues)...
pip uninstall -y numpy >nul 2>&1
pip cache purge >nul 2>&1
pip install --no-cache-dir numpy || goto error

echo Testing numpy import...
python -c "import numpy; print('NumPy', numpy.__version__, 'imported successfully')" || goto error

echo Installing ultralytics (this may take a few minutes)...
pip install --no-cache-dir ultralytics || goto error

echo Verifying yolo.exe is available...
if exist ".venv_new\Scripts\yolo.exe" (
  echo Found yolo.exe at .venv_new\Scripts\yolo.exe
) else (
  echo Warning: yolo.exe not found at expected location. Checking alternatives...
  where yolo >nul 2>&1 && echo Found yolo on PATH || echo yolo command not found
)

echo Creating dataset folders (images and labels)...
mkdir "Dataset\images\train" 2>nul
mkdir "Dataset\images\val" 2>nul
mkdir "Dataset\images\test" 2>nul
mkdir "Dataset\labels\train" 2>nul
mkdir "Dataset\labels\val" 2>nul
mkdir "Dataset\labels\test" 2>nul

echo Writing meditrust.yaml to project root...
(
  echo path: C:\Users\rasto\Desktop\MediTrust_Ai\Dataset
  echo train: C:\Users\rasto\Desktop\MediTrust_Ai\Dataset\images\train
  echo val: C:\Users\rasto\Desktop\MediTrust_Ai\Dataset\images\val
  echo test: C:\Users\rasto\Desktop\MediTrust_Ai\Dataset\images\test
  echo nc: 3
  echo names: [class1, class2, class3]
) > "%CD%\meditrust.yaml"

echo Verifying meditrust.yaml exists:
dir /b "%CD%\meditrust.yaml" || goto error
type "%CD%\meditrust.yaml"

echo Configuring ultralytics yolo settings (datasets_dir and runs_dir)...
echo Testing yolo command first...
.venv_new\Scripts\yolo.exe --help >nul 2>&1 || (
  echo ERROR: yolo.exe failed to run. Checking installation...
  python -c "import ultralytics; print('ultralytics version:', ultralytics.__version__)" || goto error
  echo Trying alternative yolo command...
  python -m ultralytics --help >nul 2>&1 || goto error
  echo Using python -m ultralytics instead of yolo.exe
  python -m ultralytics settings datasets_dir="C:\Users\rasto\Desktop\MediTrust_Ai\Dataset" || goto error
  python -m ultralytics settings runs_dir="C:\Users\rasto\runs" || goto error
  goto skip_yolo_exe
)
.venv_new\Scripts\yolo.exe settings datasets_dir="C:\Users\rasto\Desktop\MediTrust_Ai\Dataset" || goto error
.venv_new\Scripts\yolo.exe settings runs_dir="C:\Users\rasto\runs" || goto error
:skip_yolo_exe

echo Starting training (this will run until completion or error)...
echo Trying with yolo.exe first...
.venv_new\Scripts\yolo.exe detect train data="%CD%\meditrust.yaml" model=yolo11n.pt epochs=50 imgsz=640 device=cpu 2>nul || (
  echo yolo.exe failed, trying python -m ultralytics...
  python -m ultralytics detect train data="%CD%\meditrust.yaml" model=yolo11n.pt epochs=50 imgsz=640 device=cpu || goto error
)

echo Training completed.
goto done

:error
echo.
echo ERROR encountered. Check the output above for the failing step.
pause
exit /b 1

:done
echo All done. If training ran, check the runs directory for outputs.
pause
endlocal
