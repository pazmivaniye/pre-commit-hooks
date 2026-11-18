#!/usr/bin/env python3
"""Mark lines containing invalid characters."""

__all__ = ['main']

import re as _re
import sys as _sys
import typing as _typing

def _filter(c: str, /) -> str:
    """Encode a single non-ASCII/non-printing character as an escape sequence.

    Parameters
    ----------
    c : str
        Character to process.

    Returns
    -------
    str
        Input character if already valid or corresponding escape sequence.

    Raises
    ------
    TypeError
        If input is not a single character.
    """
    if not isinstance(c, str) or len(c) != 1:
        raise TypeError('Expected a single character.')
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

def _cout(msg: str, /) -> None:
    """Write to stdout and flush.

    Parameters
    ----------
    msg : str
        Message to write.
    """
    print(msg, flush = True)

def _cerr(msg: str, /) -> None:
    """Write to stderr and flush.

    Parameters
    ----------
    msg : str
        Message to write.
    """
    print(msg, file = _sys.stderr, flush = True)

def main(args: _typing.Sequence[str] | None = None, /) -> int:
    """Run main.

    Parameters
    ----------
    args : Sequence[str] | None
        Command-line argument overrides. Defaults to `None`.

    Returns
    -------
    int
        Zero on success, nonzero on failure.
    """
    if args is None:
        args = _sys.argv[1:]
    if not args:
        return 0
    if args[0] in ['-v', '--verbose']:
        verbose = True
        paths = args[1:]
        _cout('Checking %i files for invalid characters'%(len(paths)))
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
                line = line.rstrip('\n')
                if _re.search('[^ -~]', line):
                    failed = True
                    line = ''.join(_filter(n) for n in line)
                    _cerr('%s:%i:%s'%(path, num, line))
    return int(failed)

if __name__ == '__main__':
    if _sys.platform != 'win32':
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    _sys.exit(main())
