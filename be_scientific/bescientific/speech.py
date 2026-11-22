"""Optional text-to-speech (Android via plyer). Silent no-op elsewhere."""
from __future__ import annotations


def speak(text: str) -> bool:
    try:
        from plyer import tts  # available when built with the `plyer` requirement
        tts.speak(text)
        return True
    except Exception:
        return False
