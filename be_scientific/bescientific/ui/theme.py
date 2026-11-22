"""Font + theme setup (Hindi needs a Devanagari font; Kivy's default Roboto lacks it)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FONT_NAME = "NotoSansDevanagari"
FONT_FILE = ROOT / "assets" / "fonts" / "NotoSansDevanagari-Regular.ttf"


def register_fonts(theme_cls) -> bool:
    """Register the bundled Devanagari font and use it for every KivyMD text style.

    Returns True if the font was found. Without it Hindi renders as empty boxes
    (see README: download Noto Sans Devanagari into assets/fonts/).
    """
    if not FONT_FILE.is_file():
        print(f"[be_scientific] WARNING: {FONT_FILE} missing - Hindi text will not display.")
        return False
    from kivy.core.text import LabelBase
    LabelBase.register(name=FONT_NAME, fn_regular=str(FONT_FILE))
    styles = getattr(theme_cls, "font_styles", None)
    if isinstance(styles, dict):
        for style, spec in styles.items():
            if isinstance(spec, dict):
                for variant in spec.values():
                    if isinstance(variant, dict) and "font-name" in variant:
                        variant["font-name"] = FONT_NAME
            elif isinstance(spec, list) and spec:
                spec[0] = FONT_NAME
            elif isinstance(spec, tuple) and spec:
                styles[style] = (FONT_NAME, *spec[1:])
    return True


def font_for_fields() -> str | None:
    return FONT_NAME if FONT_FILE.is_file() else None


_ENGLISH_NAMES = {"en": "English", "hi": "Hindi"}


def lang_label(code: str) -> str:
    """Native name when the font can draw it, otherwise a Latin fallback (avoids empty boxes)."""
    from ..i18n import LANGS
    if code == "en" or FONT_FILE.exists():
        return LANGS[code]
    return _ENGLISH_NAMES.get(code, code)
