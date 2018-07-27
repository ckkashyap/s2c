import ast as A
import debug as D
import parse as P
import re
import symbol as S

def py2clj(s):
    s1 = re.sub(r'\[', '(', s)
    s2 = re.sub(r']', ')', s1)
    s3 = re.sub(r'\'', '', s2)
    s4 = re.sub(r',', '', s3)
    return s4

def xe(e, cte):
    if A.isConstExpr(e):
        r = xeConstExpr(e, cte)
        return r
    if A.isIdentExpr(e):
        r = xeIdentExpr(e, cte)
        return r
    if A.isFormExpr(e):
        r = xeFormExpr(e, cte)
        return r
    print ('Syntax error {}'.format(e))
    exit()

def xeConstExpr(e, cte):
    return A.makeLit([], e)

def xeIdentExpr(e, cte):
    b = xeLookup(e, cte)
    if A.isVarClj(b):
        return A.makeRef([], b)
    else:
        print("Can't reference nonvariable")
        exit()

def xeFormExpr (e, cte):
    h = e[0]
    b = A.isIdentExpr(h) and xeLookup(h, cte)
    if A.isMacro(b):
        f = A.macroExpander(b)
        r = f(e, cte)
        return r
    else:
        return A.makeApp(xeExprs(e, cte))

def xeExprs(le, cte):
    return [xe(x, cte) for x in le]

def makeInitialCte():
    def binOp(op, n):
        def m(e, cte):
            if len(e[1:]) == n:
                return A.makePrim(xeExprs(e[1:], cte), op)
            else:
                print(f'Expecting {n} args')
                exit()
        return lambda x, y: m(x, y)

    def setFunc(e, cte):
        if len(e) == 3: # Needs to be (set! variableName variableValue)
            varName = e[1]
            varBinding = xeLookup(varName, [])
            if A.isVarClj(varBinding):
                varValue = e[2:]
                return A.makeSet(xeExprs(varValue, cte), varBinding)
            else:
                print('Not a valid set expression {}'.format(e))
                exit()

    def defFunc(e,cte):
        return xe(['set!'] + e[1:], cte)

    def ifFunc(e, cte):
        if len(e) == 4:
            return A.makeCnd(xeExprs(e[1:], cte))
        elif len(e) == 3:
            return xe(['if', e[1], e[2], False], cte)
        else:
            print ("Bad if")
            exit()

    def lambdaFunc(e, cte):
        if len(e) >= 2:
            params = [S.newVar(x) for x in e[1]]
            body = e[2:]
            newCte = S.extendClj(params, cte)
            return A.makeLam([xe(['begin'] + body, newCte)], params)
        else:
            print("Lambda expects a parameter")
            exit()

    def beginFunc(e, cte):
        if len(e)==1:
            return xe(False, cte)
        elif len(e)==2:
            return xe(e[1], cte)
        else:
            return A.makeSeq(xeExprs(e[1:], cte))

    def letFunc(e, cte):
        if len(e)>=2:
            bindingNames = [x[0] for x in e[1]]
            bindingValues = [x[1] for x in e[1]]
            body = e[2:]
            return xe([['lambda', bindingNames] + body] + bindingValues, cte)
        else:
            print('BAD LET {}'.format(e))
            exit()
            
    def orFunc(e, cte):
        if len(e) == 1:
            return xe(False, cte)
        elif len(e) == 2:
            return xe(e[1], cte)
        else:
            x1 = py2clj(str(e[1]))
            x2 = py2clj(' '.join([str(x) for x in e[2:]]))
            s = ''.join(["((lambda (t1 t2) (if t1 t1 (t2))) ",
                        x1, "(lambda () (or ", x2, ")))"])
            x3 = P.parse(s)
            return xe(x3, cte)

    def andFunc(e, cte):
        if len(e) == 1:
            return xe(True, cte)
        elif len(e) == 2:
            return xe(e[1], cte)
        else:
            x1 = py2clj(str(e[1]))
            x2 = py2clj(' '.join([str(x) for x in e[2:]]))
            s = ''.join(["((lambda (t1 t2) (if t1 (t2) t1)) ",
                        x1, "(lambda () (and ", x2, ")))"])
            x3 = P.parse(s)
            return xe(x3, cte)

    return [
            A.makeMacro('=', binOp('%=', 2)),
            A.makeMacro ('<', binOp('%<', 2)),
            A.makeMacro ('+', binOp('%+', 2)),
            A.makeMacro ('-', binOp('%-', 2)),
            A.makeMacro ('*', binOp('%*', 2)),
            A.makeMacro ('add3', binOp('%+3', 3)),
            A.makeMacro ('print-vector', binOp('%print-vec', 1)),
            A.makeMacro ('new-vector', binOp('%new-vec', 1)),
            A.makeMacro ('display', binOp('%display', 1)),
            A.makeMacro ('set!', setFunc),
            A.makeMacro ('define', defFunc),
            A.makeMacro ('if', ifFunc),
            A.makeMacro ('lambda', lambdaFunc),
            A.makeMacro ('begin', beginFunc),
            A.makeMacro ('let', letFunc),
            A.makeMacro ('or', orFunc),
            A.makeMacro ('and', andFunc)]

def xeLookupGlobalCte (var):
    return S.lookup(var, xeGlobalCte)

def xeAddToGlobalCte(var):
    global xeGlobalCte
    xeGlobalCte = [var] + xeGlobalCte

def xeLookup(sym, cte):
    v = S.lookup(sym, cte)
    if v:
        return v

    v = xeLookupGlobalCte(sym)
    if v:
        return v

    v = S.newGlobalVar(sym)
    xeAddToGlobalCte(v)
    return v

xeGlobalCte = makeInitialCte()

def parseSchemeString(s):
    sPrime = '(begin {})'.format(s)
    return P.parse(sPrime)

def parse(input):
    p = parseSchemeString(input)
    a = xe(p, [])
    return a
