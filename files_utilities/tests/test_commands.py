# run test with: pytest -s -v files_utilities/tests/test_commands.py
from scripts.commands import (
    ls,
    rename_many,
)
from scripts.utilities import (
    to_snake_case,
)
from typing import (
    TypeVar,
)
import os

from unittest.mock import (
    patch,
    MagicMock,
)

PytestFixture = TypeVar('PytestFixture')


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
