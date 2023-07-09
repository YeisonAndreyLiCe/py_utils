""" script to rename (snake_case) files in a directory, the objective
is to keep part of the name and remove a repeated pattern
e.g. file name 'Joh Doe - Course from 2018-01-01 to 2018-01-31.pdf'
should be rename to from_2018_01_01_to_2018_01_31.pdf
the scrip should receive the folder path as an argument

Note: the script also rename folders in the specified directory

Usage:
    python to_snake_case_removing_pattern.py \
    /home/username/folder/path/ 'Joh Doe - Course '
"""

from utilities import (
    to_snake_case,
)
from commands import (
    ls,
    rename_many,
    get_parser,
    add_argument_type_str,
    get_parser_arguments,
)


def main() -> None:
    parser = get_parser(
        'Rename files in a directory and remove a pattern from the file name')
    add_argument_type_str(parser, 'path', 'path to the directory')
    add_argument_type_str(parser, 'pattern', 'pattern to be removed')
    add_argument_type_str(parser, 'replacement', 'replacement for the pattern')

    args = get_parser_arguments(parser)
    path, pattern, replacement = args.path, args.pattern, args.replacement
    files = ls(path)

    # Note: we won't rename the README.md file
    rename_many(files, path, lambda file_name: (to_snake_case(
        file_name.replace(pattern, replacement)), file_name != "README"))


if __name__ == '__main__':
    main()

# run the script
# python to_snake_case_removing_pattern.py /home/username/folder/path/ 'Joh Doe - Course ' 'from_'
