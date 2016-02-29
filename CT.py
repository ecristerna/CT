import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

literals = ['{','}',',',';','=','(',')','[', ']', '>', '<', '+','-','*','/']
reserved = ['PROGRAM','STRUCT','DICT','FUNC','RETURNS','RETURN','INT', 'FLOAT', 'STRING', 'OBJECT', 'BOOL', 'TRUE', 'FALSE', 'VARS', 'MAIN', 'AND', 'OR', 'WHILE', 'FOR', 'IF', 'ELSE',]
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
    '''program : PROGRAM ID "{" a b main "}"'''
    print("program")
    pass

def p_a(p):
	'''a : vars
		| empty'''
	print("a")
	pass

def p_b(p):
	'''b : function b
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
	'''main : MAIN "{" a body "}"'''
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
	'''function : FUNC ID l m "{" a body "}" '''
	print("function")
	pass

def p_l(p):
	'''l : "(" param n ")" '''
	print("l")
	pass

def p_n(p):
	'''n : param
		| empty '''
	print("n")
	pass

def p_m(p):
	'''m : RETURNS type
		| empty '''
	print("m")
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
	'''body : empty'''
	print("body")
	pass

def p_cycle(p):
	'''cycle : empty'''
	print("cycle")
	pass

def p_assign(p):
	'''assign : empty'''
	print("assign")
	pass

def p_funcCall(p):
	'''funcCall : empty'''
	print("funcCall")
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
	'''condition : empty'''
	print("condition")
	pass

def p_dict(p):
	'''dict : empty'''
	print("dict")
	pass

def p_expresion(p):
	'''expresion : empty'''
	print("expresion")
	pass

def p_cte(p):
	'''cte : empty'''
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