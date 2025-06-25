import ply.lex as lex

tokens = [
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'MUL', 'DIV',
    'EQ', 'LPAREN', 'RPAREN',
    'COMMENT'
] + [
    'MEK', 'IF', 'ELSE', 'BEGIN', 'DONE', 'FOR', 'TO', 'SET', 'INCREASE', 'FLING'
]

# Reserved words mapping
reserved = {
    'mek': 'MEK', 'if': 'IF', 'else': 'ELSE', 'begin': 'BEGIN',
    'Done': 'DONE', 'for': 'FOR', 'to': 'TO', 'set': 'SET',
    'increase': 'INCREASE', 'fling': 'FLING'
}

# Token regex rules
t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_EQ = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'[+-]?\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    r'\"[^"\n]*\"'
    t.value = t.value[1:-1]
    return t

def t_COMMENT(t): r'\#.*'; pass
def t_newline(t): r'\n+'; t.lexer.lineno += len(t.value)
def t_error(t): print(f"Illegal character: {t.value[0]}"); t.lexer.skip(1)

lexer = lex.lex()
