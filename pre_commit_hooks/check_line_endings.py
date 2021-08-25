import argparse
import subprocess
from typing import Any
from typing import Generator
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Sequence


# git eolinfo constants
EMPTY_EOLINFO = ''
NONTEXT_EOLINFO = '-text'
NONE_EOLINFO = 'none'
LF_EOLINFO = 'lf'
CRLF_EOLINFO = 'crlf'
MIXED_EOLINFO = 'mixed'


### copy from https://github.com/pre-commit/pre-commit-hooks/blob/v4.0.1/pre_commit_hooks/util.py
class CalledProcessError(RuntimeError):
    pass


def cmd_output(*cmd: str, retcode: Optional[int] = 0, **kwargs: Any) -> str:
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode()
    if retcode is not None and proc.returncode != retcode:
        raise CalledProcessError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout


def zsplit(s: str) -> List[str]:
    s = s.strip('\0')
    if s:
        return s.split('\0')
    else:
        return []
###


class GitFileInfo(NamedTuple):
    index_eolinfo: str
    filename: str


def get_git_file_infos(paths: Sequence[str]) -> Generator[GitFileInfo, None, None]:
    outs = cmd_output('git', 'ls-files', '-z', '--eol', '--', *paths)
    for out in zsplit(outs):
        metadata, filename = out.split('\t')
        metadata_index_eolinfo = metadata.split()[0]
        index_eolinfo = metadata_index_eolinfo.split('/')[1]
        yield GitFileInfo(index_eolinfo, filename)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    parser.add_argument(
        '--allow-eol',
        choices=(LF_EOLINFO, CRLF_EOLINFO),
        default=LF_EOLINFO,
    )
    args = parser.parse_args(argv)

    return_code = 0
    for file_info in get_git_file_infos(args.filenames):
        eolinfo = file_info.index_eolinfo
        if eolinfo == NONTEXT_EOLINFO or eolinfo == NONE_EOLINFO or eolinfo == args.allow_eol:
            continue
        if eolinfo == EMPTY_EOLINFO:
            print(f'{file_info.filename}: is not a regular file')
        else:
            print(f'{file_info.filename}: contains invalid line endings "{eolinfo}"')
        return_code = 1
    return return_code


if __name__ == '__main__':
    exit(main())
