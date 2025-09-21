<#
run_backend.ps1
Creates or reuses .venv_run, installs requirements and ultralytics, and starts uvicorn on port 8000.
Run as: .\run_backend.ps1
#>
Param(
    [int]$Port = 8000
)

Write-Host '=== MediTrust_Ai: run_backend (PowerShell) ==='

# choose python
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }
if (-not $py) { Write-Error 'Python not found on PATH. Install Python 3.10+ and retry.'; exit 1 }
Write-Host 'Using Python:' $py

if (-not (Test-Path '.venv_run\Scripts\python.exe')) {
    Write-Host 'Creating .venv_run virtual environment...'
    & $py -m venv .venv_run
    if ($LASTEXITCODE -ne 0) { Write-Error 'Failed to create venv. Try running PowerShell as Administrator.'; exit 1 }
} else {
    Write-Host 'Using existing .venv_run'
}

Write-Host 'Upgrading pip...'
.\.venv_run\Scripts\python.exe -m pip install --upgrade pip setuptools wheel

Write-Host 'Installing requirements (may take a few minutes)...'
.\.venv_run\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { Write-Warning 'pip install returned non-zero. Check output above.' }

Write-Host 'Attempting to install ultralytics (optional for model inference)...'
.\.venv_run\Scripts\python.exe -m pip install ultralytics
if ($LASTEXITCODE -ne 0) { Write-Warning 'ultralytics install failed. Model inference will be disabled.' }

Write-Host "Starting uvicorn on port $Port"
.\.venv_run\Scripts\python.exe -m uvicorn app.main:app --reload --port $Port
