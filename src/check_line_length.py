#!/usr/bin/env python3
"""Mark lines longer than 80 characters"""

__all__ = ['main']

import sys as _sys

_maxLen = 80
_tabLen = 8

def _cout(msg: str) -> None:
    print(msg, flush = True)

def _cerr(msg: str) -> None:
    print(msg, file = _sys.stderr, flush = True)

def main(args: list[str] | None = None) -> int:
    if args is None:
        args = _sys.argv[1:]
    if not args:
        return 0
    if args[0] in ['-v', '--verbose']:
        verbose = True
        paths = args[1:]
        _cout('Checking %i files for overlong lines'%(len(paths)))
    else:
        verbose = False
        paths = args
    failed = False
    for path in paths:
        if verbose:
            _cout('Checking "%s"'%(path))
        with open(path) as inFile:
            num = 0
            for line in inFile:
                num += 1
                line = line[0:-1]
                curLen = 0
                for n in line:
                    if n == '\t':
                        curLen += _tabLen
                    else:
                        curLen += 1
                    if curLen > _maxLen:
                        failed = True
                        fmt = '%s:%i:%s'
                        if len(line) > _maxLen + 3:
                            fmt += '...'
                            line = line[0:_maxLen]
                        _cerr(fmt%(path, num, line))
                        break
    return int(failed)

if __name__ == '__main__':
    if _sys.platform != 'win32':
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    _sys.exit(main())
