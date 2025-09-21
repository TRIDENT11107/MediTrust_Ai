# Resuming YOLO training (quick guide)

If training stopped and you want to resume from the latest checkpoint, follow these steps.

1) Locate checkpoint(s) on your machine

PowerShell (recommended) — run this and paste the output here if you want help locating the correct path:

```powershell
Get-ChildItem -Path 'C:\Users\rasto\runs' -Filter *.pt -Recurse -ErrorAction SilentlyContinue |
  Select-Object FullName,Length,LastWriteTime | Format-Table -AutoSize
```

Or using cmd.exe:

```cmd
for /r "C:\Users\rasto\runs" %f in (*.pt) do @echo %~ff
dir "C:\Users\rasto\runs\*.pt" /s /b
```

Common ultralytics checkpoint paths:
- `C:\Users\rasto\runs\train\exp\weights\last.pt`
- `C:\Users\rasto\runs\train\exp\weights\best.pt`

2) Copy the checkpoint into the project (optional)

If you prefer to keep checkpoints inside the repository (so tools here can access them), run:

```cmd
mkdir "C:\Users\rasto\Desktop\MediTrust_Ai\runs" 2>nul
copy "C:\Users\rasto\runs\train\exp\weights\last.pt" "C:\Users\rasto\Desktop\MediTrust_Ai\runs\last.pt"
```

3) Resume training with the helper

We added `resume_train.cmd` to the repo root. It will attempt to find the checkpoint in the common location `C:\Users\rasto\runs\train\exp\weights\last.pt` or `runs\last.pt` inside the project, then run the proper `yolo`/`python -m ultralytics` resume command.

To run it (cmd.exe):

```cmd
cd C:\Users\rasto\Desktop\MediTrust_Ai
resume_train.cmd
```

Notes:
- If your checkpoint is in a different path, either copy it into `C:\Users\rasto\Desktop\MediTrust_Ai\runs\last.pt` or edit `resume_train.cmd` and set the `CHECK1`/`CHECK2` variables accordingly.
- The helper uses `device=cpu` by default (matching the original `setup_and_train.cmd`). If you trained on GPU and want to use `device=cuda`, edit the command in the helper or run the python command manually.
