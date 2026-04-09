Run backend helper
==================

Quick Windows helper scripts to create a fresh Python venv (`.venv_run`), install requirements, and start the FastAPI server (uvicorn).

Usage (cmd.exe):

1. Open `cmd.exe` and `cd` to the project root:

   ```cmd
   cd C:\Users\rasto\Desktop\MediTrust_Ai
   run_backend.cmd
   ```

Usage (PowerShell):

1. Open PowerShell and `cd` to project root, then run:

   ```powershell
   .\run_backend.ps1
   ```

Notes:
- The scripts create `.venv_run` and will not modify existing `.venv` or `.venv_new` folders.
- The scripts attempt to install `ultralytics` (optional). If `ultralytics` fails to install the backend will still run but detection inference will be disabled.
- To change server port, run `run_backend.ps1 -Port 3000` or edit `run_backend.cmd` manually.
