#!/usr/bin/env python
"""Check for unsafe filenames."""

__all__ = ['main']

import re as _re
import signal as _signal
import sys as _sys
import typing as _typing

_pattern = '([^ -~]|[][<>:"\\\\\\|?*\\(\\)\'`\\s])'

def _check(p: str, /) -> bool:
    """Check if any path component is unsafe.

    Parameters
    ----------
    p : str
        Path to check.

    Returns
    -------
    bool
        True if unsafe, false if safe.
    """
    if p and (p[-1] == '.' or _re.search(_pattern, p)):
        return True
    return False

def _filter(s: str, /) -> str:
    """Replace non-ASCII/non-printing characters with question marks.

    Parameters
    ----------
    s : str
        String to filter.

    Returns
    -------
    str
        Filtered string.
    """
    return ''.join(n if ' ' <= n <= '~' else '?' for n in s)

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
            _cerr(_filter(path))
    return int(failed)

if __name__ == '__main__':
    if hasattr(_signal, 'SIGPIPE'):
        _signal.signal(_signal.SIGPIPE, _signal.SIG_DFL)
    _sys.exit(main())
