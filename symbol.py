from functools import reduce
import ast as A
import debug as D

varNumber = 0

def bindingId(b):
    return b[2]

def incrementId():
    global varNumber
    varNumber = varNumber + 1
    return varNumber

def getVarNumber():
    return incrementId()

def union(s1, s2):
    if not s1:
        return s2
    if not s2:
        return s1
    if s1[0] in s2:
        return union(s1[1:], s2)
    else:
        return [s1[0]] + union(s1[1:], s2)
 
def diff(s1, s2):
    if not s1:
        return []
    if s1[0] in s2:
        return diff(s1[1:], s2)
    else:
        return [s1[0]] + diff(s1[1:], s2)
 
def unionMulti(ls):
    if not ls:
        return []
    return reduce(union, ls)
 
def fv(ast):
    D.debugPrint('FV: {}'.format(ast))

    if A.isRef(ast):
        r = [A.refVar(ast)]
        return r
    if A.isSetClj(ast):
        r = union(fv(A.astSubx(ast)[0]), [A.setVar(ast)])
        return r
    if A.isLam(ast):
        r = diff(fv(A.astSubx(ast)[0]), A.lamParams(ast))
        return r
    r = unionMulti([fv(i) for i in A.astSubx(ast)])
    return r
 
def posInList1(x, lst):
    if not lst:
        return -1
 
    for i, e in enumerate(lst):
        if e == x:
            return i
 
    return -1

def posInList(x, lst):
    r = posInList1(x, lst)
    D.debugPrint('POS = {}'.format(r))
    return r


def newVar(i):
    return A.makeVar(i, '{i}.{n}'.format(i=i, n=getVarNumber()))

def newGlobalVar(i):
    return A.makeVar(i, i)

def isGlobalVar(v):
    return bindingId(v) == A.varUid(v)

def extend1 (r, l1, l2):
    c1 = len(l1)
    c2 = len(l2)
    if c1 == 0 and c2 == 0:
        return [i for i in reversed(r)]
    elif c1 > 0:
        return extend1([l1[0]] + r, l1[1:], l2)
    elif c2 > 0:
        return extend1([l2[0]] + r, l1, l2[1:])

def extendClj (bindings, env):
    return extend1([], bindings, env)


def lookup(identifier, env):
    if len(env) == 0:
        return False

    if bindingId(env[0]) == identifier:
        return env[0]
    else:
        return lookup(identifier, env[1:])

