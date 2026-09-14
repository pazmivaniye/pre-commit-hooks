#!/usr/bin/env python

import re
import signal
import sys

if sys.platform != 'win32':
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

pattern = '([^ -~]|[][<>:"\\\\\\|?*\\(\\)\'`\\s])'

def check(p):
    if p and (p[-1] == '.' or re.search(pattern, p)):
        return True
    return False

def filter(c):
    if ' ' <= c <= '~':
        return c
    return '?'

def main():
    failed = False
    for i in range(1, len(sys.argv)):
        if check(sys.argv[i]):
            failed = True
            name = ''.join(filter(n) for n in sys.argv[i])
            print(name, file = sys.stderr, flush = True)
    if failed:
        exit(1)

if __name__ == "__main__":
    main()
