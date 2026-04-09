# app/models/pii_detector.py
import re
from typing import List, Dict

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b")
DATE_RE  = re.compile(r"\b(?:\d{1,2}[/\-\.]){2}\d{2,4}\b")

def find_pii(text: str) -> List[Dict[str, str]]:
    """
    Return a list of {"type": ..., "value": ...}.
    """
    results: List[Dict[str, str]] = []
    for m in EMAIL_RE.findall(text or ""):
        results.append({"type": "email", "value": m})
    for m in PHONE_RE.findall(text or ""):
        results.append({"type": "phone", "value": m})
    for m in DATE_RE.findall(text or ""):
        results.append({"type": "date", "value": m})
    return results
