#!/usr/bin/env python3

import signal
import sys

if sys.platform != 'win32':
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

maxLen = 80

def main():
    failed = False
    for i in range(1, len(sys.argv)):
        with open(sys.argv[i]) as inFile:
            num = 0
            for line in inFile:
                num += 1
                line = line.rstrip('\n')
                if len(line) > maxLen:
                    failed = True
                    print('%s:%i:%s'%(sys.argv[i], num, line), file = sys.
                        stderr, flush = True)
    if failed:
        exit(1)

if __name__ == '__main__':
    main()
