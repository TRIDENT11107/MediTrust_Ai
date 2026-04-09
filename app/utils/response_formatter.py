# app/utils/response_formatter.py
from typing import Any, Dict

def ok(data: Any) -> Dict[str, Any]:
    return {"ok": True, "data": data}

def error(message: str) -> Dict[str, Any]:
    return {"ok": False, "error": message}
