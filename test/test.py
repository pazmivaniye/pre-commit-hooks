#!/usr/bin/env python3
"""Run tests on each pre-commit hook"""

__all__ = ['main']

import importlib as _importlib
import json as _json
import pathlib as _pathlib
import sys as _sys

def _cout(msg: str) -> None:
    print(msg, flush = True)

def _cerr(msg: str) -> None:
    print(msg, file = _sys.stderr, flush = True)

def main(args: list[str] | None = None) -> int:
    if args is None:
        args = _sys.argv[1:]
    if args:
        _cerr('ValueError: This program does not accept arguments.')
        return 1

    testDir = _pathlib.Path(__file__).parent.resolve()
    rootDir = testDir.parent
    srcDir = rootDir / 'src'
    _sys.path.insert(0, str(srcDir))

    with open(testDir / 'tests.json') as inFile:
        tests = _json.load(inFile)

    tempDir = testDir / 'temp'
    _cout('Creating "%s"'%(tempDir))
    tempDir.mkdir(exist_ok = True)

    for scriptName in tests:
        _cout('Testing hook %s'%(scriptName))
        module = _importlib.import_module(scriptName)
        paths = []
        for fileName in tests[scriptName]['files']:
            paths.append(tempDir / fileName)
            if tests[scriptName]['files'][fileName] is not None:
                _cout('Creating "%s"'%(paths[-1]))
                with open(paths[-1], 'w') as outFile:
                    outFile.write(tests[scriptName]['files'][fileName])
        try:
            ret = module.main(['-v'] + [str(n) for n in paths])
        except Exception as e:
            _cerr('%s: Uncaught exception in hook %s: %s'%(type(e).__name__,
                scriptName, e))
            return 1
        else:
            if ret != tests[scriptName]['ret']:
                _cerr('ValueError: Expected return value %i for hook %s but got'
                    ' %i.'%(tests[scriptName]['ret'], scriptName, ret))
                return 1

    _cout('Removing "%s"'%(tempDir))
    for n in tempDir.iterdir():
        n.unlink()
    tempDir.rmdir()

    return 0

if __name__ == '__main__':
    if _sys.platform != 'win32':
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    _sys.exit(main())
