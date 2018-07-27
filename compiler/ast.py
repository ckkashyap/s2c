BINDING = "BINDING"
VAR = "VAR"
MACRO = "MACRO"

AST = "AST"
LIT = "LIT"
REF = "REF"
SET = "SET"
CND = "CND"
PRIM = "PRIM"
APP = "APP"
LAM = "LAM"
SEQ = "SEQ"

def bindingTag(x):
    return x[0]
def bindingType(x):
    return x[1]
def astTag(x):
    return x[0]
def astType(x):
    return x[1]
def astSubx(x):
    return x[2]

def makeLit(subx, val):
    return [AST, LIT, subx, val]
def litVal(x):
    return x[3]
def isLit (x):
    return isinstance(x, list) and (len(x)==4) and (astTag(x) == AST) and (astType(x) == LIT)

def makeRef (subx, var):
    return [AST, REF, subx, var]
def refVar (x):
    return x[3]
def isRef (x):
    return isinstance(x, list) and (len(x)==4) and (astTag(x) == AST) and (astType(x) == REF)

def makeSet (subx, var):
    return [AST, SET, subx, var]
def setVar (x): 
    return x[3]
def isSetClj (x):
    return isinstance(x, list) and (len(x)==4) and (astTag(x) == AST) and (astType(x) == SET)

def makeCnd (subx):
    return [AST, CND, subx]
def isCnd (x):
    return isinstance(x, list) and (len(x)==3) and (astTag(x) == AST) and (astType(x) == CND)

def makePrim (subx, op):
    return [AST, PRIM, subx, op]
def primOp (x): 
    return x[3]
def isPrim (x):
    return isinstance(x, list) and (len(x)==4) and (astTag(x) == AST) and (astType(x) == PRIM)

def makeApp (subx):
    return [AST, APP, subx]
def isApp (x):
    return isinstance(x, list) and (len(x)==3) and (astTag(x) == AST) and (astType(x) == APP)

def makeLam (subx, params):
    return [AST, LAM, subx, params]
def lamParams (x):
    return x[3]
def isLam (x):
    return isinstance(x, list) and (len(x)==4) and (astTag(x) == AST) and (astType(x) == LAM)

def makeSeq (subx):
    return [AST, SEQ, subx]
def isSeqClj (x):
    return isinstance(x, list) and (len(x)==3) and (astTag(x) == AST) and (astType(x) == SEQ)

def makeMacro (identifier, expander):
    return [BINDING, MACRO, identifier, expander]
def macroExpander (b): 
    return b[3]
def isMacro (x):
    return isinstance(x, list) and (len(x)==4) and (bindingTag(x) == BINDING) and (bindingType(x) == MACRO)

def makeVar (identifier, uid):
    return [BINDING, VAR, identifier, uid]
def varUid (b):
    return b[3]
def isVarClj (x):
    return isinstance(x, list) and (len(x)==4) and (bindingTag(x) == BINDING) and (bindingType(x) == VAR)

def isBooleanClj (e):
    return type(e) == type(True)
def isConstExpr (e):
   return isBooleanClj(e) or type(e) == type(1)
def isIdentExpr (e):
    return type(e) == type("")
def isFormExpr (e):
    return (isinstance(e, list) and len(e) > 0)
