from LambdaLexer import tokens
import ply.yacc as yacc
from LambdaNode import Node


def p_normal_start(p):
    '''exprStart : expr SEMI'''
    # p[0] = str(p[1])
    p[0] = p[1]


def p_substiute_start(p):
    '''exprStart : expr LB ID EQ expr RB SEMI'''
    # p[0] = str(p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7])
    substitue = Node()
    substitue.method = 'sub'
    substitue.var = p[3]
    substitue.left = p[1]
    substitue.right = p[5]
    p[0] = substitue


def p_free_variable_start(p):
    '''exprStart : FV LB expr RB SEMI'''
    # p[0] = str(p[1] + p[2] + p[3] + p[4] + p[5])
    freeVariable = Node()
    freeVariable.method = 'frV'
    freeVariable.left = p[3]
    p[0] = freeVariable


def p_alpha_start(p):
    '''exprStart : ALPH LB expr COMA ID RB SEMI'''
    # p[0] = str(p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7])
    alpha = Node()
    alpha.method = 'alpha'
    alpha.left = p[3]
    alpha.var = p[5]
    p[0] = alpha


def p_expression_terminals(p):
    '''expr : NUM
            | ID'''
    terminal_node = Node()
    if isinstance(p[1], float):
        terminal_node.type = 'num'
        terminal_node.val = p[1]
    else: 
        terminal_node.type = 'var'
        terminal_node.var = p[1]
        terminal_node.free_var = p[1]
        terminal_node.free_vars.add(p[1])
    p[0] = terminal_node


def p_expression_body(p):
    '''expr : LP expr expr RP'''
    # p[0] = str(p[1] + p[2] + p[3] + p[4])
    body = Node()
    body.type = 'apply'
    body.left = p[2]
    body.right = p[3]
    body.free_vars = body.free_vars.union(body.left.free_vars, body.right.free_vars)
    p[0] = body


def p_expression_operation_body(p):
    '''expr : LP OP expr expr RP'''
    # p[0] = str(p[1] + p[2] + p[3] + p[4] + p[5])
    oper = Node()
    oper.type = 'oper'
    oper.op = p[2]
    oper.left = p[3]
    oper.right = p[4]
    oper.free_vars = oper.free_vars.union(oper.left.free_vars, oper.right.free_vars)
    p[0] = oper 


def p_expression_abstraction(p):
    '''expr : LP LAM ID expr RP'''
    # p[0] = str(p[1] + p[2] + p[3] + p[4] + p[5])
    abstract = Node()
    abstract.type = 'lambda'
    abstract.var = p[3]
    abstract.left = p[4]
    abstract.free_vars = abstract.left.free_vars.copy()
    if p[3] in abstract.free_vars: abstract.free_vars.remove(p[3])
    p[0] = abstract


def p_error(p):
    print("Error in the parser")


parser = yacc.yacc()
