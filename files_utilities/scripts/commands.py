import os
import argparse
import logging
from collections.abc import (
    Callable
)

# set the logging configuration
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

LOGGER = logging.getLogger(__name__)


def get_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    return parser


def get_parser_arguments(parser: argparse.ArgumentParser) -> argparse.Namespace:
    return parser.parse_args()


def ls(path: str) -> list[str | bytes]:
    return os.listdir(path)


def add_argument_type_str(
    parser: argparse.ArgumentParser,
    arg_name: str,
    help_text: str
) -> None:
    parser.add_argument(arg_name, metavar=arg_name, type=str,
                        help=help_text)


def rename(path: str, old_file_name: str, new_file_name: str) -> bool:
    if old_file_name == new_file_name:
        return False
    try:
        os.rename(os.path.join(path, old_file_name),
                  os.path.join(path, new_file_name))
        LOGGER.info('File %s renamed to %s', old_file_name, new_file_name)
        return True
    except OSError as error:
        LOGGER.error('Error renaming file %s', old_file_name)
        LOGGER.error(error)
        return False


def rename_many(
    files: list[str],
    path: str,
    function: Callable[[str], tuple[str, bool]],
) -> None:
    """
    Function to rename many files in a directory
    :param files: list of files to be renamed
    :param path: path to the directory
    :param function:
        function to be applied to the file name
        it should return a tuple with the new name and a boolean
        indicating if the file should be renamed
    :return: None
    """
    count = 0
    for file in files:
        file_name, file_extension = os.path.splitext(file)
        new_name, should_rename = function(file_name)
        if should_rename and new_name != file_name:
            count += rename(path, file, new_name + file_extension)
    LOGGER.info('Total files renamed: %s', count)
