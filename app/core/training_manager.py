import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

_proc: Optional[subprocess.Popen] = None
_log_path: Optional[Path] = None


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _train_script() -> Path:
    # Expect the existing script at app/models/train_yolo.py
    return _repo_root() / 'app' / 'models' / 'train_yolo.py'


def start_training(python_exe: Optional[str] = None, extra_args: Optional[list] = None) -> Dict[str, Any]:
    global _proc, _log_path
    if _proc and _proc.poll() is None:
        return {"status": "already_running", "pid": _proc.pid}

    script = _train_script()
    if not script.exists():
        return {"status": "error", "error": f"Training script not found: {script}"}

    python = python_exe or sys.executable or 'python'
    logs_dir = _repo_root() / 'training_logs'
    logs_dir.mkdir(parents=True, exist_ok=True)
    _log_path = logs_dir / 'train.log'

    cmd = [python, str(script)]
    if extra_args:
        cmd += extra_args

    # Start detached process across platforms and redirect output to log
    stdout_f = open(_log_path, 'ab')
    stderr_f = stdout_f
    kwargs = {'stdout': stdout_f, 'stderr': stderr_f}
    if os.name == 'nt':
        # CREATE_NEW_CONSOLE creates a new window on Windows
        kwargs['creationflags'] = subprocess.CREATE_NEW_CONSOLE
    else:
        # start a new session on POSIX
        kwargs['start_new_session'] = True

    _proc = subprocess.Popen(cmd, cwd=str(_repo_root()), **kwargs)

    return {"status": "started", "pid": _proc.pid, "log": str(_log_path)}


def stop_training() -> Dict[str, Any]:
    global _proc
    if not _proc:
        return {"status": "not_running"}
    if _proc.poll() is not None:
        return {"status": "not_running", "returncode": _proc.returncode}
    try:
        _proc.terminate()
        _proc.wait(timeout=10)
        return {"status": "stopped", "returncode": _proc.returncode}
    except Exception as e:
        try:
            _proc.kill()
            return {"status": "killed"}
        except Exception as e2:
            return {"status": "error", "error": str(e2)}


def status() -> Dict[str, Any]:
    global _proc, _log_path
    if not _proc:
        return {"running": False}
    return {"running": _proc.poll() is None, "pid": _proc.pid, "returncode": _proc.returncode}


def tail_log(lines: int = 200) -> Dict[str, Any]:
    global _log_path
    if not _log_path or not _log_path.exists():
        return {"found": False, "lines": []}
    with _log_path.open('rb') as f:
        data = f.read()
    try:
        text = data.decode('utf-8', errors='replace')
    except Exception:
        text = data.decode('latin-1', errors='replace')
    all_lines = text.splitlines()
    return {"found": True, "lines": all_lines[-lines:]}
