from . import ast as A
from . import parse as P
from . import symbol as S

def cc(selfVar, freeVars, ast):

    if A.isLit(ast):
        return ast

    if A.isRef(ast):
        i = S.posInList(A.refVar(ast), freeVars)
        ret = 0
        if i != -1:
            ret = A.makePrim(
                    [A.makeRef([], selfVar), A.makeLit([], i + 1)],
                    '%closure-ref')
        else:
            ret = ast

        return ret

    if A.isSetClj(ast):
        ret = A.makeSet([cc(selfVar, freeVars, x) for x in A.astSubx(ast)],
                         A.setVar(ast))
        return ret

    if A.isCnd(ast):
        ret = A.makeCnd([cc(selfVar, freeVars, x) for x in A.astSubx(ast)])
        return ret

    if A.isPrim(ast):
        ret =  A.makePrim([cc(selfVar, freeVars, x) for x in A.astSubx(ast)],
                          A.primOp(ast))
        return ret

    if A.isApp(ast):
        func = A.astSubx(ast)[0]
        args = [cc(selfVar, freeVars, x) for x in A.astSubx(ast)[1:]]
        ret = 0
        if A.isLam(func):
            lam = (lambda x: cc(selfVar, freeVars, x))
            lamApplied = lam(A.astSubx(func)[0])
            ret = A.makeApp([A.makeLam([lamApplied], A.lamParams(func))] + args)
            return ret
        else:
            f = (lambda x: cc(selfVar, freeVars, x))(func)
            prim = A.makePrim([f, A.makeLit([], 0)], '%closure-ref')
            ret = A.makeApp([prim, f] + args)
            return ret

    if A.isLam(ast):
        newFreeVars = [x for x in S.fv(ast) if not S.isGlobalVar(x)]
        newSelfVar = S.newVar('self')

        subExp = A.astSubx(ast)[0]
        convertedSubExp = cc(newSelfVar, newFreeVars, subExp)
        params = [newSelfVar] + A.lamParams(ast)

        closureFunc = A.makeLam([convertedSubExp], params) 
        closureParams = [(lambda x: cc(selfVar, freeVars, x))(A.makeRef([], v)) for v in newFreeVars]

        ret = A.makePrim([closureFunc] + closureParams, '%closure')
        return ret

    if A.isSeqClj(ast):
        ret = A.makeSeq(
                [cc(selfVar, freeVars, x) for x in A.astSubx(ast)])
        return ret

    print('Unknown AST in clconvert {}'.format(ast))
    exit()

def convert(ast, selfVar, freeVars):
    return cc(selfVar, freeVars, ast)

def closureConvert(ast):
    ret = A.makeLam([convert(ast, False, [])], [])
    return ret
