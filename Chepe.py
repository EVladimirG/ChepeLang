from ply import lex, yacc
import sys
import os

import logging
logging.getLogger('ply').disabled = True

tokens = (
    'NUMBER',
    'PLUS',
    'TIMES',
    'LPAREN',
    'RPAREN',
    'CHEPE',
    'STRING',
    'VARIABLE',
    'EQUALS'
)

variables = {}

t_PLUS = r'\+'
t_TIMES = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'\='
t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CHEPE(t):
    r'Chepe'
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Remover comillas dobles
    return t

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_error(t):
    print("\tHubo un error en esta línea, contacta con Vladimir, si eres Vladimir y no sabes por qué hubo un error, reza a tu entidad divina de preferencia")
    os.system("pause")
    exit()

def p_statement(p):
    '''
    statement : CHEPE LPAREN expression RPAREN
             | CHEPE LPAREN ChepeVar RPAREN
    '''
    p[0] = p[3]

def p_expression_variable(p):
    '''
    expression : VARIABLE
    '''
    if p[1] in variables:
        p[0] = variables[p[1]]
    else:
        print("Variable no definida:", p[1])
        p[0] = None

def p_ChepeVar(p):
    '''
    ChepeVar : VARIABLE EQUALS expression
                        | VARIABLE
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if isinstance(p[3], tuple) and p[3][0] == 'ChepeVar':
            variables[p[1]] = variables[p[3][1]]
        else:
            variables[p[1]] = p[3]
        p[0] = ('ChepeVar', p[1], p[3])


def p_expression_string(p):
    '''
    expression : STRING
    '''
    p[0] = p[1]

def p_expression_plus(p):
    '''
    expression : expression PLUS term
    '''
    p[0] = p[1] + p[3]

def p_expression_term(p):
    '''
    expression : term
    '''
    p[0] = p[1]

def p_term_times(p):
    '''
    term : term TIMES factor
    '''
    p[0] = p[1] * p[3]

def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]

def p_factor_number(p):
    '''
    factor : NUMBER
    '''
    p[0] = p[1]

def p_factor_expression(p):
    '''
    factor : LPAREN expression RPAREN
    '''
    p[0] = p[2]

def p_error(p):
    pass
    #print("Error de sintaxis")

lexer = lex.lex()

parser = yacc.yacc()

def ejecutar_desde_archivo(filename):
    with open(filename, 'r') as f:
        expresiones = f.readlines()
        os.system("cls")
        for exp in expresiones:
            exp = exp.strip()
            if exp:
                if '=' in exp:
                    var, val = exp.split('=')
                    var = var.strip()
                    val = val.strip()
                    try:
                        val = int(val)
                    except ValueError:
                        pass  # Si no es un entero, lo dejamos como está
                    variables[var] = val
                else:
                    resultado = parser.parse(exp)
                    print(resultado)
archivo = sys.argv[1]
ejecutar_desde_archivo(archivo)
print('\t\t\t')
os.system("pause")
