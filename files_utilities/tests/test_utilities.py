from scripts.utilities import (
    remove_extra_whitespace,
    clean_up_string,
    separate_words_and_numbers,
    to_snake_case,
)
from typing import (
    TypeVar,
)

from scripts.commands import (
    ls,
    rename_many,
)
import uuid

import pytest
import os

from unittest.mock import (
    patch,
    MagicMock,
)

PytestFixture = TypeVar('PytestFixture')


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
        ("JOHN DOE", "john_doe"),
        ("README", "readme"),
        ("", "_"),
        (" ", "_"),
        ("John   Doe", "john_doe"),
        ("JohnDoe  ", "john_doe"),
        ("John   Doe  123", "john_doe_123"),
        ("JohnDoe123", "john_doe123"),
        ("John#Doe~123$", "john_doe_123"),
        ("John-Doe_123", "john_doe_123"),
        ("john-doe_123", "john_doe_123"),
        ("John Dóè - 123", "john_dóè_123"),
        (
            "John dóè245 - Course from 2018-01-01 to 2018-01-31",
            "john_dóè245_course_from_2018_01_01_to_2018_01_31"
        ),
    ]
)
def test_to_snake_case(string: str, expected: str) -> None:
    assert to_snake_case(string) == expected


@patch("scripts.commands.uuid.uuid4", new_callable=MagicMock)
def test_rename_many(
    mock_uuid4: MagicMock,
    temp_dir: PytestFixture,
    temp_files: PytestFixture
) -> None:
    class MockUUID:
        def __init__(self, hex: str) -> None:
            self.hex = hex

    uuid_s = [
        MockUUID("1234567890"),
        MockUUID("1234567891"),
        MockUUID("1234567892"),
    ]
    mock_uuid4.side_effect = uuid_s
    files_names = [
        "John Doe",
        "John   Doe.pdf",
        "JohnDoe45-45_875#l.pdf",
        "JohnDoe45-45_875 l.pdf",
        "John Doe45-45_875#l.pdf",
        "john_doe45_45_875_l.pdf",
    ]
    temp_files_paths = temp_files(temp_dir, files_names)
    folder_content = os.listdir(temp_dir)
    for file_path in temp_files_paths:
        assert file_path.split("/")[-1] in folder_content
        assert file_path.split("/")[-1] in files_names

    expected = [
        "john_doe",
        "john_doe.pdf",
        "john_doe45_45_875_l.pdf",
        f"john_doe45_45_875_l_{uuid_s[0].hex}.pdf",
        f"john_doe45_45_875_l_{uuid_s[1].hex}.pdf",
        f"john_doe45_45_875_l_{uuid_s[2].hex}.pdf",
    ]
    rename_many(folder_content, temp_dir,
                lambda file_name: (to_snake_case(file_name), True))
    _ls = ls(temp_dir)
    # assert mock_uuid4.call_count == 3
    assert len(_ls) == len(files_names)
    for file_path in _ls:
        assert file_path.split("/")[-1] in expected
