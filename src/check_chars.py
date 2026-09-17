#!/usr/bin/env python3

import re
import sys

def filter(c: str) -> str:
    if ' ' <= c <= '~':
        return c
    elif c == '\a':
        return '\\a'
    elif c == '\b':
        return '\\b'
    elif c == '\f':
        return '\\f'
    elif c == '\n':
        return '\\n'
    elif c == '\r':
        return '\\r'
    elif c == '\t':
        return '\\t'
    elif c == '\v':
        return '\\v'
    elif ord(c) < 1 << 8:
        return '\\x%02x'%(ord(c))
    elif ord(c) < 1 << 16:
        return '\\u%04x'%(ord(c))
    return '\\U%08x'%(ord(c))

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
        with open(path) as inFile:
            num = 0
            for line in inFile:
                num += 1
                line = line.rstrip('\n')
                if re.search('[^ -~]', line):
                    failed = True
                    line = ''.join(filter(n) for n in line)
                    print('%s:%i:%s'%(path, num, line), file = sys.stderr, flush
                        = True)
    return int(failed)

if __name__ == '__main__':
    import signal

    if sys.platform != 'win32':
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    sys.exit(main(sys.argv[1:]))
