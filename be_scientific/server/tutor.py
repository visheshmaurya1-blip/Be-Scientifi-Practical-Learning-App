"""Cloud tutor: LLM hints via LangChain when configured, static hints otherwise.

Configure with environment variables (none are required):

    LLM_PROVIDER = anthropic | openai        (unset => static hints only)
    LLM_MODEL    = model name for that provider
    plus the provider's usual key, e.g. ANTHROPIC_API_KEY / OPENAI_API_KEY

The LLM path is deliberately defensive: any failure (missing package, no key,
timeout, empty reply) falls back to the static hint, so the endpoint never
breaks the learner's flow. NOTE: the LLM path needs real credentials and has
not been exercised in this repository's tests - only the fallback is tested.
"""
from __future__ import annotations

import os

STATIC = {
    "gravity_equal_fall": {
        "en": "Look at the landing times. When there is no air, gravity gives every object the same acceleration.",
        "hi": "ज़मीन पर पहुँचने के समय देखें। हवा न हो तो गुरुत्वाकर्षण हर वस्तु को एक जैसा त्वरण देता है।"},
    "friction": {
        "en": "Friction resists sliding. Rough surfaces grip more than ice, so the block stops sooner.",
        "hi": "घर्षण फिसलने का विरोध करता है। खुरदरी सतह बर्फ से ज़्यादा पकड़ती है, इसलिए ब्लॉक जल्दी रुकता है।"},
    "elasticity": {
        "en": "A bouncier ball returns more energy after the hit, so it rises higher.",
        "hi": "ज़्यादा उछाल वाली गेंद टकराने के बाद ज़्यादा ऊर्जा लौटाती है, इसलिए ऊँचा उठती है।"},
}
SKILL_TOPIC = {"gravity_equal_fall": "gravity and falling objects", "friction": "friction on a ramp",
               "elasticity": "bounciness (elasticity) of a ball"}
LANG_NAME = {"en": "English", "hi": "Hindi"}


def static_hint(skill_id: str, lang: str) -> str | None:
    entry = STATIC.get(skill_id)
    if not entry:
        return None
    return entry.get(lang) or entry["en"]


def _llm_hint(skill_id: str, lang: str, attempt: int) -> str | None:
    provider = os.getenv("LLM_PROVIDER", "").lower()
    if provider not in ("anthropic", "openai") or skill_id not in SKILL_TOPIC:
        return None
    try:
        if provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            llm = ChatAnthropic(model=os.environ["LLM_MODEL"], max_tokens=120, timeout=8)
        else:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model=os.environ["LLM_MODEL"], max_tokens=120, timeout=8)
        prompt = (
            f"You are a kind science tutor for a child in Class 1-6 in India. The child just answered a "
            f"question about {SKILL_TOPIC[skill_id]} incorrectly (attempt {attempt}). Give ONE short hint "
            f"(max 2 sentences, simple words) in {LANG_NAME.get(lang, 'English')} that nudges them to "
            f"think again WITHOUT stating the final answer."
        )
        text = getattr(llm.invoke(prompt), "content", "")
        if isinstance(text, list):        # some providers return content blocks
            text = "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in text)
        text = (text or "").strip()
        return text or None
    except Exception:
        return None


def get_hint(skill_id: str, lang: str = "en", attempt: int = 1) -> tuple[str, str] | None:
    """Return (hint, source) or None for an unknown skill."""
    hint = _llm_hint(skill_id, lang, attempt)
    if hint:
        return hint, "llm"
    s = static_hint(skill_id, lang)
    return (s, "static") if s else None
