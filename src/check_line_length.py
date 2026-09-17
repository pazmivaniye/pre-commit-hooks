#!/usr/bin/env python3

import sys

maxLen = 80
tabLen = 8

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
        cout('Checking %i files for overlong lines'%(len(paths)))
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
                line = line[0:-1]
                curLen = 0
                for n in line:
                    if n == '\t':
                        curLen += tabLen
                    else:
                        curLen += 1
                    if curLen > maxLen:
                        failed = True
                        fmt = '%s:%i:%s'
                        if len(line) > maxLen + 3:
                            fmt += '...'
                            line = line[0:maxLen]
                        cerr(fmt%(path, num, line))
                        break
    return int(failed)

if __name__ == '__main__':
    import signal

    if sys.platform != 'win32':
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    sys.exit(main())
