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
        print(f"[DEBUG] Detected language: {language}")
        if language not in COMMON_LANGUAGE_CODES:
            return "unknown"
        return language
    except LangDetectException:
        print("[DEBUG] LangDetectException raised")
        return "unknown"
    except Exception as e:
        print(f"[DEBUG] Unexpected error in detect_language: {e}")
        raise
