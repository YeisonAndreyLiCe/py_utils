import pytest
import os
from collections.abc import (
    Generator,
)
import shutil

# write a fixture to create a temporary directory and delete it after the test
# is done


@pytest.fixture(scope="function")
def temp_dir() -> Generator[str, None, None]:
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.mkdir(temp_dir)
    yield temp_dir
    shutil.rmtree(temp_dir)

# write a fixture to create files in the temporary directory and delete them
# after the test is done


@pytest.fixture(scope="function")
def temp_files() -> callable:
    temp_files = []

    def _create_files(
        temp_dir: str,
        files_names: list[str]
    ) -> Generator[list[str], None, None]:
        temp_files = [
            os.path.join(temp_dir, file_name) for file_name in files_names
        ]
        for file in temp_files:
            with open(file, "w") as f:
                f.write("This is a test file")
        return temp_files

    yield _create_files
    for file in temp_files:
        os.remove(file)
