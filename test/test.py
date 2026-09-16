#!/usr/bin/env python3

import importlib
import json
import pathlib
import sys

def main(args = []):
    testDir = pathlib.Path(__file__).parent.resolve()
    rootDir = testDir.parent
    srcDir = rootDir / 'src'
    sys.path.insert(0, str(srcDir))

    with open(testDir / 'tests.json') as inFile:
        tests = json.load(inFile)

    tempDir = testDir / 'temp'
    tempDir.mkdir(exist_ok = True)

    for scriptName in tests:
        module = importlib.import_module(scriptName)
        paths = []
        for fileName in tests[scriptName]:
            paths.append(tempDir / fileName)
            if tests[scriptName][fileName] is not None:
                with open(paths[-1], 'w') as outFile:
                    outFile.write(tests[scriptName][fileName])
        try:
            module.main([str(n) for n in paths])
        except SystemExit as e:
            pass

    for n in tempDir.iterdir():
        n.unlink()
    tempDir.rmdir()

if __name__ == '__main__':
    main(sys.argv[1:])
