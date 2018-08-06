#!/usr/bin/python3
from compiler import clconvert
from compiler import codegen
from compiler import cpsconvert
from compiler import string2ast
import sys

sourceName = 'samples/test.scm'
dll = False

while len(sys.argv) > 1:
    v = sys.argv.pop()
    if v == '-dll':
        dll = True
        continue
    sourceName = v

with open(sourceName) as f:
    s = f.read()
    a = string2ast.parse(s)
    b = cpsconvert.cpsConvert(a)
    c = clconvert.closureConvert(b)

    code = codegen.codeGenerate(c)
    if not dll: print('#define __STANDALONE_EXE__\n')
    print(code)
