import os
import argparse
import logging

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


def rename(path: str, file: str, new_file_name: str) -> bool:
    try:
        os.rename(os.path.join(path, file),
                  os.path.join(path, new_file_name))
        LOGGER.info('File %s renamed to %s', file, new_file_name)
        return True
    except os.error as error:
        LOGGER.error('Error renaming file %s', file)
        LOGGER.error(error)
        return False


def rename_many(
    files: list[str],
    path: str,
    function: callable,
) -> None:
    """
    Function to rename many files in a directory
    :param files: list of files to be renamed
    :param path: path to the directory
    :param function callable[[str], tuple[str, bool]]:
        function to be applied to the file name
        it should return a tuple with the new name and a boolean
        indicating if the file should be renamed
    :return: None
    """
    count = 0
    for file in files:
        file_name, file_extension = os.path.splitext(file)
        new_name, should_rename = function(file_name)
        if should_rename:
            count += rename(path, file, new_name + file_extension)
    LOGGER.info('Total files renamed: %s', count)
