import uuid
from ply import lex

class Symbol(str):
    pass

tokens = (
    'OPEN',
    'CLOSE',
    'NULL',
    'NAME',
    'SYMBOL',
    'STRING',
    'UUID',
    'FLOAT',
    'INT',
    )

# Tokens

t_OPEN   = r'<'
t_CLOSE  = r'>'

def t_NAME(t):
    r'[A-Z][A-Z0-9_]*(?=\s+)'
    return t

def t_UUID(t):
    r"(?P<quote>(?:'?))\{[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\}(?P=quote)"
    t.value = uuid.UUID(t.value.strip("'"))
    return t

def t_STRING(t):
    r'(?:"([^"]*)")|(?:\'([^\']*)\')'
    if t.value[0] == '"':
        t.value = t.value.strip('"')
    else:
        t.value = t.value.strip("'")
    return t

def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_NULL(t):
    r'-'
    t.value = None
    return t

def t_SYMBOL(t):
    r'[a-zA-Z0-9_+/:=]+'
    t.value = Symbol(t.value)
    return t

# Ignored characters
t_ignore = ' \t'

def t_newline(t): 
    r'[\r\n]+'
    t.lexer.lineno += len(t.value.splitlines())

def t_error(t):
    args = t.value[0], t.lineno or 0
    message = "Scanning error. Illegal character '%s' at line %d" % args
    raise lex.LexError(message, '')

lex.lex()

def tokenize(string):
    lex.input(string)
    while True:
        tok = lex.token()
        if not tok: 
            break
        yield tok
