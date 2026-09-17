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

def main(args: list[str] = []) -> int:
    if not args:
        return 0
    if args[0] in ['-v', '--verbose']:
        verbose = True
        paths = args[1:]
    else:
        verbose = False
        paths = args
    failed = False
    for path in paths:
        if verbose:
            print('Checking "%s"'%(path), flush = True)
        if check(path):
            failed = True
            name = ''.join(filter(n) for n in path)
            print(name, file = sys.stderr, flush = True)
    return int(failed)

if __name__ == '__main__':
    import signal

    if sys.platform != 'win32':
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    sys.exit(main(sys.argv[1:]))
