from . import ast as A
import re

lineNumber = 0
indent = 0

def debugIndent ():
    global indent
    indent = indent + 4

def debugOutdent ():
    global indent
    indent = indent - 4

def debugPrint (s):
    global lineNumber
    with open('debug.txt', 'a') as df:
        prefix = " " * indent
        cleanString = re.sub('"', '', str(s))
        cleanString = re.sub('\'', '', cleanString)
        cleanString = re.sub(',', '', cleanString)
        cleanString = re.sub('\[', '(', cleanString)
        cleanString = re.sub('\]', ')', cleanString)
        cleanString = re.sub('False', 'false', cleanString)
        df.write('{}: {}{}\n'.format(lineNumber, prefix, str(cleanString)))
        lineNumber = lineNumber + 1
        

def source(ast):
    if A.isLit(ast):
        return A.litVal(ast)
    if A.isRef(ast):
        return A.varUid(A.refVar(ast))
    if A.isSetClj(ast):
        return ['set!', A.varUid(A.setVar(ast)), source(A.astSubx(ast)[0])]
    if A.isCnd(ast):
        return ['if']  + [source(i) for i in A.astSubx(ast)]
    if A.isPrim(ast):
        return [A.primOp(ast)] + [source(i) for i in A.astSubx(ast)]

    if A.isApp(ast):
        if A.isLam(A.astSubx(ast)[0]):
            return ['let', [[A.varUid(p[0]), source(p[1])] for p in zip(A.lamParams(A.astSubx(ast)[0]), A.astSubx(ast)[1:])], source(A.astSubx(A.astSubx(ast)[0])[0])]
        else:
            return [source(a) for a in A.astSubx(ast)]
        
    if A.isLam(ast):
        x1 = [A.varUid(p) for p in A.lamParams(ast)] 
        x2 = source(A.astSubx(ast)[0])
        return ['lambda',  x1, x2]

    if A.isSeqClj(ast):
        return ['begin'] + [source(a) for a in A.astSubx(ast)]

    print('CRASH')
    exit()
