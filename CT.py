import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

literals = ['{','}',',',';','=','(',')','[', ']', '>', '<', '+','-','*','/', ':', '.']
reserved = ['PROGRAM','STRUCT','DICT','FUNC','RETURNS','RETURN','INT', 'FLOAT', 'STRING', 'OBJECT', 'BOOL', 'TRUE', 'FALSE', 'VARS', 'MAIN', 'AND', 'OR', 'WHILE', 'FOR', 'IF', 'ELSE', 'FIRST', 'LAST',]
tokens = ['GTOEQ', 'LTOEQ','DIF', 'EQ','ID','CTED','CTEF','CTES',] + reserved

line = 1
errorMsg = ""

# Tokens

t_ignore = " \t"
t_DIF = "!="
t_EQ = "=="
t_GTOEQ = ">="
t_LTOEQ = "<="

def t_CTEF(t):
    r'(\d+)(\.\d+)'
    t.value = float(t.value)
    return t

def t_CTED(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value,"ID")
    return t

def t_CTES(t):
    r'\"([^\\\n]|(\\.))*?\"'
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
    '''program : errorProgram PROGRAM ID "{" opVars opFunctions main "}"'''
    print("program")
    pass

def p_errorProgram(p):
	'''errorProgram : '''
	global errorMsg
	errorMsg = "Error in rule PROGRAM"
	pass

def p_opVars(p):
	'''opVars : vars
			| empty'''
	print("optional vars")
	pass

def p_opFunctions(p):
	'''opFunctions : function opFunctions
				| empty'''
	pass

def p_vars(p):
	'''vars : errorVars VARS declare '''
	print("vars")
	pass

def p_errorVars(p):
	'''errorVars : '''
	global errorMsg
	errorMsg = "Error in rule VARS"
	pass

def p_type(p):
	'''type : errorType INT
			| FLOAT
			| STRING
			| OBJECT
			| BOOL'''
	print("type")
	pass

def p_errorType(p):
	'''errorType : '''
	global errorMsg
	errorMsg = "Error in rule TYPE"
	pass

def p_main(p):
	'''main : errorMain MAIN "{" opVars body "}"'''
	print("main")
	pass

def p_errorMain(p):
	'''errorMain : '''
	global errorMsg
	errorMsg = "Error in rule MAIN"
	pass

def p_instr(p):
	'''instr : basicStatements ";"
			| condition
			| cycle '''
	print("instr")
	pass
def p_basicStatements(p):
	'''basicStatements : assign
					| funcCall '''
	pass

def p_declare(p):
	'''declare : basicDeclare
			| structDeclare
			| dictDeclare '''
	print("declare")
	pass

def p_init(p):
	'''init : "=" initWith errorInit'''
	print("init")
	pass

def p_errorInit(p):
	'''errorInit : '''
	global errorMsg
	errorMsg = "Error in rule INIT"
	pass

def p_initWith(p):
	'''initWith : expresion
		| funcCall '''
	print("init with")
	pass

def p_initDict(p):
	'''initDict : "=" "(" dictType ":" dictType ")" errorInitDict'''
	print("initDict")
	pass

def p_errorInitDict(p):
	'''errorInitDict : '''
	global errorMsg
	errorMsg = "Error in rule INITDICT"
	pass

def p_dictType(p):
	'''dictType : errorDictType CTES
				| cte
				| ID '''
	print("dict type")
	pass

def p_errorDictType(p):
	'''errorDictType : '''
	global errorMsg
	errorMsg = "Error in rule DICTTYPE. Dictionary not initialized."
	pass

def p_param(p):
	'''param : type errorParam ID cyTypeParam cyParam '''
	print("param")
	pass

def p_errorParam(p):
	'''errorParam : '''
	global errorMsg
	errorMsg = "Error in rule PARAM"
	pass

def p_cyParam(p):
	'''cyParam : errorCyParam ";" param
		| empty '''
	print("cycle param")
	pass

def p_errorCyParam(p):
	'''errorCyParam : '''
	global errorMsg
	errorMsg = "Error in rule CYPARAM. Missing ; "
	pass

def p_function(p):
	'''function : errorFunction FUNC ID opParameters opReturns  "}" '''
	print("function")
	pass

def p_errorFunction(p):
	'''errorFunction : '''
	global errorMsg
	errorMsg = "Error in rule FUNCTION"
	pass

def p_return(p):
	'''return : errorReturn RETURN expresion ";" '''
	print("return")
	pass

def p_errorReturn(p):
	'''errorReturn : '''
	global errorMsg
	errorMsg = "Error in rule RETURN"
	pass

def p_opParameters(p):
	'''opParameters : "(" param ")" errorOpParameters
					| empty '''
	print("optional parameters")
	pass

def p_errorOpParameters(p):
	'''errorOpParameters : '''
	global errorMsg
	errorMsg = "Error in rule OPPARAMETERS"
	pass

def p_opReturns(p):
	'''opReturns : errorOpReturns RETURNS type "{" opVars body return
		| "{" opVars body '''
	print("returns")
	pass

def p_errorOpReturns(p):
	'''errorOpReturns : '''
	global errorMsg
	errorMsg = "Error in rule OPRETURNS"
	pass

def p_basicDeclare(p):
	'''basicDeclare : type errorBasicDeclare ID cyTypeParam ";" cyDeclare '''
	print("basic declare")
	pass

def p_errorBasicDeclare(p):
	'''errorBasicDeclare : '''
	global errorMsg
	errorMsg = "Error in rule BASICDECLARE"
	pass

def p_structDeclare(p):
	'''structDeclare : errorStructDeclare STRUCT ID struct ";" cyDeclare '''
	print("struct declare")
	pass

def p_errorStructDeclare(p):
	'''errorStructDeclare : '''
	global errorMsg
	errorMsg = "Error in rule STRUCTDECLARE"
	pass

def p_dictDeclare(p):
	'''dictDeclare : errorDictDeclare DICT ID dict ";" cyDeclare '''
	print("dict declare")
	pass

def p_errorDictDeclare(p):
	'''errorDictDeclare : '''
	global errorMsg
	errorMsg = "Error in rule DICTDECLARE"
	pass

def p_cyTypeParam(p):
	'''cyTypeParam : "," ID
		| empty '''
	print("cycle type param")
	pass

def p_cyDeclare(p):
	'''cyDeclare : declare
		| empty '''
	print("cycle declare")
	pass

def p_body(p):
	'''body : errorBody cyInstruction
			| empty '''
	print("body")
	pass

def p_errorBody(p):
	'''errorBody : '''
	global errorMsg
	errorMsg = "Error in rule BODY"
	pass

def p_cyInstruction(p):
	'''cyInstruction : instr body '''
	print("cycleInstruction")
	pass

def p_cycle(p):
	'''cycle : forCycle
			| whileCycle '''
	print("cycle")
	pass

def p_whileCycle(p):
	'''whileCycle : errorWhileCycle WHILE "(" expresion ")" "{" body "}" '''
	print("while")
	pass

def p_errorWhileCycle(p):
	'''errorWhileCycle : '''
	global errorMsg
	errorMsg = "Error in rule WHILECYCLE"
	pass

def p_forCycle(p):
	'''forCycle : errorForCycle FOR "(" assign ";" expresion ";" assign ")" "{" body "}" '''
	print("for")
	pass

def p_errorForCycle(p):
	'''errorForCycle : '''
	global errorMsg
	errorMsg = "Error in rule FORCYCLE"
	pass

def p_assign(p):
	'''assign :  ID errorAssign assignOptions '''
	print("assign")
	pass
    
def p_errorAssign(p):
	'''errorAssign : '''
	global errorMsg
	errorMsg = "Error in rule ASSIGN"
	pass

def p_assignOptions(p):
	'''assignOptions : init
					| initDict
					| "[" expresion "]" assignMatrix init '''
	print("assignOptions")
	pass

def p_assignMatrix(p):
	'''assignMatrix : "[" expresion "]" errorAssignMatrix
					| empty '''
	print("assignMatrix")
	pass

def p_errorAssignMatrix(p):
	'''errorAssignMatrix : '''
	global errorMsg
	errorMsg = "Error in rule ASSIGNMATRIX"
	pass

def p_funcCall(p):
	'''funcCall : ID "(" opParamCall ")" '''
	print("funcCall")
	pass

def p_opParamCall(p):
	'''opParamCall : expresion cyParamCall
				| empty '''
	print("function parameter")
	pass

def p_cyParamCall(p):
	'''cyParamCall : "," expresion cyParamCall
				| empty '''
	print("cycle parameter call")
	pass

def p_struct(p):
	'''struct : structType "[" CTED "]" optionalMatrix '''
	print("struct")
	pass

def p_structType(p):
	'''structType : type
				| DICT dict '''
	print("struct type")
	pass

def p_optionalMatrix(p):
	'''optionalMatrix : "[" CTED "]"
					| empty '''
	print("matrix")
	pass

def p_condition(p):
	'''condition : errorCondition IF "(" expresion ")" "{" body "}" optionalElse '''
	print("condition")
	pass

def p_errorCondition(p):
	'''errorCondition : '''
	global errorMsg
	errorMsg = "Error in rule CONDITION"
	pass

def p_optionalElse(p):
	'''optionalElse : errorElse ELSE "{" body "}"
					| empty '''
	print("else")
	pass

def p_errorElse(p):
	'''errorElse : '''
	global errorMsg
	errorMsg = "Error in rule OPTIONALELSE"
	pass

def p_dict(p):
	'''dict : errorDict "(" type ":" type ")" '''
	print("dict")
	pass

def p_errorDict(p):
	'''errorDict : '''
	global errorMsg
	errorMsg = "Error in rule DICT"
	pass

def p_expresion(p):
	'''expresion : sExp cyExpresion errorExpresion '''
	print("expresion")
	pass

def p_errorExpresion(p):
	'''errorExpresion : '''
	global errorMsg
	errorMsg = "Error in rule EXPRESION"
	pass

def p_cyExpresion(p):
	'''cyExpresion : AND expresion
				| OR expresion
				| empty '''
	print("cycle expresion")
	pass

def p_sExp(p):
	'''sExp : exp errorOpSExp opSExp '''
	print("super expresion")
	pass

def p_opSExp(p):
	'''opSExp :  EQ exp
			| DIF exp
			| LTOEQ exp
			| GTOEQ exp
			| ">" exp
			| "<" exp
			| empty '''
	print("cycle super expresion")
	pass

def p_errorOpSExp(p):
	'''errorOpSExp : '''
	global errorMsg
	errorMsg = "Error in rule OPSEXP"
	pass

def p_exp(p):
	'''exp : term errorCyExp cyExp '''
	print("exp")
	pass

def p_cyExp(p):
	'''cyExp : "+" term
			| "-" term
			| empty '''
	print("cycle exp")
	pass

def p_errorCyExp(p):
	'''errorCyExp : '''
	global errorMsg
	errorMsg = "Error in rule CYEXP"
	pass

def p_term(p):
	'''term : fact cyTerm '''
	print("term")
	pass

def p_cyTerm(p):
	'''cyTerm : "*" errorFact fact
			| "/" fact
			| empty '''
	print("cycle term")
	pass

def p_fact(p):
	'''fact : CTES
			| cte
			| funcCall
			| "(" expresion ")"
			| ID opAccess errorOpAccess'''
	print("fact")
	pass	

def p_errorFact(p):
	'''errorFact : '''
	global errorMsg
	errorMsg = "Error in rule ERRORFACT"
	pass

def p_opAccess(p):
	'''opAccess : opStruct
				| opDictionary
				| empty '''
	print("optional access")
	pass

def p_errorOpAccess(p):
	'''errorOpAccess : '''
	global errorMsg
	errorMsg = "Error in rule ERROROPACCESS"
	pass

def p_opStruct(p):
	'''opStruct : errorOpStruct "[" expresion "]" opMatrix '''
	print("optional struct")
	pass

def p_errorOpStruct(p):
	'''errorOpStruct : '''
	global errorMsg
	errorMsg = "Error in rule OPSTRUCT"
	pass

def p_opMatrix(p):
	'''opMatrix : errorOpMatrix "[" expresion "]"
				| empty '''
	print("optional matrix")
	pass

def p_errorOpMatrix(p):
	'''errorOpMatrix : '''
	global errorMsg
	errorMsg = "Error in rule ERROROPMATRIX"
	pass

def p_opDictionary(p):
	'''opDictionary : "." dictIndex '''
	print("optional dictionary")
	pass

def p_dictIndex(p):
	'''dictIndex : FIRST
				| LAST '''
	print("dictionary index")
	pass

def p_cte(p):
	'''cte : CTED
		| CTEF 
		| TRUE 
		| FALSE '''
	print("cte")
	pass

def p_empty(p):
    'empty : '
    print("EMPTY")
    pass

def p_error(p):
	global line
	global errorMsg
	print("Error in line %d: Unexpected token '%s'" % (line, p.value))
	print('%s' % errorMsg)
	sys.exit()

import ply.yacc as yacc
parser = yacc.yacc()

file = open ("input.txt", "r");
yacc.parse(file.read())
