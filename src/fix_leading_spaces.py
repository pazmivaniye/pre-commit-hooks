#!/usr/bin/env python3

import io
import re
import sys

modulus = 4
tabLen = 8

def main(args = []):
    for arg in args:
        with open(arg) as inFile:
            contents = inFile.read()
        matched = False
        for line in io.StringIO(contents):
            if re.match('^\\s+', line):
                matched = True
                break
        if not matched:
            continue
        with open(arg, 'w') as outFile:
            for line in io.StringIO(contents):
                spaces = re.match('^\\s+', line.rstrip('\n'))
                if spaces:
                    spaces = spaces.group()
                    numChars = len(spaces)
                    numSpaces = sum(tabLen if n == '\t' else 1 for n in spaces)
                    if numSpaces%modulus:
                        numSpaces = int(round(numSpaces/modulus))*modulus
                    line = ' '*numSpaces + line[numChars:]
                outFile.write(line)

if __name__ == '__main__':
    import signal

    if sys.platform != 'win32':
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    main(sys.argv[1:])
