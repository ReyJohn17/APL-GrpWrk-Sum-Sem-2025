import ply.yacc as yacc
from simplipyja_lexer import tokens

variables = {}

def p_program(p):
    'program : BEGIN stmt_list DONE'
    for stmt in p[2]:
        exec_stmt(stmt)

def p_stmt_list(p):
    '''stmt_list : stmt stmt_list
                 | '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_stmt(p):
    '''stmt : assignment
            | print_stmt
            | if_stmt
            | for_loop
            | natural_stmt'''
    p[0] = p[1]

def p_assignment(p):
    'assignment : MEK ID EQ expr'
    p[0] = ('assign', p[2], p[4])

def p_print_stmt(p):
    'print_stmt : FLING LPAREN STRING RPAREN'
    p[0] = ('print', p[3])

def p_if_stmt(p):
    '''if_stmt : IF expr BEGIN stmt_list DONE
               | IF expr BEGIN stmt_list DONE ELSE BEGIN stmt_list DONE'''
    if len(p) == 6:
        p[0] = ('if', p[2], p[4], [])
    else:
        p[0] = ('if', p[2], p[4], p[8])

def p_for_loop(p):
    'for_loop : FOR ID EQ expr TO expr BEGIN stmt_list DONE'
    p[0] = ('for', p[2], p[4], p[6], p[8])

def p_natural_stmt(p):
    '''natural_stmt : SET ID TO expr
                    | INCREASE ID BY expr'''
    if p[1] == 'set':
        p[0] = ('assign', p[2], p[4])
    else:
        p[0] = ('increase', p[2], p[4])

def p_expr_binop(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr MUL expr
            | expr DIV expr'''
    if p[2] == '+': p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expr_group(p): 'expr : LPAREN expr RPAREN'; p[0] = p[2]
def p_expr_number(p): 'expr : NUMBER'; p[0] = p[1]
def p_expr_id(p): 'expr : ID'; p[0] = variables.get(p[1], 0)

def p_error(p):
    print(f"Syntax error at '{p.value}'" if p else "Syntax error at EOF")

def exec_stmt(stmt):
    match stmt:
        case ('assign', name, val):
            variables[name] = val
        case ('increase', name, val):
            variables[name] = variables.get(name, 0) + val
        case ('print', msg):
            print(msg)
        case ('if', cond, then_stmts, else_stmts):
            branch = then_stmts if cond else else_stmts
            for stmt in branch:
                exec_stmt(stmt)
        case ('for', var, start, end, body):
            for i in range(start, end + 1):
                variables[var] = i
                for stmt in body:
                    exec_stmt(stmt)

parser = yacc.yacc()

if __name__ == "__main__":
    code = '''
    begin
        mek x = 10
        mek y = 5
        mek result = (x + y) * 2
        fling("Starting Loop...")
        for i = 1 to 3
        begin
            increase result by i
        Done
        if result > 30
        begin
            fling("Result is large")
        Done
        else
        begin
            fling("Result is small")
        Done
    Done
    '''
    parser.parse(code)
