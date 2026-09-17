#!/usr/bin/env python3

import io
import re
import sys

modulus = 4
tabLen = 8

def cout(msg: str) -> None:
    print(msg, flush = True)

def main(args: list[str] | None = None) -> int:
    if args is None:
        args = sys.argv[1:]
    if not args:
        return 0
    if args[0] in ['-v', '--verbose']:
        verbose = True
        paths = args[1:]
        cout('Checking %i files for simple indentation issues'%(len(paths)))
    else:
        verbose = False
        paths = args
    for path in paths:
        if verbose:
            cout('Checking "%s"'%(path))
        with open(path) as inFile:
            contents = inFile.read()
        matched = False
        for line in io.StringIO(contents):
            if re.match('^\\s+', line):
                matched = True
                break
        if not matched:
            continue
        if verbose:
            cout('Fixing "%s"'%(path))
        with open(path, 'w') as outFile:
            for line in io.StringIO(contents):
                spaces = re.match('^\\s+', line.rstrip('\n'))
                if spaces:
                    numChars = len(spaces.group())
                    numSpaces = sum(tabLen if n == '\t' else 1 for n in spaces.
                        group())
                    if numSpaces%modulus:
                        numSpaces = int(round(numSpaces/modulus))*modulus
                    line = ' '*numSpaces + line[numChars:]
                outFile.write(line)
    return 0

if __name__ == '__main__':
    import signal

    if sys.platform != 'win32':
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    sys.exit(main())
