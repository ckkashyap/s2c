#!/usr/bin/python3
import clconvert
import codegen
import cpsconvert
import re
import string2ast
import sys

def py2clj(s):
    s1 = re.sub(r'\[', '(', s)
    s2 = re.sub(r']', ')', s1)
    s3 = re.sub(r'\'', '', s2)
    s4 = re.sub(r',', '', s3)
    return s4

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
