#!/usr/bin/env python

import re
import sys

pattern = '([^ -~]|[][<>:"\\\\\\|?*\\(\\)\'`\\s])'

def check(p: str) -> bool:
    if p and (p[-1] == '.' or re.search(pattern, p)):
        return True
    return False

def filter(c: str) -> str:
    if ' ' <= c <= '~':
        return c
    return '?'

def cout(msg: str) -> None:
    print(msg, flush = True)

def cerr(msg: str) -> None:
    print(msg, file = sys.stderr, flush = True)

def main(args: list[str] | None = None) -> int:
    if args is None:
        args = sys.argv[1:]
    if not args:
        return 0
    if args[0] in ['-v', '--verbose']:
        verbose = True
        paths = args[1:]
        cout('Checking safety of %i filenames'%(len(paths)))
    else:
        verbose = False
        paths = args
    failed = False
    for path in paths:
        if verbose:
            cout('Checking "%s"'%(path))
        if check(path):
            failed = True
            name = ''.join(filter(n) for n in path)
            cerr(name)
    return int(failed)

if __name__ == '__main__':
    if sys.platform != 'win32':
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
