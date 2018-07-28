#!/usr/bin/python3
from compiler import clconvert
from compiler import codegen
from compiler import cpsconvert
from compiler import string2ast
import sys

if len(sys.argv) > 1:
    sourceName = sys.argv[1]
else:
    sourceName = 'samples/test.scm'

with open(sourceName) as f:
    s = f.read()
    a = string2ast.parse(s)
    b = cpsconvert.cpsConvert(a)
    c = clconvert.closureConvert(b)

    code = codegen.codeGenerate(c)
    print(code)
