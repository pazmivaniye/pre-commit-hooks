#!/usr/bin/env python

import re
import sys

pattern = '([^ -~]|[][<>:"\\\\\\|?*\\(\\)\'`\\s])'

def check(p):
    if p and (p[-1] == '.' or re.search(pattern, p)):
        return True
    return False

def filter(c):
    if ' ' <= c <= '~':
        return c
    return '?'

def main(args = []):
    failed = False
    for arg in args:
        if check(arg):
            failed = True
            name = ''.join(filter(n) for n in arg)
            print(name, file = sys.stderr, flush = True)
    if failed:
        exit(1)

if __name__ == '__main__':
    import signal

    if sys.platform != 'win32':
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    main(sys.argv[1:])
