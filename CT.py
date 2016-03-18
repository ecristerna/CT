import sys

sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

literals = ['{','}',',',';','=','(',')','[', ']', '>', '<', '+','-','*','/', ':', '.']
reserved = ['PROGRAM','STRUCT','DICT','FUNC','RETURNS','RETURN','INT', 'FLOAT', 'STRING', 'BOOL', 'TRUE', 'FALSE', 'VARS', 'MAIN', 'AND', 'OR', 'WHILE', 'FOR', 'IF', 'ELSE', 'FIRST', 'LAST',]
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

# Addresses

MIN_INT = 1000
MAX_INT = 1999
MIN_FLOAT = 2000
MAX_FLOAT = 2999
MIN_BOOL = 3000
MAX_BOOL = 3999
MIN_STRING = 4000
MAX_STRING = 4999
MIN_TEMP = 5000
MAX_TEMP = 6999
MIN_CONST = 7000
MAX_CONST= 9999

contInt = MIN_INT
contFloat = MIN_FLOAT
contBool = MIN_BOOL
contString = MIN_STRING
contTemp = MIN_TEMP
contConst = MIN_CONST

# Types & Operators Codes

INT = 10
FLOAT = 20
BOOL = 30
STRING = 40
ERROR = 50

ADD = 100
SUBSTRACT = 110
MULTIPLY = 120
DIVISION = 130
LESS_THAN = 140
GREATER_TAN = 150
LESS_EQUAL = 160
GREATER_EQUAL = 170
EQUAL = 180
DIFFERENT = 190
AND = 200
OR = 210
ASSIGN = 220

# Semantic Cube

			# 	 +	   	 -      *      /      <      >     <=     >=     ==     !=     AND    OR     =   
semanticCube = [[INT,   INT,   INT,   INT,   BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  ERROR, ERROR, INT], 	 # Int vs Int
                [FLOAT, FLOAT, FLOAT, FLOAT, BOOL, 	BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  ERROR, ERROR, ERROR], # Int vs Float
                [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # Int vs Bool
                [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # Int vs String
                [FLOAT, FLOAT, FLOAT, FLOAT, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, FLOAT], # Float vs Int
                [FLOAT, FLOAT, FLOAT, FLOAT, BOOL, 	BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  ERROR, ERROR, FLOAT], # Float vs Float
                [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # Float vs Bool
                [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # Float vs String
                [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # Bool vs Int
                [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # Bool vs Float
                [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, BOOL,  BOOL,  BOOL,  BOOL,  BOOL ], # Bool vs Bool
                [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # Bool vs String
                [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # String vs Int
                [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # String vs Float
                [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # String vs Bool
                [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, BOOL,  BOOL,  ERROR, ERROR, STRING]]# String vs String 

# Instructions Matrix

cuadruplos = []

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
    '''program : errorProgram PROGRAM saveType ID saveProc "{" opVars changeCurrentScope opFunctions main "}" printTables'''
    # print("program")

def p_changeCurrentScope(p):
    '''changeCurrentScope : '''
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
	# print("optional vars")


def p_opFunctions(p):
	'''opFunctions : function opFunctions
				| empty'''


def p_vars(p):
	'''vars : errorVars VARS declare '''
	# print("vars")


def p_saveID(p):
	'''saveID : '''
	global currentScope
	global currentType
	global currentToken
	global semanticError
	if currentScope is "global":
		global vars_global
		if currentToken in vars_global:
			semanticError = "Varibale '" + currentToken + "' already declared"
			semanticErrorHalt()
		else:
			vars_global[currentToken] = getAdressForType(currentType)
	else:
		global vars_local
		if currentToken in vars_local:
			semanticError = "Variable '" + currentToken + "' already declared on this scope"
			semanticErrorHalt()
		else:
			vars_local[currentToken] = getAdressForType(currentType)

def semanticErrorHalt():
	global semanticError
	global currentToken
	global line
	print("Semantic Error: " + semanticError)
	print("Line: %d" % line)
	sys.exit()

def p_errorVars(p):
	'''errorVars : '''
	global errorMsg
	errorMsg = "Error in rule VARS"


def p_type(p):
	'''type : errorType INT
			| FLOAT
			| STRING
			| BOOL'''
	# print("type")


def p_errorType(p):
	'''errorType : '''
	global errorMsg
	errorMsg = "Error in rule TYPE"


def p_main(p):
	'''main : errorMain MAIN saveMain "{" opVars body "}" clearVarsTable'''
	# print("main")

def p_saveMain(p):
	'''saveMain : '''
	global dir_procs
	global currentToken
	newProc = [currentToken, "main", None, None, vars_local]
	dir_procs += [newProc]


def p_errorMain(p):
	'''errorMain : '''
	global errorMsg
	errorMsg = "Error in rule MAIN"


def p_instr(p):
	'''instr : basicStatements ";"
			| condition
			| cycle '''
	# print("instr")

def p_basicStatements(p):
	'''basicStatements : assign
					| funcCall '''


def p_declare(p):
	'''declare : basicDeclare
			| structDeclare
			| dictDeclare '''
	# print("declare")


def p_init(p):
	'''init : "=" initWith errorInit'''
	# print("init")


def p_errorInit(p):
	'''errorInit : '''
	global errorMsg
	errorMsg = "Error in rule INIT"


def p_initWith(p):
	'''initWith : expresion
		| funcCall '''
	# print("init with")


def p_initDict(p):
	'''initDict : "=" "(" dictType ":" dictType ")" errorInitDict'''
	# print("initDict")


def p_errorInitDict(p):
	'''errorInitDict : '''
	global errorMsg
	errorMsg = "Error in rule INITDICT"


def p_dictType(p):
	'''dictType : errorDictType CTES
				| cte
				| ID '''
	# print("dict type")


def p_errorDictType(p):
	'''errorDictType : '''
	global errorMsg
	errorMsg = "Error in rule DICTTYPE. Dictionary not initialized."


def p_param(p):
	'''param : saveType type errorParam ID cyTypeParam cyParam '''
	# print("param")


def p_errorParam(p):
	'''errorParam : '''
	global errorMsg
	errorMsg = "Error in rule PARAM"


def p_cyParam(p):
	'''cyParam : errorCyParam saveID saveTypeParam ";"  param
		| empty saveID saveTypeParam'''
	# print("cycle param")


def p_cyTypeParam(p):
	'''cyTypeParam : "," saveID saveTypeParam ID cyTypeParam
		| empty '''
	# print("cycle type param")

def p_saveTypeParam(p):
        '''saveTypeParam : '''
        global declaringParameters
        if declaringParameters:
            global currenType
            global param_types
            param_types.append(typeToCode(currentType))


def p_errorCyParam(p):
	'''errorCyParam : '''
	global errorMsg
	errorMsg = "Error in rule CYPARAM. Missing ; "


def p_function(p):
	'''function : errorFunction FUNC saveType ID saveProc flagParameters "(" opParameters ")" flagParameters opReturns  "}" clearVarsTable '''
	# print("function")

def p_errorFunction(p):
	'''errorFunction : '''
	global errorMsg
	errorMsg = "Error in rule FUNCTION"

def p_clearVarsTable(p):
    '''clearVarsTable : '''
    global vars_local
    print
    print("=========================================================")
    print("This is VARS LOCAL --> ")
    print(vars_local)
    print("=========================================================")
    print
    vars_local = {}

def p_return(p):
	'''return : errorReturn RETURN expresion ";" '''
	# print("return")


def p_errorReturn(p):
	'''errorReturn : '''
	global errorMsg
	errorMsg = "Error in rule RETURN"


def p_opParameters(p):
	'''opParameters : param saveParamToDirProc errorOpParameters
					| empty '''
	# print("optional parameters")

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
	# print("returns")


def p_saveReturnType(p):
	'''saveReturnType : '''
	global dir_procs
	global currentToken
	dir_procs[len(dir_procs) - 1][3] = typeToCode(currentToken)

def p_errorOpReturns(p):
	'''errorOpReturns : '''
	global errorMsg
	errorMsg = "Error in rule OPRETURNS"


def p_basicDeclare(p):
	'''basicDeclare : saveType type errorBasicDeclare ID cyTypeParam saveID ";" cyDeclare '''
	# print("basic declare")


def p_errorBasicDeclare(p):
	'''errorBasicDeclare : '''
	global errorMsg
	errorMsg = "Error in rule BASICDECLARE"


def p_structDeclare(p):
	'''structDeclare : errorStructDeclare STRUCT ID struct ";" cyDeclare '''
	# print("struct declare")


def p_errorStructDeclare(p):
	'''errorStructDeclare : '''
	global errorMsg
	errorMsg = "Error in rule STRUCTDECLARE"


def p_dictDeclare(p):
	'''dictDeclare : errorDictDeclare DICT ID dict ";" cyDeclare '''
	# print("dict declare")


def p_errorDictDeclare(p):
	'''errorDictDeclare : '''
	global errorMsg
	errorMsg = "Error in rule DICTDECLARE"


def p_cyDeclare(p):
	'''cyDeclare : declare
		| empty '''
	# print("cycle declare")


def p_body(p):
	'''body : errorBody cyInstruction
			| empty '''
	# print("body")


def p_errorBody(p):
	'''errorBody : '''
	global errorMsg
	errorMsg = "Error in rule BODY"


def p_cyInstruction(p):
	'''cyInstruction : instr body '''
	# print("cycleInstruction")


def p_cycle(p):
	'''cycle : forCycle
			| whileCycle '''
	# print("cycle")


def p_whileCycle(p):
	'''whileCycle : errorWhileCycle WHILE "(" expresion ")" "{" body "}" '''
	# print("while")


def p_errorWhileCycle(p):
	'''errorWhileCycle : '''
	global errorMsg
	errorMsg = "Error in rule WHILECYCLE"


def p_forCycle(p):
	'''forCycle : errorForCycle FOR "(" assign ";" expresion ";" assign ")" "{" body "}" '''
	# print("for")


def p_errorForCycle(p):
	'''errorForCycle : '''
	global errorMsg
	errorMsg = "Error in rule FORCYCLE"


def p_assign(p):
	'''assign :  ID errorAssign assignOptions '''
	# print("assign")


def p_errorAssign(p):
	'''errorAssign : '''
	global errorMsg
	errorMsg = "Error in rule ASSIGN"


def p_assignOptions(p):
	'''assignOptions : init
					| initDict
					| "[" expresion "]" assignMatrix init '''
	# print("assignOptions")


def p_assignMatrix(p):
	'''assignMatrix : "[" expresion "]" errorAssignMatrix
					| empty '''
	# print("assignMatrix")


def p_errorAssignMatrix(p):
	'''errorAssignMatrix : '''
	global errorMsg
	errorMsg = "Error in rule ASSIGNMATRIX"


def p_funcCall(p):
	'''funcCall : ID "(" opParamCall ")" '''
	# print("funcCall")


def p_opParamCall(p):
	'''opParamCall : expresion cyParamCall
				| empty '''
	# print("function parameter")


def p_cyParamCall(p):
	'''cyParamCall : "," expresion cyParamCall
				| empty '''
	# print("cycle parameter call")


def p_struct(p):
	'''struct : structType "[" CTED "]" optionalMatrix '''
	# print("struct")


def p_structType(p):
	'''structType : type
				| DICT dict '''
	# print("struct type")


def p_optionalMatrix(p):
	'''optionalMatrix : "[" CTED "]"
					| empty '''
	# print("matrix")


def p_condition(p):
	'''condition : errorCondition IF "(" expresion ")" "{" body "}" optionalElse '''
	# print("condition")


def p_errorCondition(p):
	'''errorCondition : '''
	global errorMsg
	errorMsg = "Error in rule CONDITION"


def p_optionalElse(p):
	'''optionalElse : errorElse ELSE "{" body "}"
					| empty '''
	# print("else")


def p_errorElse(p):
	'''errorElse : '''
	global errorMsg
	errorMsg = "Error in rule OPTIONALELSE"


def p_dict(p):
	'''dict : errorDict "(" type ":" type ")" '''
	# print("dict")


def p_errorDict(p):
	'''errorDict : '''
	global errorMsg
	errorMsg = "Error in rule DICT"


def p_expresion(p):
	'''expresion : sExp cyExpresion errorExpresion '''
	# print("expresion")


def p_errorExpresion(p):
	'''errorExpresion : '''
	global errorMsg
	errorMsg = "Error in rule EXPRESION"


def p_cyExpresion(p):
	'''cyExpresion : AND expresion
				| OR expresion
				| empty '''
	# print("cycle expresion")


def p_sExp(p):
	'''sExp : exp errorOpSExp opSExp '''
	# print("super expresion")


def p_opSExp(p):
	'''opSExp :  EQ exp
			| DIF exp
			| LTOEQ exp
			| GTOEQ exp
			| ">" exp
			| "<" exp
			| empty '''
	# print("cycle super expresion")


def p_errorOpSExp(p):
	'''errorOpSExp : '''
	global errorMsg
	errorMsg = "Error in rule OPSEXP"


def p_exp(p):
	'''exp : term errorCyExp cyExp '''
	# print("exp")


def p_cyExp(p):
	'''cyExp : "+" term
			| "-" term
			| empty '''
	# print("cycle exp")


def p_errorCyExp(p):
	'''errorCyExp : '''
	global errorMsg
	errorMsg = "Error in rule CYEXP"


def p_term(p):
	'''term : fact cyTerm '''
	# print("term")


def p_cyTerm(p):
	'''cyTerm : "*" errorFact fact
			| "/" fact
			| empty '''
	# print("cycle term")


def p_fact(p):
	'''fact : CTES
			| cte
			| funcCall
			| "(" expresion ")"
			| ID opAccess errorOpAccess'''
	# print("fact")


def p_errorFact(p):
	'''errorFact : '''
	global errorMsg
	errorMsg = "Error in rule ERRORFACT"


def p_opAccess(p):
	'''opAccess : opStruct
				| opDictionary
				| empty '''
	# print("optional access")


def p_errorOpAccess(p):
	'''errorOpAccess : '''
	global errorMsg
	errorMsg = "Error in rule ERROROPACCESS"


def p_opStruct(p):
	'''opStruct : errorOpStruct "[" expresion "]" opMatrix '''
	# print("optional struct")


def p_errorOpStruct(p):
	'''errorOpStruct : '''
	global errorMsg
	errorMsg = "Error in rule OPSTRUCT"


def p_opMatrix(p):
	'''opMatrix : errorOpMatrix "[" expresion "]"
				| empty '''
	# print("optional matrix")


def p_errorOpMatrix(p):
	'''errorOpMatrix : '''
	global errorMsg
	errorMsg = "Error in rule ERROROPMATRIX"


def p_opDictionary(p):
	'''opDictionary : "." dictIndex '''
	# print("optional dictionary")


def p_dictIndex(p):
	'''dictIndex : FIRST
				| LAST '''
	# print("dictionary index")


def p_cte(p):
	'''cte : CTED
		| CTEF
		| TRUE
		| FALSE '''
	# print("cte")


def p_empty(p):
    '''empty : '''
    # print("EMPTY")


def p_printTables(p):
	'''printTables : '''
	# global semanticCube
	print
	print("=========================================================")
	print("This is DIR PROCS --> ")
	print(dir_procs)
	print("=========================================================")
	print
	print
	print("=========================================================")
	print("This is VARS GLOBAL --> ")
	print(vars_global)
	print("=========================================================")
	print
	print(cuadruplos)
	print(typesValidator(BOOL, BOOL, EQUAL))

def p_error(p):
	global line
	global errorMsg
	print("Error in line %d: Unexpected token '%s'" % (line, p.value))
	print('%s' % errorMsg)
	sys.exit()

def typeToCode(type):
    switcher = {
        "int": 10,
        "float": 20,
        "bool": 30,
        "string": 40,
    }
    return switcher.get(type, 50)

def getAdressForType(type):
	global contInt
	global contFloat
	global contBool
	global contString

	typeCode = typeToCode(type)
	
	if typeCode is INT:
		contInt += 1
		return contInt - 1

	if typeCode is FLOAT:
		contFloat += 1
		return contFloat - 1

	if typeCode is BOOL:
		contBool += 1
		return contBool - 1

	if typeCode is STRING:
		contString += 1
		return contString - 1

def typesValidator(left, right, operator):
	opMap = operator / 10 % 10

	if operator >= 200:
		opMap += 10
	
	return semanticCube[(left / 10 - 1) * 4 + (right / 10 - 1)][opMap]


import ply.yacc as yacc
parser = yacc.yacc()

file = open ("input.txt", "r");
yacc.parse(file.read())
