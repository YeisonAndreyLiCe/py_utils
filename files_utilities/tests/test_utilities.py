from scripts.utilities import (
    remove_extra_whitespace,
    clean_up_string,
    separate_words_and_numbers,
    to_snake_case,
)

import pytest


@pytest.mark.parametrize(
    "string, expected",
    [
        ("John Doe", "John Doe"),
        ("John   Doe", "John Doe"),
        ("JohnDoe  ", "JohnDoe"),
        ("John   Doe  123", "John Doe 123"),
    ]
)
def test_remove_extra_whitespace(string: str, expected: str) -> None:
    assert remove_extra_whitespace(string) == expected


# test_clean_up_string
@pytest.mark.parametrize(
    "string, expected",
    [
        ("John Doe", "John Doe"),
        ("John   Doe", "John Doe"),
        ("JohnDoe  ", "JohnDoe"),
        ("John   Doe  123", "John Doe 123"),
        ("JohnDoe123", "JohnDoe123"),
        ("John#Doe~123$", "John Doe 123"),
        ("John-Doe_123", "John Doe 123"),
        ("John Doe - 123", "John Doe 123"),
        ("John Dóè - 123", "John Dóè 123"),
    ]
)
def test_clean_up_string(string: str, expected: str) -> None:
    assert clean_up_string(string) == expected


# test_separate_words_and_numbers
@pytest.mark.parametrize(
    "string, expected",
    [
        ("John123Doe32", "John 123 Doe 32"),
        ("John Doe123", "John Doe 123"),
        ("JohnDoe123", "JohnDoe 123"),
        ("JohnDoe123#123", "JohnDoe 123 # 123"),
    ]
)
def test_separate_words_and_numbers(string: str, expected: str) -> None:
    assert separate_words_and_numbers(string) == expected


# test_to_snake_case
@pytest.mark.parametrize(
    "string, expected",
    [
        ("John Doe", "john_doe"),
        ("John   Doe", "john_doe"),
        ("JohnDoe  ", "john_doe"),
        ("John   Doe  123", "john_doe_123"),
        ("JohnDoe123", "john_doe_123"),
        ("John#Doe~123$", "john_doe_123"),
        ("John-Doe_123", "john_doe_123"),
        ("John Doe - 123", "john_doe_123"),
        ("John Dóè - 123", "john_dóè_123"),
        (
            "John dóè245 - Course from 2018-01-01 to 2018-01-31",
            "john_dóè_245_course_from_2018_01_01_to_2018_01_31"
        ),
    ]
)
def test_to_snake_case(string: str, expected: str) -> None:
    assert to_snake_case(string) == expected

# run the tests
# pytest test_utilities.py -v
