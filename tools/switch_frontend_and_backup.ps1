<#
switch_frontend_and_backup.ps1

Non-destructive helper: keeps one frontend folder and moves the other to a timestamped backup.

Usage (from repo root):
  PowerShell -NoProfile -ExecutionPolicy Bypass -File .\tools\switch_frontend_and_backup.ps1 -Keep meditrust-ai-react

Default Keep: meditrust-ai-react
If the other frontend exists (MediTrust_Ai) it will be renamed to e.g. MediTrust_Ai_backup_20250920_120501
This is safer than deleting — you can restore the folder later if needed.
#>

param(
  [string]$Keep = 'meditrust-ai-react'
)

Set-StrictMode -Version Latest
Write-Host "Project root: $(Get-Location)"

$candidates = @('MediTrust_Ai','meditrust-ai-react')

if (-not ($candidates -contains $Keep)) {
  Write-Error "Keep value '$Keep' is not recognized. Valid options: $($candidates -join ', ')"
  exit 2
}

$removeList = $candidates | Where-Object { $_ -ne $Keep }
$toRemove = $null
foreach ($r in $removeList) {
  if (Test-Path (Join-Path (Get-Location) $r)) { $toRemove = $r; break }
}

if (-not $toRemove) {
  Write-Host "No other frontend folder found to move. Nothing to do."; exit 0
}

Write-Host "Keeping: $Keep" -ForegroundColor Green
Write-Host "Found folder to move: $toRemove"

$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupName = "${toRemove}_backup_$timestamp"

try {
  Write-Host "Renaming '$toRemove' -> '$backupName' (non-destructive)..."
  Rename-Item -Path (Join-Path (Get-Location) $toRemove) -NewName $backupName -ErrorAction Stop
  Write-Host "Moved. Backup folder: $backupName" -ForegroundColor Yellow
} catch {
  Write-Error "Failed to move folder: $_"; exit 3
}

Write-Host "\nTo start the kept frontend run the following (example):" -ForegroundColor Cyan
Write-Host "cd \"$(Join-Path (Get-Location) $Keep)\"; npm install; npm run dev" -ForegroundColor Cyan

Write-Host "If you prefer static serving instead, run from repo root: npm start" -ForegroundColor Cyan

exit 0
