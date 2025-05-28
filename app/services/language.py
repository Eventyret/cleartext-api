"""Utility for language detection using langdetect."""

from langdetect import detect, LangDetectException

COMMON_LANGUAGE_CODES = {
    "en",
    "fr",
    "de",
    "es",
    "it",
    "pt",
    "nl",
    "ru",
    "zh-cn",
    "zh-tw",
    "ja",
    "ko",
    "ar",
    "tr",
    "sv",
    "no",
    "fi",
    "pl",
}


def detect_language(text: str) -> str:
    """Detect the language from a string of text.

    Args:
        text (str): The input text to analyze.

    Returns:
        dict: Detected language and probability score.
    """
    try:
        language = detect(text)
        if language not in COMMON_LANGUAGE_CODES:
            return "unknown"
        return language
    except LangDetectException:
        return "unknown"
    except Exception:
        raise
