import argparse
import chardet
from typing import Optional
from typing import Sequence

def check_encoding_of_file(filename: str) -> bool:
    with open(filename, 'rb') as f:
        bytes_file = f.read()
        chardet_data = chardet.detect(bytes_file)
        file_encoding = (chardet_data['encoding'])

        if file_encoding != None:        
            return file_encoding in ['ascii', 'utf-8']

        return False

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    return_code = 0
    for filename in args.filenames:
        if not check_encoding_of_file(filename):
            print(f'{filename}: must be with UTF-8 encoding')
            return_code = 1
    return return_code


if __name__ == '__main__':
    exit(main())
