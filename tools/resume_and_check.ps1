<#
resume_and_check.ps1

Quick helper (PowerShell) that:
- finds the newest `last.pt` under C:\Users\rasto\runs or ./runs
- copies it into the project at `./runs/last.pt` (safe, non-destructive)
- runs `tools/quick_check.py` using the project's venv python to validate the checkpoint
- starts `resume_train.cmd` in a new cmd window so training resumes independently

Usage (run from project root PowerShell):
  .\tools\resume_and_check.ps1

This script assumes you have a venv at `.venv_new` and `resume_train.cmd` in project root.
#>

param(
    [int]$Samples = 5,
    [string]$Device = 'cpu'
)

Set-StrictMode -Version Latest
$proj = (Get-Location).Path
Write-Host "Project path: $proj"

Write-Host 'Searching for newest last.pt under C:\Users\rasto\runs and project runs folder...'
$ck = Get-ChildItem -Path 'C:\Users\rasto\runs' -Filter 'last.pt' -Recurse -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $ck) {
    $ck = Get-ChildItem -Path (Join-Path $proj 'runs') -Filter 'last.pt' -Recurse -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
}

if (-not $ck) {
    Write-Error 'No last.pt found. Please place a checkpoint under C:\Users\rasto\runs or copy it into ./runs/last.pt'
    exit 1
}

Write-Host 'Found checkpoint:' $ck.FullName

$destDir = Join-Path $proj 'runs'
if (-not (Test-Path $destDir)) { New-Item -Path $destDir -ItemType Directory | Out-Null }
$dest = Join-Path $destDir 'last.pt'

Write-Host "Copying checkpoint to $dest (will overwrite if exists)"
Copy-Item -Path $ck.FullName -Destination $dest -Force

Write-Host 'Running quick inference check (this uses the venv python)'
$python = Join-Path $proj '.venv_new\Scripts\python.exe'
if (-not (Test-Path $python)) {
    Write-Error "Python executable not found at $python. Activate your venv or provide .venv_new with ultralytics installed."
    exit 2
}

$qc = Join-Path $proj 'tools\quick_check.py'
if (-not (Test-Path $qc)) {
    Write-Error "quick_check.py not found at $qc"
    exit 2
}

& $python $qc --weights $dest --samples $Samples --device $Device

Write-Host 'Launching resume_train.cmd in a new cmd window to resume training (output will be in that window).'
Start-Process -FilePath 'cmd.exe' -ArgumentList '/k', "cd /d `"$proj`" && resume_train.cmd"

Write-Host 'Done. A new command window should have opened and started resume_train.cmd.'
