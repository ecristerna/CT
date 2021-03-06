import sys

sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
	raw_input = input

avoidTokens = ['{','}',',',';','[', ']', ':', '.', '+', '-', '*', '/', '%', '>', '>=', '<', '<=', '!=', '==', '=', '(', ')', 'RETURN', 'AND', 'OR']
literals = ['{','}',',',';','[', ']', ':', '.']
reserved = ['LINE', 'HISTO', 'PIE', 'STACKED', 'DBARS', 'BARS', 'SUM', 'MUL', 'AVERAGE', 'VARIANCE', 'STDEVIATION', 'NEG', 'PRINT', 'READ', 'PROGRAM','STRUCT','FUNC','RETURNS','RETURN','INT', 'FLOAT', 'STRING', 'BOOL', 'TRUE', 'FALSE', 'VARS', 'MAIN', 'AND', 'OR', 'WHILE', 'FOR', 'IF', 'ELSE',]
tokens = ['PARINI', 'PARFIN', 'ASGN', 'LT', 'GT', 'PLUS', 'MINUS', 'MULT', 'DIV', 'RES', 'GTOEQ', 'LTOEQ','DIF', 'EQ','ID','CTED','CTEF','CTES',] + reserved

line = 1
errorMsg = ""
currentScope = "global"
vars_global = {}
vars_local = {}
constants_table = {}
dir_procs = []
param_types = []
currentType = ""
currentTable = ""
currentToken = ""
previousToken = ""
semanticError = ""
declaringParameters = False
paramCounter = 0
currentProc = []
dim = 1
varR = 1
currentDimensionedVariable = ''
currentStructDimension = []

# Addresses

MIN_INT_GLOBAL = 1000
MAX_INT_GLOBAL = 1999
MIN_FLOAT_GLOBAL = 2000
MAX_FLOAT_GLOBAL = 2999
MIN_BOOL_GLOBAL = 3000
MAX_BOOL_GLOBAL = 3999
MIN_STRING_GLOBAL = 4000
MAX_STRING_GLOBAL = 4999

MIN_INT = 5000
MAX_INT = 5999
MIN_FLOAT = 6000
MAX_FLOAT = 6999
MIN_BOOL = 7000
MAX_BOOL = 7999
MIN_STRING = 8000
MAX_STRING = 8999

MIN_CONST_INT = 9000
MAX_CONST_INT= 9332
MIN_CONST_FLOAT = 9333
MAX_CONST_FLOAT= 9665
MIN_CONST_STRING = 9666
MAX_CONST_STRING= 9997
MIN_CONST_BOOL = 9998
MAX_CONST_BOOL= 9999

MIN_TEMP_INT = 10000
MAX_TEMP_INT = 10999
MIN_TEMP_FLOAT = 11000
MAX_TEMP_FLOAT = 11999
MIN_TEMP_BOOL = 12000
MAX_TEMP_BOOL = 12999
MIN_TEMP_STRING = 13000
MAX_TEMP_STRING = 13999

contIntGlobal = MIN_INT_GLOBAL
contFloatGlobal = MIN_FLOAT_GLOBAL
contBoolGlobal = MIN_BOOL_GLOBAL
contStringGlobal = MIN_STRING_GLOBAL

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

currentTempInt = 0
currentTempFloat = 0
currentTempBool = 0
currentTempString = 0

contQuadruples = 2

# Types & Operators Codes

INT = 10
FLOAT = 20
BOOL = 30
STRING = 40
ERROR = 50
PROGRAM = 60
FUNC = 70
MAIN = 80

FONDO_FALSO = 99

ADD = 100
SUBSTRACT = 110
MULTIPLY = 120
DIVISION = 130
RESIDUE = 140
LESS_THAN = 150
GREATER_THAN = 160
LESS_EQUAL = 170
GREATER_EQUAL = 180
EQUAL = 190
DIFFERENT = 200
AND = 210
OR = 220
ASSIGN = 230
PRINT = 240
READ = 250
GOTOF = 260
GOTOV = 270
GOTO = 280
ERA = 290
GOSUB = 300
RETORNO = 310
PARAM = 320
FUNCRETURN = 330
VER = 340
NEG = 350
AVERAGE = 360
VARIANCE = 370
STDEV = 380
SUM = 390
MUL = 400
BARS = 410
DBARS = 420
STACKED = 430
PIE = 440
HISTO = 450
LINE = 460


# Semantic Cube

			# 	 +	   	 -      *      /  	   %   	<      >     <=     >=     ==     !=     AND    OR     =   
semanticCube = [[INT,   INT,   INT,   INT, 	 INT,   BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  ERROR, ERROR, INT], 	 # Int vs Int
				[FLOAT, FLOAT, FLOAT, FLOAT, ERROR, BOOL, 	BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  ERROR, ERROR, ERROR], # Int vs Float
				[ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # Int vs Bool
				[ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # Int vs String
				[FLOAT, FLOAT, FLOAT, FLOAT, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, FLOAT], # Float vs Int
				[FLOAT, FLOAT, FLOAT, FLOAT, ERROR, BOOL, 	BOOL,  BOOL,  BOOL,  BOOL,  BOOL,  ERROR, ERROR, FLOAT], # Float vs Float
				[ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # Float vs Bool
				[ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # Float vs String
				[ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # Bool vs Int
				[ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # Bool vs Float
				[ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, BOOL,  BOOL,  BOOL,  BOOL,  BOOL ], # Bool vs Bool
				[ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # Bool vs String
				[ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # String vs Int
				[ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # String vs Float
				[ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR], # String vs Bool
				[STRING, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, BOOL,  BOOL,  ERROR, ERROR, STRING]]# String vs String 

# Quadruples

cuadruplos = [(), ()]

# Stacks

pilaO = []
pOper = []
pTipos = []
pSaltos = []
pDimensionadas = []

# Tokens - Scanner

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

def t_RES(t):
	r'%'
	global currentToken
	global previousToken
	previousToken = currentToken
	currentToken = '%'
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
	# print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

# Initial Rule
def p_program(p):
	'''program : errorProgram PROGRAM saveType ID saveProc "{" opVars changeCurrentScope opFunctions main "}" printTables'''
	# print("program")

# Changes scope for vars declaration
def p_changeCurrentScope(p):
	'''changeCurrentScope : '''
	global currentScope
	global dir_procs
	currentScope = "local"

	dir_procs[-1].append(0)
	dir_procs[-1].append([contIntGlobal - MIN_INT_GLOBAL, contFloatGlobal - MIN_FLOAT_GLOBAL, contBoolGlobal - MIN_BOOL_GLOBAL, contStringGlobal - MIN_STRING_GLOBAL, 0, 0, 0, 0])

# Saves type of current declaring var
def p_saveType(p):
	'''saveType : '''
	global currentScope
	global currentToken
	global currentType
	currentType = currentToken

# Saves proc into dir_procs
def p_saveProc(p):
	'''saveProc : '''
	global dir_procs
	global currentScope
	global currentType
	global currentToken
	global semanticError

	for proc in dir_procs:
		if proc[0] == currentToken:
			semanticError = "Function '" + currentToken + "' already declared"
			semanticErrorHalt()
		if currentToken in vars_global:
			semanticError = "Cannot declare function with same name as variable '" + currentToken + "'"
			semanticErrorHalt()

	if currentScope == "global":
		newProc = [currentToken, PROGRAM, None, None, vars_global]
	else:
		newProc = [currentToken, FUNC, None, None, vars_local]

	dir_procs += [newProc]

def p_errorProgram(p):
	'''errorProgram : '''

	# print("---------------")
	# print("   Compiler")
	# print("---------------")

	global errorMsg
	errorMsg = "Error in rule PROGRAM"

# Decides if vars block exists
def p_opVars(p):
	'''opVars : vars
			| empty'''
	# print("optional vars")

# Decides if there is a function declaration in the program
def p_opFunctions(p):
	'''opFunctions : function opFunctions
				| empty'''

# Initialize vars declaration block
def p_vars(p):
	'''vars : errorVars VARS declare '''
	# print("vars")

# Saves ID for a new variable into vars table (global or local)
def p_saveID(p):
	'''saveID : '''
	global currentScope
	global currentType
	global currentToken
	global semanticError

	tokenToUse = currentToken

	if currentToken == ')':
		tokenToUse = previousToken

	if currentScope == "global":
		global vars_global

		if tokenToUse in vars_global:
			semanticError = "Variable '" + tokenToUse + "' already declared"
			semanticErrorHalt()

		vars_global[currentToken] = getAddressForType(currentType)
	else:
		global vars_local

		if tokenToUse in vars_local:
			semanticError = "Variable '" + tokenToUse + "' already declared on this scope"
			semanticErrorHalt()

		for proc in dir_procs:
			if proc[0] == tokenToUse:
				semanticError = "Function '" + currentToken + "' already declared"
				semanticErrorHalt()
		
		vars_local[tokenToUse] = getAddressForType(currentType)

		if declaringParameters:
			param_types[-1] = vars_local[tokenToUse]

# Halts the program if any semantic error occurs
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

# Possible types for declaring variables
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

# Main function block
def p_main(p):
	'''main : errorMain MAIN saveCurrentTemps saveMain "{" opVars generateInitialQuadruple body "}" clearVarsTable'''
	# print("main")

# Saves initial quadruple, once compiler knows where the Main block starts
def p_generateInitialQuadruple(p):
	'''generateInitialQuadruple : '''
	global contQuadruples

	cuadruplo = (ERA, "main", "", "")
	cuadruplos[0] = cuadruplo
	cuadruplo = (GOSUB, "main", "", contQuadruples)
	cuadruplos[1] = cuadruplo

# Saves Main block to dir_procs
def p_saveMain(p):
	'''saveMain : '''
	global dir_procs
	global currentToken

	newProc = [currentToken, MAIN, None, None, vars_local, contQuadruples]
	dir_procs += [newProc]

def p_errorMain(p):
	'''errorMain : '''
	global errorMsg
	errorMsg = "Error in rule MAIN"

# Possible instructions in the program
def p_instr(p):
	'''instr : basicStatements ";"
			| graphFunctions ";"
			| condition
			| cycle '''
	# print("instr")

# Graph Functions
def p_graphFunctions(p):
	'''graphFunctions : STACKED PARINI putFondo ID saveStructID "," ID saveStructID "," expresion "," expresion "," expresion takeFondo PARFIN performStacked
					|  BARS PARINI putFondo ID saveStructID "," ID saveStringStructID "," expresion "," expresion takeFondo PARFIN performBars
					| DBARS PARINI putFondo ID saveStructID "," ID saveStructID "," ID saveStringStructID "," expresion "," expresion "," expresion takeFondo PARFIN performDBars
					| PIE PARINI putFondo ID saveStructID "," ID saveStringStructID "," expresion takeFondo PARFIN performPie
					| HISTO PARINI putFondo ID saveStructID "," expresion "," expresion takeFondo PARFIN performHisto 
					| LINE PARINI putFondo ID saveStructID "," ID saveStructID "," expresion takeFondo PARFIN performLine'''

# Checks semantic and saves quadruple for Line Function
def p_performLine(p):
	'''performLine : '''
	global semanticError
	global contQuadruples

	lenght = pOper.pop()
	tipoLen = pTipos.pop()

	if tipoLen != INT:
		semanticError = "Len parameter must be an INT value."
		semanticErrorHalt()

	addressB = pOper.pop()
	tipoB = pTipos.pop()
	addressA = pOper.pop()
	tipoA = pTipos.pop()

	cuadruplo = (LINE, addressA, addressB, lenght)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

# Checks semantic and saves quadruple for Stacked Function
def p_performStacked(p):
	'''performStacked : '''
	global semanticError
	global contQuadruples

	labelB = pOper.pop()
	tipoLabelB = pTipos.pop()

	if tipoLabelB != STRING:
		semanticError = "LabelB parameter must be a STRING value."
		semanticErrorHalt()

	labelA = pOper.pop()
	tipoLabelA = pTipos.pop()

	if tipoLabelA != STRING:
		semanticError = "LabelA parameter must be a STRING value."
		semanticErrorHalt()

	lenght = pOper.pop()
	tipoLen = pTipos.pop()

	if tipoLen != INT:
		semanticError = "Len parameter must be an INT value."
		semanticErrorHalt()

	addressB = pOper.pop()
	tipoB = pTipos.pop()
	addressA = pOper.pop()
	tipoA = pTipos.pop()

	cuadruplo = (STACKED, addressA, addressB, lenght, labelA, labelB)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

# Checks semantic and saves quadruple for Bars Function
def p_performBars(p):
	'''performBars : '''
	global semanticError
	global contQuadruples

	labelGroup = pOper.pop()
	tipoLabelGroup = pTipos.pop()

	if tipoLabelGroup != STRING:
		semanticError = "LabelGroup parameter must be a STRING value."
		semanticErrorHalt()

	lenght = pOper.pop()
	tipoLen = pTipos.pop()

	if tipoLen != INT:
		semanticError = "Len parameter must be an INT value."
		semanticErrorHalt()

	addressLabels = pOper.pop()
	tipoLabels = pTipos.pop()
	addressA = pOper.pop()
	tipoA = pTipos.pop()

	cuadruplo = (BARS, addressA, addressLabels, lenght, labelGroup)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

# Checks semantic and saves quadruple for DBars Function
def p_performDBars(p):
	'''performDBars : '''
	global semanticError
	global contQuadruples

	labelB = pOper.pop()
	tipoLabelB = pTipos.pop()

	if tipoLabelB != STRING:
		semanticError = "LabelB parameter must be a STRING value."
		semanticErrorHalt()

	labelA = pOper.pop()
	tipoLabelA = pTipos.pop()

	if tipoLabelA != STRING:
		semanticError = "LabelA parameter must be a STRING value."
		semanticErrorHalt()

	lenght = pOper.pop()
	tipoLen = pTipos.pop()

	if tipoLen != INT:
		semanticError = "Len parameter must be an INT value."
		semanticErrorHalt()

	addressLabels = pOper.pop()
	tipoLabels = pTipos.pop()
	addressB = pOper.pop()
	tipoB = pTipos.pop()
	addressA = pOper.pop()
	tipoA = pTipos.pop()

	cuadruplo = (DBARS, addressA, addressB, addressLabels, lenght, labelA, labelB)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

# Checks semantic and saves quadruple for Pie Function
def p_performPie(p):
	'''performPie : '''
	global semanticError
	global contQuadruples

	lenght = pOper.pop()
	tipoLen = pTipos.pop()

	if tipoLen != INT:
		semanticError = "Len parameter must be an INT value."
		semanticErrorHalt()

	addressLabels = pOper.pop()
	tipoLabels = pTipos.pop()
	addressA = pOper.pop()
	tipoA = pTipos.pop()

	cuadruplo = (PIE, addressA, addressLabels, lenght)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

# Checks semantic and saves quadruple for Histo Function
def p_performHisto(p):
	'''performHisto : '''
	global semanticError
	global contQuadruples

	nGroups = pOper.pop()
	tipoLabelnGroups = pTipos.pop()

	if tipoLabelnGroups != INT:
		semanticError = "NGroups parameter must be a INT value."
		semanticErrorHalt()

	lenght = pOper.pop()
	tipoLen = pTipos.pop()

	if tipoLen != INT:
		semanticError = "Len parameter must be an INT value."
		semanticErrorHalt()

	addressA = pOper.pop()
	tipoA = pTipos.pop()

	cuadruplo = (HISTO, addressA, lenght, nGroups)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

# Checks semantic and saves ID for struct var
def p_saveStringStructID(p):
	'''saveStringStructID : '''
	global semanticError

	address = 0

	if currentToken in vars_local:
		if not isinstance(vars_local[currentToken], list):
			semanticError = "Parameter must be a STRING struct."
			semanticErrorHalt()

		address = vars_local[currentToken][0]
	elif currentToken in vars_global:
		if not isinstance(vars_global[currentToken], list):
			semanticError = "Parameter must be a STRING struct."
			semanticErrorHalt()

		address = vars_global[currentToken][0]
	else:
		semanticError = "Undeclared variable " + currentToken
		semanticErrorHalt()

	tipo = getTypeForAddress(address)

	if tipo != STRING:
		semanticError = "Parameter must be a STRING struct."
		semanticErrorHalt()

	pOper.append(address)
	pTipos.append(tipo)

# Basic statements within an instruction
def p_basicStatements(p):
	'''basicStatements : assign
					| funcCall
					| print
					| read '''

# Print function
def p_print(p):
	'''print : PRINT PARINI exp performPrint cyPrint PARFIN '''

# Multiple prints in one line
def p_cyPrint(p):
	'''cyPrint : "," fix exp performPrint cyPrint
				| empty '''

# Read function
def p_read(p):
	'''read : READ PARINI ID saveVariable performRead cyRead PARFIN '''

# Multiple reads in one line
def p_cyRead(p):
	'''cyRead : "," fix ID saveVariable performRead cyRead
				| empty '''

def p_fix(p):
	'''fix : '''
	global previousToken
	previousToken = ","

# Declare variable, either atomic or struct
def p_declare(p):
	'''declare : basicDeclare
			| structDeclare '''
	# print("declare")

# Initialize variable with value
def p_init(p):
	'''init : ASGN saveOperator errorInit initWith '''
	# print("init")

def p_errorInit(p):
	'''errorInit : '''
	global errorMsg
	errorMsg = "Error in rule INIT"

# Initializes variable with expresion or funcCall
def p_initWith(p):
	'''initWith : expresion
		| funcCall '''
	# print("init with")

# Declare parameter when declaring a function
def p_param(p):
	'''param : saveType type errorParam ID cyTypeParam cyParam '''
	# print("param")

def p_errorParam(p):
	'''errorParam : '''
	global errorMsg
	errorMsg = "Error in rule PARAM"

# Multiple parameters for different types
def p_cyParam(p):
	'''cyParam : errorCyParam saveTypeParam saveID ";"  param
		| empty saveTypeParam saveID '''
	# print("cycle param")

# Multiple parameters for same type
def p_cyTypeParam(p):
	'''cyTypeParam : "," saveTypeParam saveID ID cyTypeParam
		| empty '''
	# print("cycle type param")

# Saves current type when declaring function parameters
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

# Function declaration
def p_function(p):
	'''function : errorFunction saveCurrentTemps FUNC saveType ID saveProc flagParameters PARINI opParameters PARFIN flagParameters opReturns "}" clearVarsTable '''
	# print("function")

# Saves current counter for temporals, to know whow many are used into a function
def p_saveCurrentTemps(p):
	'''saveCurrentTemps : '''
	global currentTempInt
	global currentTempFloat
	global currentTempBool
	global currentTempString

	currentTempInt = contTempInt
	currentTempFloat = contTempFloat
	currentTempBool = contTempBool
	currentTempString = contTempString

def p_errorFunction(p):
	'''errorFunction : '''
	global errorMsg
	errorMsg = "Error in rule FUNCTION"

# Re initializes local vars table when function declaration ends
def p_clearVarsTable(p):
	'''clearVarsTable : '''
	global vars_local
	global contInt
	global contFloat
	global contBool
	global contString
	global contTempInt
	global contTempFloat
	global contTempBool
	global contTempString

	ints = contInt - MIN_INT
	floats = contFloat - MIN_FLOAT
	bools = contBool - MIN_BOOL
	strings = contString - MIN_STRING
	tempInts = contTempInt - currentTempInt
	tempFloats = contTempFloat - currentTempFloat
	tempBools = contTempBool - currentTempBool
	tempStrings = contTempString - currentTempString

	currentProc = dir_procs[len(dir_procs) - 1]
	currentProc += [[ints, floats, bools, strings, tempInts, tempFloats, tempBools, tempStrings]]
	dir_procs[len(dir_procs) - 1] = currentProc

	if currentProc[1] == FUNC:
		generateQuadruple(RETORNO)

	contInt = MIN_INT
	contFloat = MIN_FLOAT
	contBool = MIN_BOOL
	contString = MIN_STRING

	# print("\nVARS " + currentProc[0])
	# print(vars_local)

	vars_local = {}

	contTempInt = MIN_TEMP_INT
	contTempFloat = MIN_TEMP_FLOAT
	contTempBool = MIN_TEMP_BOOL
	contTempString = MIN_TEMP_STRING

# Return statement for function 
def p_return(p):
	'''return : errorReturn RETURN expresion saveReturnValue ";" '''
	# print("return")

# Saves return value into a global var related to the function name
def p_saveReturnValue(p):
	'''saveReturnValue : '''
	global contQuadruples
	global semanticError

	value = pOper.pop()
	tipo = pTipos.pop()
	
	if tipo != getTypeForAddress(vars_global[dir_procs[len(dir_procs) - 1][0]]):
		semanticError = "Return expression does not match function type"
		semanticErrorHalt()


	address = vars_global[dir_procs[len(dir_procs) - 1][0]]
	typeAddress = getTypeForAddress(address)

	cuadruplo = (FUNCRETURN, value, "", address)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

def p_errorReturn(p):
	'''errorReturn : '''
	global errorMsg
	errorMsg = "Error in rule RETURN"

# Parameters for function declaration
def p_opParameters(p):
	'''opParameters : param saveParamToDirProc errorOpParameters
					| empty '''
	# print("optional parameters")

def p_flagParameters(p):
	'''flagParameters : '''
	global declaringParameters
	declaringParameters = not declaringParameters

# Saves read param into dir_procs
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

# Decission for optiona returns for function declaration
def p_opReturns(p):
	'''opReturns : errorOpReturns RETURNS type saveReturnType "{" opVars saveQuadruple body return
		| "{" opVars saveQuadruple body '''
	# print("returns")

# Saves quadruple number where function starts
def p_saveQuadruple(p):
	'''saveQuadruple : '''
	currentProc = dir_procs[len(dir_procs) - 1]
	currentProc += [contQuadruples]
	dir_procs[len(dir_procs) - 1] = currentProc

# Saves return type into dir_procs entry
def p_saveReturnType(p):
	'''saveReturnType : '''
	global dir_procs
	global currentToken
	global vars_global

	dir_procs[len(dir_procs) - 1][3] = typeToCode(currentToken)
	vars_global[dir_procs[len(dir_procs) - 1][0]] = getGlobalAddressForType(currentToken)

def p_errorOpReturns(p):
	'''errorOpReturns : '''
	global errorMsg
	errorMsg = "Error in rule OPRETURNS"

# Declare for atomic variables
def p_basicDeclare(p):
	'''basicDeclare : saveType type errorBasicDeclare ID cyTypeParam saveID ";" cyDeclare '''
	# print("basic declare")


def p_errorBasicDeclare(p):
	'''errorBasicDeclare : '''
	global errorMsg
	errorMsg = "Error in rule BASICDECLARE"

# Declare for struct variables
def p_structDeclare(p):
	'''structDeclare : errorStructDeclare STRUCT struct ";" cyDeclare '''
	# print("struct declare")

def p_errorStructDeclare(p):
	'''errorStructDeclare : '''
	global errorMsg
	errorMsg = "Error in rule STRUCTDECLARE"

# Multiple declares
def p_cyDeclare(p):
	'''cyDeclare : declare
		| empty '''
	# print("cycle declare")

# Body for blocks
def p_body(p):
	'''body : errorBody cyInstruction
			| empty '''
	# print("body")

def p_errorBody(p):
	'''errorBody : '''
	global errorMsg
	errorMsg = "Error in rule BODY"

# Multiple instructions
def p_cyInstruction(p):
	'''cyInstruction : instr body '''
	# print("cycleInstruction")

# Cycles statements
def p_cycle(p):
	'''cycle : forCycle
			| whileCycle '''
	# print("cycle")

# While cycle
def p_whileCycle(p):
	'''whileCycle : errorWhileCycle WHILE saveReturn PARINI expresion PARFIN saveFalso "{" body "}" repeatWhile'''
	# print("while")

# Last quadruple for while return
def p_repeatWhile(p):
	'''repeatWhile : '''
	falso = pSaltos.pop()
	retorno = pSaltos.pop()
	generateJump('s', retorno)
	rellena(falso, contQuadruples)

# Saves where to return on while cycle
def p_saveReturn(p):
	'''saveReturn : '''
	pSaltos.append(contQuadruples)

def p_errorWhileCycle(p):
	'''errorWhileCycle : '''
	global errorMsg
	errorMsg = "Error in rule WHILECYCLE"

# For cycle
def p_forCycle(p):
	'''forCycle : errorForCycle FOR PARINI assign ";" saveReturn expresion saveFalso ";" saltoBody assign returnFor PARFIN "{" rellenaBody body "}" returnAssign '''
	# print("for")

# Jump to body of For
def p_saltoBody(p):
	'''saltoBody : '''
	generateJump('s', None)
	pSaltos.append(contQuadruples - 1)
	pSaltos.append(contQuadruples)

# Jump to init of For
def p_returnFor(p):
	'''returnFor : '''
	aux = pSaltos.pop()
	aux2 = pSaltos.pop()
	aux3 = pSaltos.pop()
	
	generateJump('s', pSaltos.pop())

	pSaltos.append(aux3)
	pSaltos.append(aux2)
	pSaltos.append(aux)

# Detects where Dor body starts
def p_rellenaBody(p):
	'''rellenaBody : '''
	aux = pSaltos.pop()
	
	rellena(pSaltos.pop(), contQuadruples)

	pSaltos.append(aux)

# Jump to update For variable
def p_returnAssign(p):
	'''returnAssign : '''
	generateJump('s', pSaltos.pop())
	rellena(pSaltos.pop(), contQuadruples)

def p_errorForCycle(p):
	'''errorForCycle : '''
	global errorMsg
	errorMsg = "Error in rule FORCYCLE"

# Assign to variable
def p_assign(p):
	'''assign : ID saveVariable errorAssign assignOptions performAssign'''
	# print("assign")

def p_errorAssign(p):
	'''errorAssign : '''
	global errorMsg
	errorMsg = "Error in rule ASSIGN"

# Assign to atomic variable or struct variable
def p_assignOptions(p):
	'''assignOptions : init
					| saveToDimensionStacks "[" expresion verifyIndex "]" assignMatrix accessStruct init '''
	# print("assignOptions")

# Assign to matrix
def p_assignMatrix(p):
	'''assignMatrix : updateDimension "[" expresion verifyIndex "]" errorAssignMatrix
					| empty '''
	# print("assignMatrix")

def p_errorAssignMatrix(p):
	'''errorAssignMatrix : '''
	global errorMsg
	errorMsg = "Error in rule ASSIGNMATRIX"

# Function call
def p_funcCall(p):
	'''funcCall : ID checkFunction PARINI putFondo opParamCall takeFondo PARFIN checkNumParams '''
	# print("funcCall")

# Semantic for check num params coincidence
def p_checkNumParams(p):
	'''checkNumParams : '''
	global contQuadruples
	global paramCounter
	global semanticError

	if currentProc[2] == None:
		if paramCounter != 0:
			semanticError = "Function " + currentProc[0] + " has no parameters"
			semanticErrorHalt()
	elif len(currentProc[2]) > paramCounter:
		semanticError = "Missing parameters"
		semanticErrorHalt()

	cuadruplo = (GOSUB, currentProc[0], "", currentProc[5])
	cuadruplos.append(cuadruplo)
	contQuadruples += 1
	paramCounter = 0;

	if currentProc[3] != None:
		address = vars_global[currentProc[0]]
		typeAddress = getTypeForAddress(address)
		temp = getTempForType(typeAddress)

		cuadruplo = (ASSIGN, address, "", temp)
		cuadruplos.append(cuadruplo)
		contQuadruples += 1

		pOper.append(temp)
		pTipos.append(typeAddress)

# Checks if function exists
def p_checkFunction(p):
	'''checkFunction : '''
	global currentProc

	for proc in dir_procs:
		if proc[0] == previousToken:
			currentProc = proc
			generateQuadruple(ERA)

			return

	global semanticError
	semanticError = "Undeclared function " + previousToken
	semanticErrorHalt()

# Funciton call with parameters
def p_opParamCall(p):
	'''opParamCall : expresion checkParamType cyParamCall
				| empty '''
	# print("function parameter")

# Multiple parameters
def p_cyParamCall(p):
	'''cyParamCall :  "," expresion checkParamType cyParamCall
				| empty '''
	# print("cycle parameter call")

# Semantic validation for param type coincidence
def p_checkParamType(p):
	'''checkParamType : '''
	global paramCounter
	global contQuadruples
	global semanticError

	paramCounter += 1
	argumento = pOper.pop()
	tipo = pTipos.pop()

	if currentProc[2] == None:
		semanticError = "Function " + currentProc[0] + " has no parameters."
		semanticErrorHalt()

	if paramCounter > len(currentProc[2]):
		semanticError = "Number of parameters do not match function declaration"
		semanticErrorHalt()

	if getTypeForAddress(currentProc[2][paramCounter - 1]) != tipo:
		semanticError = "Parameter " + `paramCounter` + " type does not match function declaration"
		semanticErrorHalt()

	cuadruplo = (PARAM, argumento, "", currentProc[2][paramCounter - 1])
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

# Struct declaration
def p_struct(p):
	'''struct : structType ID saveID createDimension "[" CTED saveDimensionSize "]" optionalMatrix secondLap '''
	# print("struct")

# Calculations for struct tables
def p_secondLap(p):
	'''secondLap : '''
	global dim
	global varR
	global currentDimensionedVariable
	global contInt
	global contFloat
	global contBool
	global contString
	global contIntGlobal
	global contFloatGlobal
	global contBoolGlobal
	global contStringGlobal

	currentDim = 1
	suma = 0
	aux = varR
	typeVar = 0

	if currentScope == 'global':
		typeVar = getTypeForAddress(vars_global[currentDimensionedVariable][0])
		dimensionTable = vars_global[currentDimensionedVariable][1]
		m = aux / (dimensionTable[1] - dimensionTable[0] + 1)
		aux = m
		dimensionTable[2] = m
		vars_global[currentDimensionedVariable][1] = dimensionTable

		if typeVar == INT:
			contIntGlobal += varR - 1
		elif typeVar == FLOAT:
			contFloatGlobal += varR - 1
		elif typeVar == BOOL:
			contBoolGlobal += varR - 1
		elif typeVar == STRING:
			contStringGlobal += varR - 1

	else:
		typeVar = getTypeForAddress(vars_local[currentDimensionedVariable][0])
		dimensionTable = vars_local[currentDimensionedVariable][1]
		m = aux / (dimensionTable[1] - dimensionTable[0] + 1)
		aux = m
		dimensionTable[2] = m
		vars_local[currentDimensionedVariable][1] = dimensionTable

		if typeVar == INT:
			contInt += varR - 1
		elif typeVar == FLOAT:
			contFloat += varR - 1
		elif typeVar == BOOL:
			contBool += varR - 1
		elif typeVar == STRING:
			contString += varR - 1

	if dim > 1:
		if currentScope == 'global':
			dimensionTable = vars_global[currentDimensionedVariable][1][3]
			m = aux / (dimensionTable[1] - dimensionTable[0] + 1)
			dimensionTable[2] = m
			vars_global[currentDimensionedVariable][1][3] = dimensionTable
			vars_global[currentDimensionedVariable][1][3][2] = 0
		else:
			dimensionTable = vars_local[currentDimensionedVariable][1][3]
			m = aux / (dimensionTable[1] - dimensionTable[0] + 1)
			dimensionTable[2] = m
			vars_local[currentDimensionedVariable][1][3] = dimensionTable
			vars_local[currentDimensionedVariable][1][3][2] = 0
	else:
		if currentScope == 'global':
			vars_global[currentDimensionedVariable][1][2] = 0
		else:
			vars_local[currentDimensionedVariable][1][2] = 0

	currentDimensionedVariable = ''
	varR = 1
	dim = 1

# Save size of current dimension when declaring struct
def p_saveDimensionSize(p):
	'''saveDimensionSize : '''
	global vars_global
	global vars_local
	global currentDimensionedVariable
	global varR

	if currentScope == 'global':
		address = vars_global[currentDimensionedVariable]
		dimensionTable = address[1]
		dimensionTable.append(currentToken - 1)
		dimensionTable.append('')
		dimensionTable.append(None)
		vars_global[currentDimensionedVariable][1] = dimensionTable
		varR = varR * (currentToken - 1 - dimensionTable[0] + 1)
	else :
		address = vars_local[currentDimensionedVariable]
		dimensionTable = address[1]
		dimensionTable.append(currentToken - 1)
		dimensionTable.append('')
		dimensionTable.append(None)
		vars_local[currentDimensionedVariable][1] = dimensionTable
		varR = varR * (currentToken - 1 - dimensionTable[0] + 1)

# New dimension on variable
def p_createDimension(p):
	'''createDimension : '''
	global vars_global
	global vars_local
	global currentDimensionedVariable

	currentDimensionedVariable = currentToken

	if currentScope == 'global':
		address = vars_global[currentDimensionedVariable]
		dimensionTable = [address]
		dimensionTable.append([0])
		vars_global[currentDimensionedVariable] = dimensionTable
	else :
		address = vars_local[currentDimensionedVariable]
		dimensionTable = [address]
		dimensionTable.append([0])
		vars_local[currentDimensionedVariable] = dimensionTable

# Type for structs
def p_structType(p):
	'''structType : saveType type'''
	# print("struct type")

# Matrix declaration
def p_optionalMatrix(p):
	'''optionalMatrix : createSecondDimension "[" CTED saveSecondDimensionSize "]"
					| empty '''
	# print("matrix")

# Save size of second dimension
def p_saveSecondDimensionSize(p):
	'''saveSecondDimensionSize : '''
	global vars_global
	global vars_local
	global currentDimensionedVariable
	global varR

	if currentScope == 'global':
		address = vars_global[currentDimensionedVariable]
		subDimensionTable = address[1]
		dimensionTable = subDimensionTable[3]
		dimensionTable.append(currentToken - 1)
		dimensionTable.append('')
		dimensionTable.append(None)
		vars_global[currentDimensionedVariable][1][3] = dimensionTable
		varR = varR * (currentToken - 1 - dimensionTable[0] + 1)
	else :
		address = vars_local[currentDimensionedVariable]
		subDimensionTable = address[1]
		dimensionTable = subDimensionTable[3]
		dimensionTable.append(currentToken - 1)
		dimensionTable.append('')
		dimensionTable.append(None)
		vars_local[currentDimensionedVariable][1][3] = dimensionTable
		varR = varR * (currentToken - 1 - dimensionTable[0] + 1)

# Creates second dimension for struct variable
def p_createSecondDimension(p):
	'''createSecondDimension : '''
	global dim
	global currentDimensionedVariable

	dim += 1

	if currentScope == 'global':
		address = vars_global[currentDimensionedVariable]
		dimensionTable =  address
		dimensionTable[1][3] = [0]
		vars_global[currentDimensionedVariable] = dimensionTable
	else :
		address = vars_local[currentDimensionedVariable]
		dimensionTable = address
		dimensionTable[1][3] = [0]
		vars_local[currentDimensionedVariable] = dimensionTable

# IF statement
def p_condition(p):
	'''condition : errorCondition IF PARINI expresion PARFIN saveFalso "{" body "}" optionalElse rellenaFalso '''
	# print("condition")

def p_errorCondition(p):
	'''errorCondition : '''
	global errorMsg
	errorMsg = "Error in rule CONDITION"

# ELSE statement
def p_optionalElse(p):
	'''optionalElse : errorElse ELSE saveVerdadero "{" body "}"
					| empty '''
	# print("else")

def p_errorElse(p):
	'''errorElse : '''
	global errorMsg
	errorMsg = "Error in rule OPTIONALELSE"

# Expresion firs level
def p_expresion(p):
	'''expresion : sExp performAndOr cyExpresion errorExpresion '''
	# print("expresion")

def p_errorExpresion(p):
	'''errorExpresion : '''
	global errorMsg
	errorMsg = "Error in rule EXPRESION"

# Logical operators
def p_cyExpresion(p):
	'''cyExpresion : AND saveOperator expresion
				| OR saveOperator expresion
				| empty '''
	# print("cycle expresion")

# First level of expresions
def p_sExp(p):
	'''sExp : exp errorOpSExp opSExp performRelational'''
	# print("super expresion")

# Relational operators
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

# Third level of operation
def p_exp(p):
	'''exp : term performAddSub errorCyExp cyExp '''
	# print("exp")

# Plus and Minus
def p_cyExp(p):
	'''cyExp : PLUS saveOperator exp
			| MINUS saveOperator exp
			| empty '''
	# print("cycle exp")

def p_errorCyExp(p):
	'''errorCyExp : '''
	global errorMsg
	errorMsg = "Error in rule CYEXP"

# Fourth level of operation
def p_term(p):
	'''term : fact performMulDiv cyTerm '''
	# print("term")

# Mult, division, residue
def p_cyTerm(p):
	'''cyTerm : MULT saveOperator errorFact term
			| DIV saveOperator term
			| RES saveOperator term
			| empty '''
	# print("cycle term")

# Fifth level of operation, constans, parenthesis, funcCall, ID
def p_fact(p):
	'''fact : putFondo basicLanguageFunctions takeFondo
			| CTES saveConstantString
			| cte
			| funcCall
			| PARINI putFondo expresion PARFIN takeFondo
			| ID saveVariable opAccess errorOpAccess '''
	# print("fact")

# Basic proper language functions 
def p_basicLanguageFunctions(p):
	'''basicLanguageFunctions : NEG PARINI expresion performNeg PARFIN
						| AVERAGE basicFunc performAvg
						| VARIANCE basicFunc performVariance
						| STDEVIATION basicFunc performStdDev
						| SUM basicFunc performSum
						| MUL basicFunc performMul '''

# Parameters for basic proper language functions
def p_basicFunc(p):
	'''basicFunc : PARINI ID saveStructID "," expresion PARFIN '''

# Saves ID of struct (must be INT)
def p_saveStructID(p):
	'''saveStructID : '''
	global semanticError

	address = 0

	if currentToken in vars_local:
		if not isinstance(vars_local[currentToken], list):
			semanticError = "First parameters must be a struct"
			semanticErrorHalt()

		address = vars_local[currentToken][0]
	elif currentToken in vars_global:
		if not isinstance(vars_global[currentToken], list):
			semanticError = "First parameters must be a struct"
			semanticErrorHalt()

		address = vars_global[currentToken][0]
	else:
		semanticError = "Undeclared variable " + currentToken
		semanticErrorHalt()

	tipo = getTypeForAddress(address)

	if tipo != INT and tipo != FLOAT:
		semanticError = "Cannot get stats from non numerical values."
		semanticErrorHalt()

	pOper.append(address)
	pTipos.append(tipo)

# Validates semantic and performs SUM function
def p_performSum(p):
	'''performSum : '''
	global semanticError
	global contQuadruples

	lenght = pOper.pop()
	tipoLen = pTipos.pop()

	if tipoLen != INT:
		semanticError = "Second parameter must be an INT value."
		semanticErrorHalt()

	address = pOper.pop()
	tipo = pTipos.pop()

	newAddress = getTempForType(tipo)

	cuadruplo = (SUM, address, lenght, newAddress)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

	pOper.append(newAddress)
	pTipos.append(tipo)

# Validates semantic and performs MUL function
def p_performMul(p):
	'''performMul : '''
	global semanticError
	global contQuadruples

	lenght = pOper.pop()
	tipoLen = pTipos.pop()

	if tipoLen != INT:
		semanticError = "Second parameter must be an INT value."
		semanticErrorHalt()

	address = pOper.pop()
	tipo = pTipos.pop()

	newAddress = getTempForType(tipo)

	cuadruplo = (MUL, address, lenght, newAddress)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

	pOper.append(newAddress)
	pTipos.append(tipo)

# Validates semantic and performs AVG function
def p_performAvg(p):
	'''performAvg : '''
	global semanticError
	global contQuadruples

	lenght = pOper.pop()
	tipoLen = pTipos.pop()

	if tipoLen != INT:
		semanticError = "Second parameter must be an INT value."
		semanticErrorHalt()

	address = pOper.pop()
	tipo = pTipos.pop()

	newAddress = getTempForType(FLOAT)

	cuadruplo = (AVERAGE, address, lenght, newAddress)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

	pOper.append(newAddress)
	pTipos.append(FLOAT)

# Validates semantic and performs VARIANCE function
def p_performVariance(p):
	'''performVariance : '''
	global semanticError
	global contQuadruples

	lenght = pOper.pop()
	tipoLen = pTipos.pop()

	if tipoLen != INT:
		semanticError = "Second parameter must be an INT value."
		semanticErrorHalt()

	address = pOper.pop()
	tipo = pTipos.pop()

	newAddress = getTempForType(FLOAT)

	cuadruplo = (VARIANCE, address, lenght, newAddress)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

	pOper.append(newAddress)
	pTipos.append(FLOAT)

# Validates semantic and performs STDEV function
def p_performStdDev(p):
	'''performStdDev : '''
	global semanticError
	global contQuadruples

	lenght = pOper.pop()
	tipoLen = pTipos.pop()

	if tipoLen != INT:
		semanticError = "Second parameter must be an INT value."
		semanticErrorHalt()

	address = pOper.pop()
	tipo = pTipos.pop()

	newAddress = getTempForType(FLOAT)

	cuadruplo = (STDEV, address, lenght, newAddress)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

	pOper.append(newAddress)
	pTipos.append(FLOAT)

# Validates semantic and performs NEG function
def p_performNeg(p):
	'''performNeg : '''
	global semanticError
	global contQuadruples

	valor = pOper.pop()
	tipo = pTipos.pop()

	if tipo == STRING:
		semanticError = "Cannot negate a string value."
		semanticErrorHalt()

	newAddress = getTempForType(tipo)

	cuadruplo = (NEG, valor, '', newAddress)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

	pOper.append(newAddress)
	pTipos.append(tipo)

def p_errorFact(p):
	'''errorFact : '''
	global errorMsg
	errorMsg = "Error in rule ERRORFACT"

# Access to struct
def p_opAccess(p):
	'''opAccess : opStruct
				| empty '''
	# print("optional access")

def p_errorOpAccess(p):
	'''errorOpAccess : '''
	global errorMsg
	errorMsg = "Error in rule ERROROPACCESS"

# Access to struct
def p_opStruct(p):          
	'''opStruct : errorOpStruct saveToDimensionStacks "[" expresion verifyIndex "]" opMatrix accessStruct '''
	# print("optional struct")

# Saves quadruple of final address
def p_accessStruct(p):
	'''accessStruct : '''
	global contQuadruples

	aux1 = pOper.pop()
	temp = getTempForType(INT)

	cuadruplo = ()
	toSave = 0
	varType = 0

	if currentDimensionedVariable in vars_global:
		toSave = vars_global[currentDimensionedVariable][0]
		varType = getTypeForAddress(toSave)
	else:
		toSave = vars_local[currentDimensionedVariable][0]
		varType = getTypeForAddress(toSave)

	cuadruplo = (ADD, aux1, '|' + str(toSave) + '|', temp)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

	pOper.append('(' + str(temp) + ')')
	pTipos.append(varType)

	pilaO.pop()
	pDimensionadas.pop()

# Verifies index into dimension size
def p_verifyIndex(p):
	'''verifyIndex : '''
	global currentDimensionedVariable
	global contQuadruples

	address = pOper.pop()
	pOper.append(address)

	limI = currentStructDimension[0]
	limS = currentStructDimension[1]

	cuadruplo = (VER, limI, limS, address)
	cuadruplos.append(cuadruplo)
	contQuadruples += 1

	if currentStructDimension[3] != None:
		aux = pOper.pop()
		temp = getTempForType(pTipos.pop())

		cuadruplo = (MULTIPLY, aux, '|' + str(currentStructDimension[2]) + '|', temp)
		cuadruplos.append(cuadruplo)
		contQuadruples += 1

		pOper.append(temp)
		pTipos.append(getTypeForAddress(temp))

	if dim > 1:
		aux2 = pOper.pop()
		aux1 = pOper.pop()
		temp = getTempForType(pTipos.pop())
		pTipos.pop()

		cuadruplo = (ADD, aux1, aux2, temp)
		cuadruplos.append(cuadruplo)
		contQuadruples += 1
		
		pOper.append(temp)
		pTipos.append(getTypeForAddress(temp))

# Dimension Stacks update
def p_saveToDimensionStacks(p):
	'''saveToDimensionStacks : '''
	global semanticError
	global dim
	global currentDimensionedVariable
	global currentStructDimension

	pOper.pop()
	pTipos.pop()
	varID = currentToken
	currentDimensionedVariable = varID

	if varID in vars_global:
		if (not isinstance(vars_global[varID], list)):
			semanticError = "Variable " + `currentDimensionedVariable` + " is not a struct"
			semanticErrorHalt()
		
		dim = 1
		pDimensionadas.append(currentDimensionedVariable)
		pDimensionadas.append(dim)
		currentStructDimension = vars_global[currentDimensionedVariable][1]

	elif varID in vars_local:
		if (not isinstance(vars_local[varID], list)):
			semanticError = "Variable " + `currentDimensionedVariable` + " is not a struct"
			semanticErrorHalt()
		
		dim = 1
		pDimensionadas.append(currentDimensionedVariable)
		pDimensionadas.append(dim)
		currentStructDimension = vars_local[currentDimensionedVariable][1]

	pilaO.append(FONDO_FALSO)

def p_errorOpStruct(p):
	'''errorOpStruct : '''
	global errorMsg
	errorMsg = "Error in rule OPSTRUCT"

# Access to Matrix
def p_opMatrix(p):
	'''opMatrix : errorOpMatrix updateDimension "[" expresion verifyIndex "]"
				| empty '''
	# print("optional matrix")

# Updates current dimension
def p_updateDimension(p):
	'''updateDimension : '''
	global dim
	global currentDimensionedVariable
	global currentStructDimension

	pDimensionadas.pop()
	pDimensionadas.pop()

	dim += 1
	pDimensionadas.append(currentDimensionedVariable)
	pDimensionadas.append(dim)

	currentStructDimension = currentStructDimension[3]

def p_errorOpMatrix(p):
	'''errorOpMatrix : '''
	global errorMsg
	errorMsg = "Error in rule ERROROPMATRIX"

# Constants
def p_cte(p):
	'''cte : CTED saveConstantInt
		| CTEF saveConstantFloat
		| TRUE saveConstantBool
		| FALSE saveConstantBool '''
	# print("cte")

# Empty rule
def p_empty(p):
	'''empty : '''
	# print("EMPTY")

def p_printTables(p):
	'''printTables : '''
	# print("\nCONSTANTS")
	# print(constants_table)
	# print("\nVARS GLOBAL")
	# print(vars_global)
	# print("\nDIR PROCS")
	# for x in range(0, len(dir_procs)):
	# 	print(dir_procs[x])
	# print("\nCUADRUPLOS")
	# for x in range(0, len(cuadruplos)):
	# 	print(x, cuadruplos[x])

	# print("\n")

def p_error(p):
	global line
	global errorMsg
	print("Error in line %d: Unexpected token '%s'" % (line, p.value))
	print('%s' % errorMsg)
	sys.exit()

# Save in Stacks - Next procedures work for IF-ELSE and CYCLE statements
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

# Saves constant INT to stacks and constant_table
def p_saveConstantInt(p):
		'''saveConstantInt : '''
		tokenToUse = currentToken

		if tokenToUse in avoidTokens:
			tokenToUse = previousToken

		if tokenToUse in constants_table:
			address = constants_table[tokenToUse]
		else:
			address = getAddressForConstant(INT)

			constants_table[tokenToUse] = address 

		pOper.append(address)
		pTipos.append(INT)

# Saves constant FLOAT to stacks and constant_table
def p_saveConstantFloat(p):
		'''saveConstantFloat : '''
		tokenToUse = currentToken

		if tokenToUse in avoidTokens:
			tokenToUse = previousToken

		if `tokenToUse` in constants_table:
			address = constants_table[`tokenToUse`]
		else:
			address = getAddressForConstant(FLOAT)

			constants_table[`tokenToUse`] = address 

		pOper.append(address)
		pTipos.append(FLOAT)

# Saves constant BOOL to stacks and constant_table
def p_saveConstantBool(p):
		'''saveConstantBool : '''
		tokenToUse = currentToken

		if tokenToUse in avoidTokens:
			tokenToUse = previousToken

		if tokenToUse in constants_table:
			address = constants_table[tokenToUse]
		else:
			address = getAddressForConstant(BOOL)

			constants_table[tokenToUse] = address 

		pOper.append(address)
		pTipos.append(BOOL)

# Saves constant STRING to stacks and constant_table	
def p_saveConstantString(p):
		'''saveConstantString : '''
		tokenToUse = currentToken

		if tokenToUse in avoidTokens:
			tokenToUse = previousToken

		tokenToUse = tokenToUse.replace("\"", "")

		if tokenToUse in constants_table:
			address = constants_table[tokenToUse]
		else:
			address = getAddressForConstant(STRING)

			constants_table[tokenToUse] = address

		pOper.append(address)
		pTipos.append(STRING)

# Save Variable to table - Validates existance
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

# Saves operator to stack
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
	elif previousToken == '%':
		pilaO.append(RESIDUE)
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

# Perform Semantic Actions Rules - Validate Semantic and save quadruple for specific operator

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

	if operator != MULTIPLY and operator != DIVISION and operator != RESIDUE:
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

def p_performRead(p):
	'''performRead : '''
	generateQuadruple(READ)	

# General Quadruple generator given an operator
def generateQuadruple(operator):
	global contQuadruples

	if operator == ERA:
		cuadruplo = (ERA, previousToken, "", "")
		cuadruplos.append(cuadruplo)
		contQuadruples += 1

		return

	if operator == RETORNO:
		cuadruplo = (RETORNO, "", "", "")
		cuadruplos.append(cuadruplo)
		contQuadruples += 1

		return

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

# Resaves pending quadruples
def rellena(salto, add):
	cuadruplo = cuadruplos[salto]
	operator = cuadruplo[0]
	falso = cuadruplo[1]
	opDer = cuadruplo[2]

	aux = (operator, falso, opDer, add)
	cuadruplos[salto] = aux

# Generates JUMP quadruple
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

# String to Int value of type variables
def typeToCode(type):
	switcher = {
		"int": 10,
		"float": 20,
		"bool": 30,
		"string": 40,
	}
	return switcher.get(type, 50)

# String to Int value of operators
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

# Gets a new global address for specified type
def getGlobalAddressForType(type):
	global contIntGlobal
	global contFloatGlobal
	global contBoolGlobal
	global contStringGlobal

	typeCode = typeToCode(type)
	
	if typeCode == INT:
		contIntGlobal += 1
		return contIntGlobal - 1

	if typeCode == FLOAT:
		contFloatGlobal += 1
		return contFloatGlobal - 1

	if typeCode == BOOL:
		contBoolGlobal += 1
		return contBoolGlobal - 1

	if typeCode == STRING:
		contStringGlobal += 1
		return contStringGlobal - 1

# Gets a new local address for specified type
def getAddressForType(type):
	global contInt
	global contFloat
	global contBool
	global contString
	global contIntGlobal
	global contFloatGlobal
	global contBoolGlobal
	global contStringGlobal

	typeCode = typeToCode(type)

	if currentScope == 'global':
		if typeCode == INT:
			contIntGlobal += 1
			return contIntGlobal - 1

		if typeCode == FLOAT:
			contFloatGlobal += 1
			return contFloatGlobal - 1

		if typeCode == BOOL:
			contBoolGlobal += 1
			return contBoolGlobal - 1

		if typeCode == STRING:
			contStringGlobal += 1
			return contStringGlobal - 1
	else:
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

# Gets a new constant address for specified type
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

# Gets a new temporal address for specified type
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

# Returns the type of a given address
def getTypeForAddress(address):
	if (address >= MIN_INT_GLOBAL and address <= MAX_INT_GLOBAL) or (address >= MIN_INT and address <= MAX_INT) or (address >= MIN_TEMP_INT and address <= MAX_TEMP_INT) or (address >= MIN_CONST_INT and address <= MAX_CONST_INT):
		return INT
	
	if (address >= MIN_FLOAT_GLOBAL and address <= MAX_FLOAT_GLOBAL) or (address >= MIN_FLOAT and address <= MAX_FLOAT) or (address >= MIN_TEMP_FLOAT and address <= MAX_TEMP_FLOAT) or (address >= MIN_CONST_FLOAT and address <= MAX_CONST_FLOAT):
		return FLOAT
	
	if (address >= MIN_BOOL_GLOBAL and address <= MAX_BOOL_GLOBAL) or (address >= MIN_BOOL and address <= MAX_BOOL) or (address >= MIN_TEMP_BOOL and address <= MAX_TEMP_BOOL) or (address >= MIN_CONST_BOOL and address <= MAX_CONST_BOOL):
		return BOOL
	
	if (address >= MIN_STRING_GLOBAL and address <= MAX_STRING_GLOBAL) or (address >= MIN_STRING and address <= MAX_STRING) or (address >= MIN_TEMP_STRING and address <= MAX_TEMP_STRING) or (address >= MIN_CONST_STRING and address <= MAX_CONST_STRING):
		return STRING

# Validates that an operation can be perfomes with the given operands
def typesValidator(left, right, operator):
	opMap = operator / 10 % 10

	if operator >= 200:
		opMap += 10

	return semanticCube[(left / 10 - 1) * 4 + (right / 10 - 1)][opMap]

import ply.yacc as yacc
parser = yacc.yacc()

def compile(fileName):
	file = open (fileName, "r");
	yacc.parse(file.read())
