from sympy import *

tokens = (
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN', 'MIN', 'COMMA', 'SUBJECT_TO'
    )

# Tokens for simple symbols

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_COMMA = r'\,'

def t_SUBJECT_TO(t):
	r'subject\ to'
	return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_MIN(t):
    r'min'
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# dictionary of variable names
names = { }

# dictionary of optimization formulations
optimization_formulations = []

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    print(t[1])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

# The first register is the return value.
def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_statement_optimization(t):
    '''statement : MIN expression
    			 | MIN expression COMMA expression
    			 | MIN expression COMMA expression COMMA expression
    '''
    optimization_formulations.append({"problem": t, "constraints": []})

def p_statement_subject_to(t):
	'statement : SUBJECT_TO expression'
	optimization_formulations[-1]["constraints"].append(t)

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Symbol not found -- autogenerating")
        names[t[1]] = symbols(t[1])
        t[0] = symbols(t[1])

def p_error(t):
    print("Syntax error at '%s'" % t.value)

def parse_optimization_model(user_string, compiler_type="actual"):
    formulation = None
    constraints = []

    if compiler_type == "manual":

        for t in user_string.split("\n"):
            if t.startswith("min") or t.startswith("max"):
                formulation = t.split(" ")[1:]
                break
        for t in user_string.split("\n"):
            if t.startswith("subject to"):
                constraints.append(t.split(" ")[2:])

        return formulation, constraints
    if compiler_type == "actual":
        import ply.yacc as yacc
        parser = yacc.yacc()

        for ff in user_string.split("\n"):
            parser.parse(ff)

    objective_function = optimization_formulations[0]["problem"][2]
    constraints = []
    variables = name
    for i in range(len(optimization_formulations[0]["constraints"])):
        constraints.append(optimization_formulations[0]["constraints"][i][2])

    return objective_function, constraints, variables

if __name__ == "__main__":
    d = """
min 5*x + 8*x
subject to x*2
    """
    parse_optimization_model(d.strip())

