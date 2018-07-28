from . import ast as A
from . import parse as P
from . import symbol as S

def interval (n, m):
    return range (n, m + 1)
 
lambdaTodo = list()
lambdaCount = 0
globalVars = list()

def addLambda(lam):
    global lambdaTodo, lambdaCount
    i = lambdaCount
    lambdaTodo = [[i] + lam] + lambdaTodo
    lambdaCount = i + 1
    return lambdaCount - 1

def cgList (asts, vrs, stackEnv, sep, cont):
    if asts:
        x = codeGen(asts[0], stackEnv)
        return cgList(asts[1:], vrs[1:], [vrs[0]] + stackEnv, sep, lambda code, sv: cont([x, sep, code], sv))
    else:
        return cont("", stackEnv)
 
def cgArgs (args, stackEnv):
    return cgList(args, interval(1, len(args)), stackEnv, "", lambda code, sv: code)
 
def accessVar(v, stackEnv):
    global globalVars
    if S.isGlobalVar(v):
        i = S.posInList(v, globalVars)
        return ["GLOBAL(", i, "/*", A.varUid(v), "*/)"]
    else:
        i = len(stackEnv) - S.posInList(v, stackEnv) - 1
        return ["LOCAL(", i, "/*", A.varUid(v), "*/)"]
    
def cg(sv, ast):
    if A.isLit(ast):
        val = A.litVal(ast)
        if (type(val) == type(True)):
            if val:
                return [" PUSH(INT2OBJ(TRUEOBJ));"]
            else:
                return [" PUSH(INT2OBJ(FALSEOBJ));"]
        return [" PUSH(INT2OBJ(", val, "));"]
 
    if A.isRef(ast):
        var = A.refVar(ast)
        return [" PUSH(", accessVar(var, sv), ");"]
 
    if A.isSetClj(ast):
        var = A.setVar(ast)
        return [cg(sv, A.astSubx(ast)[0]), " ", accessVar(var, sv), " = TOS();"]
 
    if A.isCnd(ast):
        x = [cg(sv, i) for i in A.astSubx(ast)]
        return [x[0], "\n if (POP()) {\n", x[1], "\n } else {\n", A.astSubx(x), "\n }"]
 
    if A.isPrim(ast):
        args = A.astSubx(ast)
        op =A.primOp(ast)
        if op == "%=":
            return [cgArgs(args, sv), " EQ();"]
        if op == "%<":
            return [cgArgs(args, sv), " LT();"]
        if op == "%+":
            return [cgArgs(args, sv), " ADD();"]
        if op == "%+3":
            return [cgArgs(args, sv), " ADD3();"]
        if op == "%new-vec":
            return [cgArgs(args, sv), " NEWVEC();"]
        if op == "%print-vec":
            return [cgArgs(args, sv), " PRINTVEC();"]
        if op == "%-":
            return [cgArgs(args, sv), " SUB();"]
        if op == "%*":
            return [cgArgs(args, sv), " MUL();"]
        if op == "%display":
            return [cgArgs(args, sv), " DISPLAY();"]
        if op == "%halt":
            return [cgArgs(args, sv), " HALT();"]
        if op == "%closure":
            i = addLambda(args[0])
            n = len(args) - 1
            s = ["CLOSURE(", i, ",", n, ");"]
            return [cgArgs(args[1:], sv), " BEGIN_", s, [[" INICLO(", i, ");"] for i in reversed(interval(1,n))], " END_", s]
        if op == "%closure-ref":
            i = A.litVal(args[1])
            return [cg(sv, args[0]), " TOS() = CLOSURE_REF(TOS(),", i, ");"]
        print("Unknown primitive")
        exit()
 
    if A.isApp(ast):
        fnc = A.astSubx(ast)[0]
        args = A.astSubx(ast)[1:]
        n = len(args)
        if A.isLam(fnc):
            return cgList(args, A.lamParams(fnc), sv,  "\n", lambda code, newSv:[code, codeGen(A.astSubx(fnc)[0], newSv)])
        else:
            return cgList(
                    args,
                    interval(1, n),
                    sv,
                    "\n",
                    lambda code, newSv: [code, " BEGIN_JUMP(", n, ");", [[" PUSH(LOCAL(", j + len(sv), "));"] for j in interval(0, n - 1)], " END_JUMP(", n, ");"])
 
    print("Cannot handle this AST node")
    exit()
 
def collapse(codeList):
    stack = [codeList]
    output=[]

    while len(stack) > 0:
        cl = stack.pop()
        if cl and isinstance(cl, list):
            if len(cl) > 0:
                stack.append(cl[1:])
                stack.append(cl[0])
            else:
                print("This should not happen")
                exit()
        else:
            x = str(cl)
            if x != "[]":
                output.append(x)

    return str.join('', output)
            
def code2string(codeList):
    return collapse(codeList)

 
def codeGen(ast, sv):
    return cg(sv, ast)
 
def compileAllLambdas():
    global lambdaTodo
    if not lambdaTodo:
        return ""
    else:
        x = lambdaTodo[0]
        ast = x[1:]
        lambdaTodo = lambdaTodo[1:]
        
        return ["case ", x[0], ":\n", codeGen(A.astSubx(ast)[0], [i for i in reversed(A.lamParams(ast))]), "\n\n", compileAllLambdas()]

def codeGenerate(ast):
    global globalVars
    globalVars = S.fv(ast)
    addLambda(ast)
    code = compileAllLambdas()
    x = "#define NB_GLOBALS 1 + " + str(len(globalVars)) + "/*+1 for MSVC*/\n"
    y = "#define MAX_STACK 100 \n\n"

    code = code2string(code)

    with open("compiler/runtime/runtime.c") as f: rt = f.read()
    nrt = str.replace(rt, "//__SCHEME_CODE__", code);

    return x + y + nrt

def codeGenerateDebug(ast):
    global globalVars
    globalVars = S.fv(ast)
    addLambda(ast)
    code = compileAllLambdas()
    x = "#define NB_GLOBALS " + str(len(globalVars)) + "\n"
    y = "#define MAX_STACK 100 \n\n"

    code = code2string(code)

    with open("compiler/runtime/runtime.c") as f: rt = f.read()
    nrt = str.replace(rt, "//__SCHEME_CODE__", code);

    return code
