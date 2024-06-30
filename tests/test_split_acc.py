from typing import List

from langsplit import split_by_lang
from langsplit.split.splitter import SubString, TextSplitter, _get_languages
from langsplit.split.utils import PUNCTUATION
from tests.test_config import TEST_DATA_FOLDER

new_lang_map = {
    "zh": "zh",
    "zh-cn": "zh",
    "zh-tw": "x",
    "ko": "ko",
    "ja": "ja",
}


def get_corrected_split_result(text_file_path: str) -> List[List[SubString]]:
    """
    # 1. split by `|`
    # 2. convert to SubString, concat to list
    """
    corrected_split_result: List[List[SubString]] = []

    with open(text_file_path, "r", encoding="utf-8") as file:
        for line in file:
            substrings = line.strip().split("|")
            # print(substrings)

            substring_objects: List[SubString] = []

            current_index = 0

            for substring in substrings:
                is_punctuation = substring.strip() in PUNCTUATION
                substring_objects.append(
                    SubString(
                        lang="punctuation" if is_punctuation else "x",
                        text=substring,
                        index=current_index,
                        length=len(substring),
                        is_punctuation=is_punctuation,
                    )
                )

                current_index += len(substring)
            substring_objects = _get_languages(
                lang_text_list=substring_objects,
                lang_map=new_lang_map,
                default_lang="en",
            )
            corrected_split_result.append(substring_objects)

    return corrected_split_result


def main():
    splitter = TextSplitter()
    zh_jp_ko_en_lang_map = {
        "zh": "zh",
        "zh-cn": "zh",
        "zh-tw": "x",
        "ko": "ko",
        "ja": "ja",
    }

    text_file_name = "correct_split.txt"
    correct_split = get_corrected_split_result(
        text_file_path=f"{TEST_DATA_FOLDER}/{text_file_name}"
    )
    correct_total_substring_len = 0
    test_total_substring_len = 0
    correct_split_num = 0

    original_strings = []
    test_split: List[List[SubString]] = []
    # MARK: collect original_strings from .txt and test `split()`
    for correct_substrings in correct_split:
        current_correct_num = 0
        correct_total_substring_len += len(correct_substrings)
        substrings_text = []
        for correct_substring in correct_substrings:
            substrings_text.append(correct_substring.text)
        original_string = "".join(substrings_text)
        original_strings.append(original_string)
        # print(original_string)
        test_split_substrings = split_by_lang(
            text=original_string,
            lang_map=zh_jp_ko_en_lang_map,
            default_lang="en",
            splitter=splitter,
        )
        test_split.append(test_split_substrings)
        test_total_substring_len += len(test_split_substrings)
        correct_substrings_text = [
            f"{item.index}|{item.text}" for item in correct_substrings
        ]
        test_split_substrings_text = [
            f"{item.index}|{item.text}" for item in test_split_substrings
        ]
        print(f"correct_substrings   : {correct_substrings_text}")
        print(f"test_split_substrings: {test_split_substrings_text}")

        for test_substring in test_split_substrings:
            for correct_substring in correct_substrings:
                if (
                    test_substring.text == correct_substring.text
                    and test_substring.index == correct_substring.index
                ):
                    correct_split_num += 1
                    current_correct_num += 1
                    break

        print(
            f"acc                  : {current_correct_num}/{len(correct_substrings_text)}"
        )
        print("--------------------------")

    print(f"total substring num: {correct_total_substring_len}")
    print(f"test total substring num: {test_total_substring_len}")
    print(f"text acc num: {correct_split_num}")
    precision = correct_split_num / correct_total_substring_len
    print(f"precision: {precision}")
    recall = correct_split_num / test_total_substring_len
    print(f"recall: {recall}")
    f1_score = 2 * precision * recall / (precision + recall)
    print(f"F1 Score: {f1_score}")
    return


if __name__ == "__main__":
    main()
