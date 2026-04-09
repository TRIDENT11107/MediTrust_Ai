# app/core/auth.py
import os
from typing import Optional

API_KEY_ENV = "MEDITRUST_API_KEY"

def check_api_key(key: Optional[str]) -> bool:
    """
    Return True if the given key matches the environment variable MEDITRUST_API_KEY.
    """
    expected = os.getenv(API_KEY_ENV, "").strip()
    return bool(expected) and key == expected
