#!/usr/bin/env python3

import signal
import sys

if sys.platform != 'win32':
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

maxLen = 80
tabLen = 8

def main():
    failed = False
    for i in range(1, len(sys.argv)):
        with open(sys.argv[i]) as inFile:
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
                        print(fmt%(sys.argv[i], num, line), file = sys.stderr,
                            flush = True)
                        break
    if failed:
        exit(1)

if __name__ == '__main__':
    main()
