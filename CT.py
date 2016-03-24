import sys

sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

literals = ['{','}',',',';','[', ']', ':', '.']
reserved = ['PRINT', 'READ', 'PROGRAM','STRUCT','DICT','FUNC','RETURNS','RETURN','INT', 'FLOAT', 'STRING', 'BOOL', 'TRUE', 'FALSE', 'VARS', 'MAIN', 'AND', 'OR', 'WHILE', 'FOR', 'IF', 'ELSE', 'FIRST', 'LAST',]
tokens = ['PARINI', 'PARFIN', 'ASGN', 'LT', 'GT', 'PLUS', 'MINUS', 'MULT', 'DIV', 'GTOEQ', 'LTOEQ','DIF', 'EQ','ID','CTED','CTEF','CTES',] + reserved

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
previousToken = ""
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
MIN_TEMP_INT = 5000
MAX_TEMP_INT = 5999
MIN_TEMP_FLOAT = 6000
MAX_TEMP_FLOAT = 6999
MIN_TEMP_BOOL = 7000
MAX_TEMP_BOOL = 7999
MIN_TEMP_STRING = 8000
MAX_TEMP_STRING = 8999
MIN_CONST_INT = 9000
MAX_CONST_INT= 9199
MIN_CONST_FLOAT = 9200
MAX_CONST_FLOAT= 9399
MIN_CONST_STRING = 9400
MAX_CONST_STRING= 9599
MIN_CONST_BOOL = 9600
MAX_CONST_BOOL= 9799

contInt = MIN_INT
contFloat = MIN_FLOAT
contBool = MIN_BOOL
contString = MIN_STRING
contTempInt = MIN_TEMP_INT
contTempFloat = MIN_TEMP_FLOAT
contTempBool = MIN_TEMP_BOOL
contTempString = MIN_TEMP_STRING
contConstInt = MIN_CONST_INT
contConstFloat = MIN_CONST_FLOAT
contConstString = MIN_CONST_STRING
contConstBool = MIN_CONST_BOOL

contQuadruples = 0

# Types & Operators Codes

INT = 10
FLOAT = 20
BOOL = 30
STRING = 40
ERROR = 50

FONDO_FALSO = 99

ADD = 100
SUBSTRACT = 110
MULTIPLY = 120
DIVISION = 130
LESS_THAN = 140
GREATER_THAN = 150
LESS_EQUAL = 160
GREATER_EQUAL = 170
EQUAL = 180
DIFFERENT = 190
AND = 200
OR = 210
ASSIGN = 220
PRINT = 230
READ = 240
GOTOF = 250
GOTOV = 260
GOTO = 270

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

# Quadruples

cuadruplos = []

# Stacks

pilaO = []
pOper = []
pTipos = []
pSaltos = []

# Tokens

t_ignore = " \t"

def t_PARINI(t):
    r'\('
    global currentToken
    global previousToken
    previousToken = currentToken
    currentToken = '('
    return t

def t_PARFIN(t):
    r'\)'
    global currentToken
    global previousToken
    previousToken = currentToken
    currentToken = ')'
    return t

def t_AND(t):
    r'and'
    global currentToken
    global previousToken
    previousToken = currentToken
    currentToken = 'AND'
    return t

def t_OR(t):
    r'or'
    global currentToken
    global previousToken
    previousToken = currentToken
    currentToken = 'OR'
    return t

def t_CTEF(t):
    r'(\d+)(\.\d+)'
    t.value = float(t.value)
    global currentToken
    global previousToken
    previousToken = currentToken
    currentToken = t.value
    return t

def t_CTED(t):
	r'\d+'
	t.value = int(t.value)
	global currentToken
	global previousToken
	previousToken = currentToken
	currentToken = t.value
	return t

def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value,"ID")
    global currentToken
    global previousToken
    previousToken = currentToken
    currentToken = t.value
    return t

def t_CTES(t):
    r'\"([^\\\n]|(\\.))*?\"'
    global currentToken
    global previousToken
    previousToken = currentToken
    currentToken = t.value
    return t

def t_PLUS(t):
	r'\+'
	global currentToken
	global previousToken
	previousToken = currentToken
	currentToken = '+'
	return t

def t_MINUS(t):
	r'-'
	global currentToken
	global previousToken
	previousToken = currentToken
	currentToken = '-'
	return t

def t_MULT(t):
	r'\*'
	global currentToken
	global previousToken
	previousToken = currentToken
	currentToken = '*'
	return t

def t_DIV(t):
	r'/'
	global currentToken
	global previousToken
	previousToken = currentToken
	currentToken = '/'
	return t

def t_EQ(t):
	r'=='
	global currentToken
	global previousToken
	previousToken = currentToken
	currentToken = '=='
	return t

def t_ASGN(t):
	r'='
	global currentToken
	global previousToken
	previousToken = currentToken
	currentToken = '='
	return t

def t_DIF(t):
	r'!='
	global currentToken
	global previousToken
	previousToken = currentToken
	currentToken = '!='
	return t

def t_GTOEQ(t):
	r'>='
	global currentToken
	global previousToken
	previousToken = currentToken
	currentToken = '>='
	return t

def t_LTOEQ(t):
	r'<='
	global currentToken
	global previousToken
	previousToken = currentToken
	currentToken = '<='
	return t

def t_LT(t):
	r'<'
	global currentToken
	global previousToken
	previousToken = currentToken
	currentToken = '<'
	return t

def t_GT(t):
	r'>'
	global currentToken
	global previousToken
	previousToken = currentToken
	currentToken = '>'
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
		if proc[0] == currentToken:
			global semanticError
			semanticError = "Function '" + currentToken + "' already declared"
			semanticErrorHalt()
	if currentScope == "global":
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
	if currentScope == "global":
		global vars_global
		if currentToken in vars_global:
			semanticError = "Varibale '" + currentToken + "' already declared"
			semanticErrorHalt()
		else:
			vars_global[currentToken] = getAddressForType(currentType)
	else:
		global vars_local
		if currentToken in vars_local:
			semanticError = "Variable '" + currentToken + "' already declared on this scope"
			semanticErrorHalt()
		else:
			vars_local[currentToken] = getAddressForType(currentType)

def semanticErrorHalt():
	global semanticError
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
					| funcCall
					| print
					| read '''

def p_print(p):
	'''print : PRINT PARINI exp performPrint cyPrint PARFIN '''

def p_cyPrint(p):
	'''cyPrint : "," fix exp performPrint cyPrint
				| empty '''

def p_read(p):
	'''read : READ PARINI ID performRead cyRead PARFIN '''

def p_cyRead(p):
	'''cyRead : "," fix ID performRead cyRead
				| empty '''

def p_fix(p):
	'''fix : '''
	global previousToken
	previousToken = ","

def p_declare(p):
	'''declare : basicDeclare
			| structDeclare
			| dictDeclare '''
	# print("declare")


def p_init(p):
	'''init : ASGN saveOperator errorInit initWith '''
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
	'''initDict : ASGN PARINI dictType ":" dictType PARFIN errorInitDict'''
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
	'''function : errorFunction FUNC saveType ID saveProc flagParameters PARINI opParameters PARFIN flagParameters opReturns  "}" clearVarsTable '''
	# print("function")

def p_errorFunction(p):
	'''errorFunction : '''
	global errorMsg
	errorMsg = "Error in rule FUNCTION"

def p_clearVarsTable(p):
    '''clearVarsTable : '''
    global vars_local
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
	'''whileCycle : errorWhileCycle WHILE saveReturn PARINI expresion PARFIN saveFalso "{" body "}" repeatWhile'''
	# print("while")

def p_repeatWhile(p):
	'''repeatWhile : '''
	falso = pSaltos.pop()
	retorno = pSaltos.pop()
	generateJump('s', retorno)
	rellena(falso, contQuadruples)

def p_saveReturn(p):
	'''saveReturn : '''
	pSaltos.append(contQuadruples)

def p_errorWhileCycle(p):
	'''errorWhileCycle : '''
	global errorMsg
	errorMsg = "Error in rule WHILECYCLE"


def p_forCycle(p):
	'''forCycle : errorForCycle FOR PARINI assign ";" saveReturn expresion saveFalso ";" saltoBody assign returnFor PARFIN "{" rellenaBody body "}" returnAssign '''
	# print("for")

def p_saltoBody(p):
	'''saltoBody : '''
	generateJump('s', None)
	pSaltos.append(contQuadruples - 1)
	pSaltos.append(contQuadruples)

def p_returnFor(p):
	'''returnFor : '''
	aux = pSaltos.pop()
	aux2 = pSaltos.pop()
	aux3 = pSaltos.pop()
	
	generateJump('s', pSaltos.pop())

	pSaltos.append(aux3)
	pSaltos.append(aux2)
	pSaltos.append(aux)

def p_rellenaBody(p):
	'''rellenaBody : '''
	aux = pSaltos.pop()
	
	rellena(pSaltos.pop(), contQuadruples)

	pSaltos.append(aux)

def p_returnAssign(p):
	'''returnAssign : '''
	generateJump('s', pSaltos.pop())
	rellena(pSaltos.pop(), contQuadruples)

def p_errorForCycle(p):
	'''errorForCycle : '''
	global errorMsg
	errorMsg = "Error in rule FORCYCLE"


def p_assign(p):
	'''assign : ID saveVariable errorAssign assignOptions performAssign'''
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
	'''funcCall : ID PARINI opParamCall PARFIN '''
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
	'''condition : errorCondition IF PARINI expresion PARFIN saveFalso "{" body "}" optionalElse rellenaFalso '''
	# print("condition")


def p_errorCondition(p):
	'''errorCondition : '''
	global errorMsg
	errorMsg = "Error in rule CONDITION"


def p_optionalElse(p):
	'''optionalElse : errorElse ELSE saveVerdadero "{" body "}"
					| empty '''
	# print("else")


def p_errorElse(p):
	'''errorElse : '''
	global errorMsg
	errorMsg = "Error in rule OPTIONALELSE"


def p_dict(p):
	'''dict : errorDict PARINI type ":" type PARFIN '''
	# print("dict")


def p_errorDict(p):
	'''errorDict : '''
	global errorMsg
	errorMsg = "Error in rule DICT"


def p_expresion(p):
	'''expresion : sExp performAndOr cyExpresion errorExpresion '''
	# print("expresion")



def p_errorExpresion(p):
	'''errorExpresion : '''
	global errorMsg
	errorMsg = "Error in rule EXPRESION"


def p_cyExpresion(p):
	'''cyExpresion : AND saveOperator expresion
				| OR saveOperator expresion
				| empty '''
	# print("cycle expresion")


def p_sExp(p):
	'''sExp : exp errorOpSExp opSExp performRelational'''
	# print("super expresion")


def p_opSExp(p):
	'''opSExp : EQ saveOperator exp
			| DIF saveOperator exp
			| LTOEQ saveOperator exp
			| GTOEQ saveOperator exp
			| GT saveOperator exp
			| LT saveOperator exp
			| empty '''
	# print("cycle super expresion")

def p_errorOpSExp(p):
	'''errorOpSExp : '''
	global errorMsg
	errorMsg = "Error in rule OPSEXP"


def p_exp(p):
	'''exp : term performAddSub errorCyExp cyExp '''
	# print("exp")


def p_cyExp(p):
	'''cyExp : PLUS saveOperator exp
			| MINUS saveOperator exp
			| empty '''
	# print("cycle exp")


def p_errorCyExp(p):
	'''errorCyExp : '''
	global errorMsg
	errorMsg = "Error in rule CYEXP"

def p_term(p):
	'''term : fact performMulDiv cyTerm '''
	# print("term")


def p_cyTerm(p):
	'''cyTerm : MULT saveOperator errorFact term
			| DIV saveOperator term
			| empty '''
	# print("cycle term")


def p_fact(p):
	'''fact : CTES saveConstantString
			| cte
			| funcCall
			| PARINI putFondo expresion PARFIN takeFondo
			| ID saveVariable opAccess errorOpAccess'''
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
	'''cte : CTED saveConstantInt
		| CTEF saveConstantFloat
		| TRUE saveConstantBool
		| FALSE saveConstantBool '''
	# print("cte")

def p_empty(p):
    '''empty : '''
    # print("EMPTY")


def p_printTables(p):
	'''printTables : '''
	for x in range(0, len(cuadruplos)):
		print(x, cuadruplos[x])

def p_error(p):
	global line
	global errorMsg
	print("Error in line %d: Unexpected token '%s'" % (line, p.value))
	print('%s' % errorMsg)
	sys.exit()

# Save in Stacks

def p_rellenaFalso(p):
	'''rellenaFalso : '''
	falso = pSaltos.pop()
	rellena(falso, contQuadruples)

def p_saveFalso(p):
	'''saveFalso : '''
	aux = pTipos.pop()

	if aux != BOOL:
		global semanticError
		semanticError = "Types Mismatch"
		semanticErrorHalt()

	res = pOper.pop()
	generateJump('f', res)
	pSaltos.append(contQuadruples - 1)

def p_saveVerdadero(p):
	'''saveVerdadero : '''
	generateJump('s', None)
	falso = pSaltos.pop()
	rellena(falso, contQuadruples)
	pSaltos.append(contQuadruples - 1)

def p_saveConstantInt(p):
        '''saveConstantInt : '''
        address = getAddressForConstant(INT)

        pOper.append(address)
        pTipos.append(INT)
        
def p_saveConstantFloat(p):
        '''saveConstantFloat : '''
        address = getAddressForConstant(FLOAT)

        pOper.append(address)
        pTipos.append(FLOAT)
        
def p_saveConstantBool(p):
        '''saveConstantBool : '''
        address = getAddressForConstant(BOOL)

        pOper.append(address)
        pTipos.append(BOOL)
        
def p_saveConstantString(p):
        '''saveConstantString : '''
        address = getAddressForConstant(STRING)

        pOper.append(address)
        pTipos.append(STRING)

def p_saveVariable(p):
	'''saveVariable : '''

	variable = ""
	if (previousToken in vars_local) or (previousToken in vars_global):
		variable = previousToken
	elif (currentToken in vars_local) or (currentToken in vars_global):
		variable = currentToken

	address = 0

	if variable in vars_local:
		address = vars_local[variable]
	elif variable in vars_global:
		address = vars_global[variable]
	else:
		global semanticError
		semanticError = "Undeclared variable " + variable
		semanticErrorHalt()

	pOper.append(address)
	pTipos.append(getTypeForAddress(address))

def p_saveOperator(p):
	'''saveOperator : '''

	if previousToken == '+':
		pilaO.append(ADD)
	elif previousToken == '-':
		pilaO.append(SUBSTRACT)
	elif previousToken == '*':
		pilaO.append(MULTIPLY)
	elif previousToken == '/':
		pilaO.append(DIVISION)
	elif previousToken == '<' or currentToken == '':
		pilaO.append(LESS_THAN)
	elif previousToken == ">" or currentToken == '>':
		pilaO.append(GREATER_THAN)
	elif previousToken == '<=' or currentToken == '<=':
		pilaO.append(LESS_EQUAL)
	elif previousToken == '>=' or currentToken == '>=':
		pilaO.append(GREATER_EQUAL)
	elif previousToken == '==' or currentToken == '==':
		pilaO.append(EQUAL)
	elif previousToken == "!=":
		pilaO.append(DIFFERENT)
	elif previousToken == 'AND':
		pilaO.append(AND)
	elif previousToken == 'OR':
		pilaO.append(OR)
	elif previousToken == '=':
		pilaO.append(ASSIGN)

def p_putFondo(p):
	'''putFondo : '''

	pilaO.append(FONDO_FALSO)

def p_takeFondo(p):
	'''takeFondo : '''

	pilaO.pop()

# Perform Semantic Actions Rules

def p_performAssign(p):
	'''performAssign : '''

	if not pilaO:
		return

	operator = pilaO.pop()

	if operator == FONDO_FALSO:
		pilaO.append(operator)
		return

	if operator != ASSIGN:
		pilaO.append(operator)
		
		return

	generateQuadruple(operator)

	return

def p_performMulDiv(p):
	'''performMulDiv : '''

	if not pilaO:
		return

	operator = pilaO.pop()

	if operator == FONDO_FALSO:
		pilaO.append(operator)
		return

	if operator != MULTIPLY and operator != DIVISION:
		pilaO.append(operator)
		
		return

	generateQuadruple(operator)

	return

def p_performAddSub(p):
	'''performAddSub : '''

	if not pilaO:
		return

	operator = pilaO.pop()

	if operator == FONDO_FALSO:
		pilaO.append(operator)
		return

	if operator != ADD and operator != SUBSTRACT:
		pilaO.append(operator)
		
		return

	generateQuadruple(operator)

	return

def p_performRelational(p):
	'''performRelational : '''

	if not pilaO:
		return

	operator = pilaO.pop()

	if operator == FONDO_FALSO:
		pilaO.append(operator)
		return

	if operator != LESS_THAN and operator != GREATER_THAN and operator != LESS_EQUAL and operator != GREATER_EQUAL and operator != EQUAL and operator != DIFFERENT :
		pilaO.append(operator)
		
		return

	generateQuadruple(operator)

	return

def p_performAndOr(p):
	'''performAndOr : '''

	if not pilaO:
		return

	operator = pilaO.pop()

	if operator == FONDO_FALSO:
		pilaO.append(operator)
		return

	if operator != AND and operator != OR:
		pilaO.append(operator)
		
		return

	generateQuadruple(operator)

	return

def p_performPrint(p):
	'''performPrint : '''
	generateQuadruple(PRINT)

def p_performeRead(p):
	'''performRead : '''
	generateQuadruple(READ)	

def generateQuadruple(operator):
	global contQuadruples

	if operator == PRINT:
		res = pOper.pop()
		cuadruplo = (PRINT, '', '', res)
		cuadruplos.append(cuadruplo)
		contQuadruples += 1

		return

	if operator == READ:
		res = pOper.pop()
		cuadruplo = (READ, '', '', res)
		cuadruplos.append(cuadruplo)
		contQuadruples += 1

		return	

	if not pTipos:
		semanticErrorHalt()

	tipoDer = pTipos.pop()

	if not pTipos:
		semanticErrorHalt()

	tipoIzq = pTipos.pop()
	tipoRes = typesValidator(tipoIzq, tipoDer, operator)

	if tipoRes == ERROR:
		global semanticError
		print(pilaO)
		print(pOper)
		print(tipoIzq)
		print(operator)
		print(tipoDer)
		semanticError = "Types mismatch " + str(tipoIzq) + " " + str(operator) + " " + str(tipoDer)
		semanticErrorHalt()

	opDer = pOper.pop()
	opIzq = pOper.pop()

	if operator == ASSIGN:
		cuadruplo = (operator, opDer, "", opIzq)
		pOper.append(opIzq)
		pTipos.append(getTypeForAddress(opIzq))
	else:
		temp = getTempForType(tipoRes)
		cuadruplo = (operator, opIzq, opDer, temp)
		pOper.append(temp)
		pTipos.append(tipoRes)
	
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

def rellena(salto, add):
	cuadruplo = cuadruplos[salto]
	operator = cuadruplo[0]
	falso = cuadruplo[1]
	opDer = cuadruplo[2]

	aux = (operator, falso, opDer, add)
	cuadruplos[salto] = aux

def generateJump(tipo, cond):
	global contQuadruples

	if tipo == 'f':
		cuadruplo = (GOTOF, cond, "", "")
	elif tipo == 'v':
		cuadruplo = (GOTOV, cond, "", "")
	elif tipo == 's':
		cuadruplo = (GOTO, "", "", cond)

	cuadruplos.append(cuadruplo)
	contQuadruples += 1

# Helper Methods

def typeToCode(type):
    switcher = {
        "int": 10,
        "float": 20,
        "bool": 30,
        "string": 40,
    }
    return switcher.get(type, 50)

def operatorToCode(operator):
    switcher = {
        "+": 100,
        "-": 110,
        "*": 120,
        "/": 130,
        "<": 140,
        ">": 150,
        "<=": 160,
        ">=": 170,
        "==": 180,
        "!=": 190,
        "AND": 200,
        "OR": 210,
        "=": 220,
    }
    return switcher.get(operator, 50)

def getAddressForType(type):
	global contInt
	global contFloat
	global contBool
	global contString

	typeCode = typeToCode(type)
	
	if typeCode == INT:
		contInt += 1
		return contInt - 1

	if typeCode == FLOAT:
		contFloat += 1
		return contFloat - 1

	if typeCode == BOOL:
		contBool += 1
		return contBool - 1

	if typeCode == STRING:
		contString += 1
		return contString - 1

def getAddressForConstant(type):
	global contConstInt
	global contConstFloat
	global contConstBool
	global contConstString
	
	if type == INT:
		contConstInt += 1
		return contConstInt - 1

	if type == FLOAT:
		contConstFloat += 1
		return contConstFloat - 1

	if type == BOOL:
		contConstBool += 1
		return contConstBool - 1

	if type == STRING:
		contConstString += 1
		return contConstString - 1

def getTempForType(type):
	global contTempInt
	global contTempFloat
	global contTempBool
	global contTempString
	
	if type == INT:
		contTempInt += 1
		return contTempInt - 1

	if type == FLOAT:
		contTempFloat += 1
		return contTempFloat - 1

	if type == BOOL:
		contTempBool += 1
		return contTempBool - 1

	if type == STRING:
		contTempString += 1
		return contTempString - 1

def getTypeForAddress(address):
	if (address >= MIN_INT and address <= MAX_INT) or (address >= MIN_TEMP_INT and address <= MAX_TEMP_INT) or (address >= MIN_CONST_INT and address <= MAX_CONST_INT):
		return INT
	
	if (address >= MIN_FLOAT and address <= MAX_FLOAT) or (address >= MIN_TEMP_FLOAT and address <= MAX_TEMP_FLOAT) or (address >= MIN_CONST_FLOAT and address <= MAX_CONST_FLOAT):
		return FLOAT
	
	if (address >= MIN_BOOL and address <= MAX_BOOL) or (address >= MIN_TEMP_BOOL and address <= MAX_TEMP_BOOL) or (address >= MIN_CONST_BOOL and address <= MAX_CONST_BOOL):
		return BOOL
	
	if (address >= MIN_STRING and address <= MAX_STRING) or (address >= MIN_TEMP_STRING and address <= MAX_TEMP_STRING) or (address >= MIN_CONST_STRING and address <= MAX_CONST_STRING):
		return STRING

def typesValidator(left, right, operator):
	opMap = operator / 10 % 10

	if operator >= 200:
		opMap += 10
	
	return semanticCube[(left / 10 - 1) * 4 + (right / 10 - 1)][opMap]


import ply.yacc as yacc
parser = yacc.yacc()

file = open ("input3.txt", "r");
yacc.parse(file.read())
