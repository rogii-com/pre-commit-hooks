import argparse
import re
from typing import Optional
from typing import Sequence


def check_q_emit_in_file(filename: str) -> bool:
    result = True
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for i in range(len(lines)):
            line = lines[i]
            if re.search('Q_EMIT\\s*\(', line):
                print(f'{filename}:{i + 1}: Incorrect Q_EMIT usage (the macro should not be used as callable):\n{line}', end='')
                result = False

    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    return_code = 0
    for filename in args.filenames:
        if not filename.endswith(('.cpp', '.hpp')):
            continue
        if not check_q_emit_in_file(filename):
            return_code = 1
    return return_code


if __name__ == '__main__':
    exit(main())
