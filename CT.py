import sys

sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

literals = ['{','}',',',';','=','(',')','[', ']', '>', '<', '+','-','*','/', ':', '.']
reserved = ['PROGRAM','STRUCT','DICT','FUNC','RETURNS','RETURN','INT', 'FLOAT', 'STRING', 'OBJECT', 'BOOL', 'TRUE', 'FALSE', 'VARS', 'MAIN', 'AND', 'OR', 'WHILE', 'FOR', 'IF', 'ELSE', 'FIRST', 'LAST',]
tokens = ['GTOEQ', 'LTOEQ','DIF', 'EQ','ID','CTED','CTEF','CTES',] + reserved

line = 1
errorMsg = ""
currentScope = "global"
vars_global = {}
vars_local = {}
dir_procs = []
param_types = []
currentType = ""
currentTable = ""
currentToken = ""
semanticError = ""
declaringParameters = False

# Tokens

t_ignore = " \t"
t_DIF = "!="
t_EQ = "=="
t_GTOEQ = ">="
t_LTOEQ = "<="

def t_CTEF(t):
    r'(\d+)(\.\d+)'
    t.value = float(t.value)
    global currentToken
    currentToken = t.value
    return t

def t_CTED(t):
	r'\d+'
	t.value = int(t.value)
	global currentToken
	currentToken = t.value
	return t

def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value,"ID")
    global currentToken
    currentToken = t.value
    return t

def t_CTES(t):
    r'\"([^\\\n]|(\\.))*?\"'
    global currentToken
    currentToken = t.value
    return t


reserved_map = { }
for r in reserved:
    reserved_map[r.lower()] = r

def t_newline(t):
    r'\n'
    global line
    line += 1

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

def p_program(p):
    '''program : errorProgram PROGRAM saveType ID saveProc "{" opVars changeCurrentScope opFunctions main "}"'''
    print("program")

def p_changeCurrentScope(p):
    '''changeCurrentScope : '''
    print("Enter Change Current")
    global currentScope
    currentScope = "local"

def p_saveType(p):
	'''saveType : '''
	global currentScope
	global currentToken
	global currentType
	currentType = currentToken

def p_saveProc(p):
	'''saveProc : '''
	global dir_procs
	global currentScope
	global currentType
	global currentToken
	for proc in dir_procs:
		if proc[0] is currentToken:
			global semanticError
			semanticError = "Function '" + currentToken + "' already declared"
			semanticErrorHalt()
	if currentScope is "global":
		newProc = [currentToken, currentType, None, None, vars_global]
	else:
		newProc = [currentToken, currentType, None, None, vars_local]
	dir_procs += [newProc]

def p_errorProgram(p):
	'''errorProgram : '''
	global errorMsg
	errorMsg = "Error in rule PROGRAM"
	

def p_opVars(p):
	'''opVars : vars
			| empty'''
	print("optional vars")
	

def p_opFunctions(p):
	'''opFunctions : function opFunctions
				| empty'''
	

def p_vars(p):
	'''vars : errorVars VARS declare '''
	print("vars")
	

def p_saveID(p):
	'''saveID : '''
	global currentScope
	global vars_global
	global vars_local
	global currentType
	global currentToken
	print("CURRENT SCOPE ---- " + currentScope)
	if currentScope is "global":
		if currentToken in vars_global:
			global semanticError
			semanticError = "Varibale '" + currentToken + "' already declared"
			semanticErrorHalt()
		else:
			vars_global[currentToken] = currentType
	else:
		if currentToken in vars_local:
			global semanticError
			semanticError = "Variable '" + currentToken + "' already declared on this scope"
			semanticErrorHalt()
		else:
			vars_local[currentToken] = currentType

def semanticErrorHalt():
	global semanticError
	global currentToken
	print("Semantic Error: " + semanticError)
	sys.exit()

def p_errorVars(p):
	'''errorVars : '''
	global errorMsg
	errorMsg = "Error in rule VARS"
	

def p_type(p):
	'''type : errorType INT
			| FLOAT
			| STRING
			| OBJECT
			| BOOL'''
	print("type")


def p_errorType(p):
	'''errorType : '''
	global errorMsg
	errorMsg = "Error in rule TYPE"
	

def p_main(p):
	'''main : errorMain MAIN saveMain "{" opVars body "}"'''
	print("main")

def p_saveMain(p):
	'''saveMain : '''
	global dir_procs
	global currentToken
	newProc = [currentToken, "main", None, None, None]
	dir_procs += [newProc]
	

def p_errorMain(p):
	'''errorMain : '''
	global errorMsg
	errorMsg = "Error in rule MAIN"
	

def p_instr(p):
	'''instr : basicStatements ";"
			| condition
			| cycle '''
	print("instr")
	
def p_basicStatements(p):
	'''basicStatements : assign
					| funcCall '''
	

def p_declare(p):
	'''declare : basicDeclare
			| structDeclare
			| dictDeclare '''
	print("declare")
	

def p_init(p):
	'''init : "=" initWith errorInit'''
	print("init")
	

def p_errorInit(p):
	'''errorInit : '''
	global errorMsg
	errorMsg = "Error in rule INIT"
	

def p_initWith(p):
	'''initWith : expresion
		| funcCall '''
	print("init with")
	

def p_initDict(p):
	'''initDict : "=" "(" dictType ":" dictType ")" errorInitDict'''
	print("initDict")
	

def p_errorInitDict(p):
	'''errorInitDict : '''
	global errorMsg
	errorMsg = "Error in rule INITDICT"
	

def p_dictType(p):
	'''dictType : errorDictType CTES
				| cte
				| ID '''
	print("dict type")
	

def p_errorDictType(p):
	'''errorDictType : '''
	global errorMsg
	errorMsg = "Error in rule DICTTYPE. Dictionary not initialized."
	

def p_param(p):
	'''param : saveType type errorParam ID cyTypeParam cyParam '''
	print("param")
	

def p_errorParam(p):
	'''errorParam : '''
	global errorMsg
	errorMsg = "Error in rule PARAM"
	

def p_cyParam(p):
	'''cyParam : errorCyParam saveID saveTypeParam ";"  param
		| empty saveID saveTypeParam'''
	print("cycle param")
	

def p_cyTypeParam(p):
	'''cyTypeParam : "," saveID saveTypeParam ID cyTypeParam
		| empty '''
	print("cycle type param")

def p_saveTypeParam(p):
        '''saveTypeParam : '''
        global declaringParameters 
        if declaringParameters:
            global currenType
            global param_types
            param_types.append(currentType)


def p_errorCyParam(p):
	'''errorCyParam : '''
	global errorMsg
	errorMsg = "Error in rule CYPARAM. Missing ; "
	

def p_function(p):
	'''function : errorFunction FUNC saveType ID saveProc flagParameters "(" opParameters ")" flagParameters opReturns  "}" clearVarsTable '''
	print("function")

def p_errorFunction(p):
	'''errorFunction : '''
	global errorMsg
	errorMsg = "Error in rule FUNCTION"

def p_clearVarsTable(p):
    '''clearVarsTable : '''
    global vars_local
    print("This is VARS LOCAL --> ")
    print(vars_local)
    print("=========================================================")
    vars_local = {}

def p_return(p):
	'''return : errorReturn RETURN expresion ";" '''
	print("return")
	

def p_errorReturn(p):
	'''errorReturn : '''
	global errorMsg
	errorMsg = "Error in rule RETURN"
	

def p_opParameters(p):
	'''opParameters : param saveParamToDirProc errorOpParameters
					| empty '''
	print("optional parameters")

def p_flagParameters(p):
    '''flagParameters : '''
    global declaringParameters
    declaringParameters = not declaringParameters

def p_saveParamToDirProc(p):
        '''saveParamToDirProc : '''
        global param_types
        global dir_procs
        dir_procs[len(dir_procs) - 1][2] = param_types
        param_types = []
 

def p_errorOpParameters(p):
	'''errorOpParameters : '''
	global errorMsg
	errorMsg = "Error in rule OPPARAMETERS"
	

def p_opReturns(p):
	'''opReturns : errorOpReturns RETURNS type saveReturnType "{" opVars body return
		| "{" opVars body '''
	print("returns")
	

def p_saveReturnType(p):
	'''saveReturnType : '''
	global dir_procs
	global currentToken
	dir_procs[len(dir_procs) - 1][3] = currentToken

def p_errorOpReturns(p):
	'''errorOpReturns : '''
	global errorMsg
	errorMsg = "Error in rule OPRETURNS"
	

def p_basicDeclare(p):
	'''basicDeclare : saveType type errorBasicDeclare ID cyTypeParam saveID ";" cyDeclare '''
	print("basic declare")
	

def p_errorBasicDeclare(p):
	'''errorBasicDeclare : '''
	global errorMsg
	errorMsg = "Error in rule BASICDECLARE"
	

def p_structDeclare(p):
	'''structDeclare : errorStructDeclare STRUCT ID struct ";" cyDeclare '''
	print("struct declare")
	

def p_errorStructDeclare(p):
	'''errorStructDeclare : '''
	global errorMsg
	errorMsg = "Error in rule STRUCTDECLARE"
	

def p_dictDeclare(p):
	'''dictDeclare : errorDictDeclare DICT ID dict ";" cyDeclare '''
	print("dict declare")
	

def p_errorDictDeclare(p):
	'''errorDictDeclare : '''
	global errorMsg
	errorMsg = "Error in rule DICTDECLARE"
	

def p_cyDeclare(p):
	'''cyDeclare : declare
		| empty '''
	print("cycle declare")
	

def p_body(p):
	'''body : errorBody cyInstruction
			| empty '''
	print("body")
	

def p_errorBody(p):
	'''errorBody : '''
	global errorMsg
	errorMsg = "Error in rule BODY"
	

def p_cyInstruction(p):
	'''cyInstruction : instr body '''
	print("cycleInstruction")
	

def p_cycle(p):
	'''cycle : forCycle
			| whileCycle '''
	print("cycle")
	

def p_whileCycle(p):
	'''whileCycle : errorWhileCycle WHILE "(" expresion ")" "{" body "}" '''
	print("while")
	

def p_errorWhileCycle(p):
	'''errorWhileCycle : '''
	global errorMsg
	errorMsg = "Error in rule WHILECYCLE"
	

def p_forCycle(p):
	'''forCycle : errorForCycle FOR "(" assign ";" expresion ";" assign ")" "{" body "}" '''
	print("for")
	

def p_errorForCycle(p):
	'''errorForCycle : '''
	global errorMsg
	errorMsg = "Error in rule FORCYCLE"
	

def p_assign(p):
	'''assign :  ID errorAssign assignOptions '''
	print("assign")
	
    
def p_errorAssign(p):
	'''errorAssign : '''
	global errorMsg
	errorMsg = "Error in rule ASSIGN"
	

def p_assignOptions(p):
	'''assignOptions : init
					| initDict
					| "[" expresion "]" assignMatrix init '''
	print("assignOptions")
	

def p_assignMatrix(p):
	'''assignMatrix : "[" expresion "]" errorAssignMatrix
					| empty '''
	print("assignMatrix")
	

def p_errorAssignMatrix(p):
	'''errorAssignMatrix : '''
	global errorMsg
	errorMsg = "Error in rule ASSIGNMATRIX"
	

def p_funcCall(p):
	'''funcCall : ID "(" opParamCall ")" '''
	print("funcCall")
	

def p_opParamCall(p):
	'''opParamCall : expresion cyParamCall
				| empty '''
	print("function parameter")
	

def p_cyParamCall(p):
	'''cyParamCall : "," expresion cyParamCall
				| empty '''
	print("cycle parameter call")
	

def p_struct(p):
	'''struct : structType "[" CTED "]" optionalMatrix '''
	print("struct")
	

def p_structType(p):
	'''structType : type
				| DICT dict '''
	print("struct type")
	

def p_optionalMatrix(p):
	'''optionalMatrix : "[" CTED "]"
					| empty '''
	print("matrix")
	

def p_condition(p):
	'''condition : errorCondition IF "(" expresion ")" "{" body "}" optionalElse '''
	print("condition")
	

def p_errorCondition(p):
	'''errorCondition : '''
	global errorMsg
	errorMsg = "Error in rule CONDITION"
	

def p_optionalElse(p):
	'''optionalElse : errorElse ELSE "{" body "}"
					| empty '''
	print("else")
	

def p_errorElse(p):
	'''errorElse : '''
	global errorMsg
	errorMsg = "Error in rule OPTIONALELSE"
	

def p_dict(p):
	'''dict : errorDict "(" type ":" type ")" '''
	print("dict")
	

def p_errorDict(p):
	'''errorDict : '''
	global errorMsg
	errorMsg = "Error in rule DICT"
	

def p_expresion(p):
	'''expresion : sExp cyExpresion errorExpresion '''
	print("expresion")
	

def p_errorExpresion(p):
	'''errorExpresion : '''
	global errorMsg
	errorMsg = "Error in rule EXPRESION"
	

def p_cyExpresion(p):
	'''cyExpresion : AND expresion
				| OR expresion
				| empty '''
	print("cycle expresion")
	

def p_sExp(p):
	'''sExp : exp errorOpSExp opSExp '''
	print("super expresion")
	

def p_opSExp(p):
	'''opSExp :  EQ exp
			| DIF exp
			| LTOEQ exp
			| GTOEQ exp
			| ">" exp
			| "<" exp
			| empty '''
	print("cycle super expresion")
	

def p_errorOpSExp(p):
	'''errorOpSExp : '''
	global errorMsg
	errorMsg = "Error in rule OPSEXP"
	

def p_exp(p):
	'''exp : term errorCyExp cyExp '''
	print("exp")
	

def p_cyExp(p):
	'''cyExp : "+" term
			| "-" term
			| empty '''
	print("cycle exp")
	

def p_errorCyExp(p):
	'''errorCyExp : '''
	global errorMsg
	errorMsg = "Error in rule CYEXP"
	

def p_term(p):
	'''term : fact cyTerm '''
	print("term")
	

def p_cyTerm(p):
	'''cyTerm : "*" errorFact fact
			| "/" fact
			| empty '''
	print("cycle term")
	

def p_fact(p):
	'''fact : CTES
			| cte
			| funcCall
			| "(" expresion ")"
			| ID opAccess errorOpAccess'''
	print("fact")

		
def p_errorFact(p):
	'''errorFact : '''
	global errorMsg
	errorMsg = "Error in rule ERRORFACT"
	

def p_opAccess(p):
	'''opAccess : opStruct
				| opDictionary
				| empty '''
	print("optional access")
	

def p_errorOpAccess(p):
	'''errorOpAccess : '''
	global errorMsg
	errorMsg = "Error in rule ERROROPACCESS"
	

def p_opStruct(p):
	'''opStruct : errorOpStruct "[" expresion "]" opMatrix '''
	print("optional struct")
	

def p_errorOpStruct(p):
	'''errorOpStruct : '''
	global errorMsg
	errorMsg = "Error in rule OPSTRUCT"
	

def p_opMatrix(p):
	'''opMatrix : errorOpMatrix "[" expresion "]"
				| empty '''
	print("optional matrix")
	

def p_errorOpMatrix(p):
	'''errorOpMatrix : '''
	global errorMsg
	errorMsg = "Error in rule ERROROPMATRIX"
	

def p_opDictionary(p):
	'''opDictionary : "." dictIndex '''
	print("optional dictionary")
	

def p_dictIndex(p):
	'''dictIndex : FIRST
				| LAST '''
	print("dictionary index")
	

def p_cte(p):
	'''cte : CTED
		| CTEF 
		| TRUE 
		| FALSE '''
	print("cte")
	global currentToken
	print(currentToken)
	

def p_empty(p):
    '''empty : '''
    print("EMPTY")
    

def p_error(p):
	global line
	global errorMsg
	global currentScope
	global currentType
	print("Error in line %d: Unexpected token '%s'" % (line, p.value))
	print('%s' % errorMsg)
	print
	print("=========================================================")
	print("This is DIR PROCS --> ")
	print(dir_procs)
	print("=========================================================")
	print("This is VARS GLOBAL --> ")
	print(vars_global)
	print("=========================================================")
	print("This is VARS LOCAL --> ")
	print(vars_local)
	print("=========================================================")
	print

	sys.exit()

import ply.yacc as yacc
parser = yacc.yacc()

file = open ("input3.txt", "r");
yacc.parse(file.read())
