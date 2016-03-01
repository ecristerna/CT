import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

literals = ['{','}',',',';','=','(',')','[', ']', '>', '<', '+','-','*','/', ':', '.']
reserved = ['PROGRAM','STRUCT','DICT','FUNC','RETURNS','RETURN','INT', 'FLOAT', 'STRING', 'OBJECT', 'BOOL', 'TRUE', 'FALSE', 'VARS', 'MAIN', 'AND', 'OR', 'WHILE', 'FOR', 'IF', 'ELSE', 'FIRST', 'LAST',]
tokens = ['GTOEQ', 'LTOEQ','DIF', 'EQ','ID','CTED','CTEF','CTES',] + reserved

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
    r'\n+'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

def p_program(p):
    '''program : PROGRAM ID "{" opVars opFunctions main "}"'''
    print("program")
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
	'''vars : VARS declare '''
	print("vars")
	pass

def p_type(p):
	'''type : INT
			| FLOAT
			| STRING
			| OBJECT
			| BOOL'''
	print("type")
	pass

def p_main(p):
	'''main : MAIN "{" opVars body "}"'''
	print("main")
	pass

def p_instr(p):
	'''instr : c ";"
			| condition
			| cycle '''
	print("instr")
	pass
def p_c(p):
	'''c : assign
		| funcCall '''
	pass

def p_declare(p):
	'''declare : d
			| e
			| f '''
	print("declare")
	pass

def p_init(p):
	'''init : "=" i '''
	print("init")
	pass

def p_i(p):
	'''i : expresion
		| funcCall '''
	print("i")
	pass

def p_initDict(p):
	'''initDict : "=" "(" j ":" j ")" '''
	print("initDict")
	pass

def p_j(p):
	'''j : CTES
		| cte
		| ID '''
	print("j")
	pass

def p_param(p):
	'''param : type ID g k '''
	print("param")
	pass

def p_k(p):
	'''k : ";" param
		| empty '''
	print("k")
	pass

def p_function(p):
	'''function : FUNC ID opParameters opReturns "{" opVars body "}" '''
	print("function")
	pass

def p_opParameters(p):
	'''opParameters : "(" param ")"
					| empty '''
	print("optional parameters")
	pass

def p_opReturns(p):
	'''opReturns : RETURNS type
		| empty '''
	print("returns")
	pass

def p_d(p):
	'''d : type ID g ";" h '''
	print("d")
	pass

def p_e(p):
	'''e : STRUCT ID struct ";" h '''
	print("e")
	pass

def p_f(p):
	'''f : DICT ID dict ";" h '''
	print("f")
	pass

def p_g(p):
	'''g : "," ID
		| empty '''
	print("g")
	pass

def p_h(p):
	'''h : declare
		| empty '''
	print("h")
	pass

def p_body(p):
	'''body : cyInstruction
			| empty '''
	print("body")
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
	'''whileCycle : WHILE "(" expresion ")" "{" body "}" '''
	print("while")
	pass

def p_forCycle(p):
	'''forCycle : FOR "(" assign ";" expresion ";" assign ")" "{" body "}" '''
	print("for")
	pass

def p_assign(p):
	'''assign : ID assignOptions '''
	print("assign")
	pass

def p_assignOptions(p):
	'''assignOptions : init
					| initDict
					| "[" expresion "]" assignMatrix init '''
	print("assignOptions")
	pass

def p_assignMatrix(p):
	'''assignMatrix : "[" expresion "]"
					| empty '''
	print("assignMatrix")
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
	'''struct : type "[" CTED "]" optionalMatrix '''
	print("struct")
	pass

def p_optionalMatrix(p):
	'''optionalMatrix : "[" CTED "]"
					| empty '''
	print("matrix")
	pass

def p_condition(p):
	'''condition : IF "(" expresion ")" "{" body "}" optionalElse '''
	print("condition")
	pass

def p_optionalElse(p):
	'''optionalElse : ELSE "{" body "}"
					| empty '''
	print("else")
	pass

def p_dict(p):
	'''dict : "(" type ":" type ")" '''
	print("dict")
	pass

def p_expresion(p):
	'''expresion : sExp cyExpresion '''
	print("expresion")
	pass

def p_cyExpresion(p):
	'''cyExpresion : AND expresion
				| OR expresion
				| empty '''
	print("cycle expresion")
	pass

def p_sExp(p):
	'''sExp : exp opSExp '''
	print("super expresion")
	pass

def p_opSExp(p):
	'''opSExp : EQ exp
			| DIF exp
			| LTOEQ exp
			| GTOEQ exp
			| ">" exp
			| "<" exp
			| empty '''
	print("cycle super expresion")
	pass

def p_exp(p):
	'''exp : term cyExp '''
	print("exp")
	pass

def p_cyExp(p):
	'''cyExp : "+" term
			| "-" term
			| empty '''
	print("cycle exp")
	pass

def p_term(p):
	'''term : fact cyTerm '''
	print("term")
	pass

def p_cyTerm(p):
	'''cyTerm : "*" fact
			| "/" fact
			| empty '''
	print("cycle term")
	pass

def p_fact(p):
	'''fact : CTES
			| cte
			| funcCall
			| "(" expresion ")"
			| ID opAccess '''
	print("fact")
	pass	

def p_opAccess(p):
	'''opAccess : opStruct
				| opDictionary
				| empty '''
	print("optional access")
	pass

def p_opStruct(p):
	'''opStruct : "[" expresion "]" opMatrix '''
	print("optional struct")
	pass

def p_opMatrix(p):
	'''opMatrix : "[" expresion "]"
				| empty '''
	print("optional matrix")
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
    print("Syntax error")

import ply.yacc as yacc
parser = yacc.yacc()

file = open ("input.txt", "r");
yacc.parse(file.read())