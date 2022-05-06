import ply.lex as lex;

tokens = [
    'NUM', 'LP', 'RP', 'LB','RB','OP','EQ','COMA','LAM','ALPH','FV','ID','SEMI'
]

t_LP = r'\('
t_RP = r'\)'
t_LB = r'\['
t_RB = r'\]'
t_OP = r'[+\-/*]'
t_EQ = r'='
t_COMA = r','
t_ID = r"[a-zA-Z][a-zA-Z0-9']*"
t_SEMI = r';'


def t_LAM(t):
    r'[Ll][Aa][Mm][Bb][Dd][Aa]'
    t.type = "LAM"
    return t

def t_ALPH(t):
    r'[Aa][Ll][Pp][Hh][Aa]'
    t.type = "ALPH"
    return t

def t_FV(t):
    r'[Ff][Vv]'
    t.type = "FV"
    return t

def t_NUM(t):
    r'-?[0-9]+'
    t.value = float(t.value)
    return t


# Ignored characters
t_ignore = " \r\n\t"
t_ignore_COMMENT = r'\#.*'


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    raise Exception('Lexer Error')


lex.lex()


# lex.input("(lambda x (x y))[y = (u v)];")
# while True:
#     tok = lex.token()
#     if not tok:
#         break
#     print(tok)