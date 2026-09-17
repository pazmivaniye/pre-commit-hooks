#!/usr/bin/env python3

import importlib
import json
import pathlib
import sys

def cout(msg: str) -> None:
    print(msg, flush = True)

def cerr(msg: str) -> None:
    print(msg, file = sys.stderr, flush = True)

def main(args: list[str] | None = None) -> int:
    if args is None:
        args = sys.argv[1:]
    if args:
        cerr('Error: This program does not accept arguments.')
        return 1

    testDir = pathlib.Path(__file__).parent.resolve()
    rootDir = testDir.parent
    srcDir = rootDir / 'src'
    sys.path.insert(0, str(srcDir))

    with open(testDir / 'tests.json') as inFile:
        tests = json.load(inFile)

    tempDir = testDir / 'temp'
    cout('Creating "%s"'%(tempDir))
    tempDir.mkdir(exist_ok = True)

    for scriptName in tests:
        cout('Testing hook %s'%(scriptName))
        module = importlib.import_module(scriptName)
        paths = []
        for fileName in tests[scriptName]['files']:
            paths.append(tempDir / fileName)
            if tests[scriptName]['files'][fileName] is not None:
                cout('Creating "%s"'%(paths[-1]))
                with open(paths[-1], 'w') as outFile:
                    outFile.write(tests[scriptName]['files'][fileName])
        try:
            ret = module.main(['-v'] + [str(n) for n in paths])
        except Exception as e:
            cerr('Error: Uncaught exception in hook %s: %s'%(scriptName, e))
            return 1
        else:
            if ret != tests[scriptName]['ret']:
                cerr('Error: Expected return value %i for hook %s but got %i.'%(
                    tests[scriptName]['ret'], scriptName, ret))
                return 1

    cout('Removing "%s"'%(tempDir))
    for n in tempDir.iterdir():
        n.unlink()
    tempDir.rmdir()

    return 0

if __name__ == '__main__':
    import signal

    if sys.platform != 'win32':
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    sys.exit(main())
