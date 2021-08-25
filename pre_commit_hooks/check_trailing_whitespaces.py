import argparse
from typing import Optional
from typing import Sequence


def find_trailing_whitespaces(filename: str) -> int:
    with open(filename, 'rb') as f:
        for i, line in enumerate(f, start=1):
            line_content = line.splitlines()[0]
            if line_content and line_content[-1:].isspace():
                return i
    return -1


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    return_code = 0
    for filename in args.filenames:
        line_index = find_trailing_whitespaces(filename)
        if line_index != -1:
            print(f'{filename}: contains trailing whitespaces at line {line_index}')
            return_code = 1
    return return_code


if __name__ == '__main__':
    exit(main())
