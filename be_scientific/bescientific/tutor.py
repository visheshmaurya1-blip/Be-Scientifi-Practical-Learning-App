"""Hints: always available offline, optionally enriched by the cloud LLM tutor."""
from __future__ import annotations

import re

from .content import SKILLS
from .i18n import t


_QUESTION_WORDS = {
    "a", "an", "and", "are", "about", "can", "do", "does", "explain", "for",
    "give", "how", "i", "in", "is", "it", "me", "of", "please", "show", "tell",
    "help", "in", "into", "language", "on", "simple", "the", "this", "to", "using",
    "with", "words", "what", "when", "where", "which", "who", "why",
    "एक", "और", "कब", "कहाँ", "कौन", "क्या", "कैसे", "क्यों", "की", "का", "के",
    "को", "में", "मुझे", "बताइए", "बताओ", "है", "हैं", "होता", "समझाइए",
}
_ADULT_CONTENT_WORDS = {
    "adult", "boobs", "condom", "dick", "erotic", "fetish", "fuck", "genitals",
    "hentai", "masturbate", "masturbation", "naked", "nude", "nudes", "orgasm",
    "penis", "porn", "porno", "pornography", "pussy", "sex", "sexual", "sexting",
    "xxx", "अश्लील", "कामुक", "नग्न", "पोर्न", "संभोग", "सेक्स", "यौन",
}


def _words(text: str) -> set[str]:
    return {
        word for word in re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE)
        if word not in _QUESTION_WORDS and len(word) > 1
    }


def question_refusal_reason(question: str) -> str | None:
    """Return a safety category before any curriculum response is considered."""
    words = set(re.findall(r"[^\W_]+", question.casefold(), flags=re.UNICODE))
    return "adult_content" if words & _ADULT_CONTENT_WORDS else None


def answer_question(
    question: str,
    courses: dict,
    lang: str = "en",
    course_id: str | None = None,
    preferred_lesson_id: str | None = None,
) -> dict | None:
    """Find a relevant lesson and answer from its bundled study guide."""
    if question_refusal_reason(question):
        return None
    query_words = _words(question)
    if not query_words:
        return None

    matches = []
    for course in courses.values():
        if course_id is not None and course.id != course_id:
            continue
        for lesson in course.lessons:
            text = lesson.hi if lang == "hi" else lesson.en
            chapter = lesson.chapter_hi if lang == "hi" else lesson.chapter_en
            key_words = _words(f"{chapter} {text.focus}")
            content_words = _words(
                f"{chapter} {text.focus} {text.learn} {text.activity} {text.check}"
            )
            matching_words = query_words & content_words
            strong_matches = query_words & key_words
            if not matching_words:
                continue
            score = len(matching_words) + 2 * len(strong_matches)
            if lesson.id == preferred_lesson_id:
                score += 1
            matches.append((
                score,
                len(matching_words) / len(query_words),
                len(matching_words),
                course,
                lesson,
                text,
                chapter,
                bool(strong_matches),
            ))

    if not matches:
        return None
    matches.sort(key=lambda item: (item[0], item[1]), reverse=True)
    score, coverage, matched_count, course, lesson, text, chapter, has_strong_match = matches[0]
    if len(query_words) == 1:
        if not has_strong_match:
            return None
    elif not (
        (has_strong_match and len(query_words) <= 2 and coverage >= 0.5)
        or (matched_count >= 2 and coverage >= 0.67 and score >= 2)
    ):
        return None

    return {
        "course_id": course.id,
        "lesson_id": lesson.id,
        "course_title": course.title_hi if lang == "hi" else course.title_en,
        "book_title": course.book_hi if lang == "hi" else course.book_en,
        "chapter": chapter,
        "focus": text.focus,
        "explanation": text.learn,
        "activity": text.activity,
        "check": text.check,
        "answer": text.answer,
        "source_url": (
            course.source_url_hi if lang == "hi" and course.source_url_hi
            else course.source_url
        ),
    }


def local_hint(skill_id: str, lang: str) -> str:
    """Cached, pre-authored hint - works with no connection."""
    return t(SKILLS[skill_id].hint_key, lang)


def explanation(skill_id: str, lang: str) -> str:
    return t(SKILLS[skill_id].explain_key, lang)


def cloud_hint(base_url: str, skill_id: str, question_id: str, lang: str, attempt: int,
               api_key: str | None = None, post=None, timeout: float = 3.0) -> str | None:
    """Ask the backend LLM tutor for a hint. Returns None on any failure so callers
    fall back to `local_hint` - the learner is never blocked by the network."""
    try:
        if post is None:
            import requests
            post = requests.post
        headers = {"X-API-Key": api_key} if api_key else {}
        r = post(f"{base_url.rstrip('/')}/v1/tutor/hint",
                 json={"skill_id": skill_id, "question_id": question_id, "lang": lang, "attempt": attempt},
                 headers=headers, timeout=timeout)
        if r.status_code == 200:
            return r.json().get("hint") or None
    except Exception:
        pass
    return None
