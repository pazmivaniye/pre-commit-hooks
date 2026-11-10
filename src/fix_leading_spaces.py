#!/usr/bin/env python3
"""Make sure that each line begins with a multiple of 4 spaces"""

__all__ = ['main']

import io as _io
import re as _re
import sys as _sys

_modulus = 4
_tabLen = 8

def _cout(msg: str) -> None:
    print(msg, flush = True)

def main(args: list[str] | None = None) -> int:
    if args is None:
        args = _sys.argv[1:]
    if not args:
        return 0
    if args[0] in ['-v', '--verbose']:
        verbose = True
        paths = args[1:]
        _cout('Checking %i files for simple indentation issues'%(len(paths)))
    else:
        verbose = False
        paths = args
    for path in paths:
        if verbose:
            _cout('Checking "%s"'%(path))
        with open(path) as inFile:
            contents = inFile.read()
        matched = False
        for line in _io.StringIO(contents):
            if _re.match('^\\s+', line):
                matched = True
                break
        if not matched:
            continue
        if verbose:
            _cout('Fixing "%s"'%(path))
        with open(path, 'w') as outFile:
            for line in _io.StringIO(contents):
                spaces = _re.match('^\\s+', line.rstrip('\n'))
                if spaces:
                    numChars = len(spaces.group())
                    numSpaces = sum(_tabLen if n == '\t' else 1 for n in spaces.
                        group())
                    if numSpaces%_modulus:
                        numSpaces = int(round(numSpaces/_modulus))*_modulus
                    line = ' '*numSpaces + line[numChars:]
                outFile.write(line)
    return 0

if __name__ == '__main__':
    if _sys.platform != 'win32':
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    _sys.exit(main())
