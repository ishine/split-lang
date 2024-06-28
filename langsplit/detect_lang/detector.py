from langdetect import detect
import fast_langdetect

lang_map = {
    "zh": "zh",
    "zh-cn": "zh",
    "zh-tw": "x",
    "ko": "ko",
    "ja": "ja",
}


def detect_lang(text: str) -> str:
    result = str(detect(text))
    result = result.lower()
    return result


def fast_detect_lang(text: str, text_len_threshold=3) -> str:
    if len(text) <= text_len_threshold:
        return detect_lang(text)
    result = str(fast_langdetect.detect(text, low_memory=False)["lang"])
    result = result.lower()
    return result