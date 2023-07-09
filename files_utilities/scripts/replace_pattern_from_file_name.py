# replace the pattern in the file name with empty string, that will apply to
# all files in the directory with the specified pattern
from commands import (
    ls,
    get_parser,
    add_argument_type_str,
    get_parser_arguments,
    rename_many,
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

    rename_many(files, path, lambda file_name: (
        file_name.replace(pattern, replacement), pattern in file_name))


if __name__ == '__main__':
    main()

# run the script
# python remove_pattern_from_file_name.py /home/username/folder/path/ 'CertificateOfCompletion - '
