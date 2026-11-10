#!/usr/bin/env python
"""Check for unsafe filenames"""

__all__ = ['main']

import re as _re
import sys as _sys

_pattern = '([^ -~]|[][<>:"\\\\\\|?*\\(\\)\'`\\s])'

def _check(p: str) -> bool:
    if p and (p[-1] == '.' or _re.search(_pattern, p)):
        return True
    return False

def _filter(c: str) -> str:
    if ' ' <= c <= '~':
        return c
    return '?'

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
        _cout('Checking safety of %i filenames'%(len(paths)))
    else:
        verbose = False
        paths = args
    failed = False
    for path in paths:
        if verbose:
            _cout('Checking "%s"'%(path))
        if _check(path):
            failed = True
            name = ''.join(_filter(n) for n in path)
            _cerr(name)
    return int(failed)

if __name__ == '__main__':
    if _sys.platform != 'win32':
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    _sys.exit(main())
