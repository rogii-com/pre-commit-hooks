import argparse
import os
from typing import Optional
from typing import Sequence


# 4 bytes for \r\n\r\n
MAX_DOUBLE_LINE_BREAK_SIZE = 4


def check_end_of_file(filename: str) -> bool:
    with open(filename, 'rb') as f:
        f.seek(0, os.SEEK_END)
        total_count = f.tell()
        if total_count == 0:
            return True
        read_count = min(total_count, MAX_DOUBLE_LINE_BREAK_SIZE)
        f.seek(-read_count, os.SEEK_END)
        # read from 1 up to MAX_DOUBLE_LINE_BREAK_SIZE bytes
        last_lines = f.read(read_count).splitlines(True)
        last_line = last_lines[-1]
        line_content = last_line.splitlines()[0]
        # last line must contain line break and not be empty
        if not line_content or line_content == last_line:
            return False
    return True


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    return_code = 0
    for filename in args.filenames:
        if not check_end_of_file(filename):
            print(f'{filename}: must end with single line break')
            return_code = 1
    return return_code


if __name__ == '__main__':
    exit(main())
