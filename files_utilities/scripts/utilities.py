import re


def remove_extra_whitespace(string: str) -> str:
    return " ".join(re.sub(r'\s+', ' ', string).split())


def clean_up_string(string: str) -> str:
    # define the pattern, It should keep accented characters
    pattern = r"([^\W_]+[A-Za-z0-9]*)"  # r"([A-Z]*[a-z]*[\d]*)"
    return remove_extra_whitespace(' '.join(re.findall(pattern, string)))


def separate_words_and_numbers(string: str) -> str:
    pattern = r"(\d+)"
    return ' '.join(re.split(pattern, string)).strip()


def split_camel_case(string: str) -> str:
    # split the string if CamelCase
    return " ".join(re.split(r'([A-Z]+[a-z0-9]+)', string))


def to_snake_case(string: str) -> str:
    _string = split_camel_case(string)
    _string = clean_up_string(_string).lower()
    _string = separate_words_and_numbers(_string)
    return '_'.join(_string.split())
