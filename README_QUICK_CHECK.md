Quick checkpoint integrity & inference check

Files added:
- `tools/quick_check.py` — auto-discovers newest `last.pt`, loads with `ultralytics.YOLO`, and runs inference on a few `Dataset/images/val` images.

How to run (Windows, from project root):

1) Activate venv (if using the project's venv):

```
.venv_new\Scripts\activate.bat
```

2) Run quick check (auto-discover weights):

```
.venv_new\Scripts\python.exe tools\quick_check.py --samples 5 --device cpu
```

3) Or point to a specific checkpoint:

```
.venv_new\Scripts\python.exe tools\quick_check.py --weights "C:\Users\rasto\runs\detect\train8\weights\last.pt" --samples 3 --device cpu
```

Notes:
- The script requires `ultralytics` to be installed in the active Python environment.
- If the script fails to import `ultralytics`, install with:

```
.venv_new\Scripts\python.exe -m pip install ultralytics
```

What it checks:
- Whether the checkpoint file can be loaded.
- Whether inference runs on several val images without raising exceptions.
- It does not check training history or per-epoch logs — for that, inspect the `C:\Users\rasto\runs` experiment folders and `results.txt` files.

PowerShell helper: `tools\resume_and_check.ps1`
------------------------------------------------
This helper automates a few steps (non-destructive):

- Finds the newest `last.pt` under `C:\Users\rasto\runs` or the project's `./runs`.
- Copies it into the project at `./runs/last.pt` (overwrites if present) so resume can be run locally.
- Runs the quick inference check using the project's venv Python.
- Starts `resume_train.cmd` in a new cmd window so training resumes there and continues independently.

Usage (PowerShell, from project root):

```
.
	ools\resume_and_check.ps1
```

You can pass optional params:

```
.
	ools\resume_and_check.ps1 -Samples 3 -Device cpu
```

Notes:
- The script expects `.venv_new\Scripts\python.exe` to exist and have `ultralytics` installed.
- The script is non-destructive: it copies the checkpoint into `./runs/last.pt` instead of moving the original.
- If you need the resume to run in the background or on a remote machine, consider running `resume_train.cmd` via a service or screen/tmux-equivalent. On Windows, `start cmd /k "..."` is used to open a new window that will keep the process running.
