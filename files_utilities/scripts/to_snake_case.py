# script to rename into snake_case files in a folder, the objective
# e.g. file name 'John Dóè CourseFrom 2018-01-01 to 2018-01-31.pdf'
# should be rename to john_dóè_course_2018_01_31.pdf
# the scrip should receive the folder path as an argument

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
        'Rename files in a directory to snake_case')
    add_argument_type_str(parser, 'path', 'path to the directory')

    args = get_parser_arguments(parser)
    path = args.path
    files = ls(path)

    # Note: we won't rename the README.md file
    rename_many(files, path, lambda file_name: (
        to_snake_case(file_name), file_name != "README"
    ))


if __name__ == '__main__':
    main()


# run the script
# python to_snake_case.py /home/username/folder/path/
