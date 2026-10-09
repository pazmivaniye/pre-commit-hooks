#!/usr/bin/env python3
'''Check for use of double quotes for Python string literals'''

import re
import sys

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
        cout('Checking %i files for string literals in double quotes'%(len(
            paths)))
    else:
        verbose = False
        paths = args
    failed = False
    for path in paths:
        if verbose:
            cout('Checking "%s"'%(path))
        with open(path) as inFile:
            num = 0
            for line in inFile:
                num += 1
                line = line.rstrip('\n')
                if not line or re.match('\\s*#', line):
                    continue
                line = re.sub('\\s#.*$', '', line)
                firstDouble = line.find('\"')
                if firstDouble < 0:
                    continue
                firstSingle = line.find('\'')
                if firstSingle < 0 or firstSingle > firstDouble:
                    failed = True
                    cerr('%s:%i: %s'%(path, num, line))
    return int(failed)

if __name__ == '__main__':
    if sys.platform != 'win32':
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
