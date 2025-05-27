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
    try:
        language = detect(text)
        if language not in COMMON_LANGUAGE_CODES:
            return "unknown"
        return language
    except LangDetectException:
        return "unknown"
    except Exception:
        raise
