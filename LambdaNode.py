import copy

class Node:
    """Summary
        var: Variable 
        num: Number  
        apply: (M N) 
        oper: (* M N) 
        lambda: (lambda.M N)
        Method:
            frV: fv[(lambda M (M N))]; -> {N}
            alpha: alpha[(lambda x (x y)),z]; -> (lambda z (z y))
            sub: (lambda x (x y))[y = (u v)]; -> (lambda x (x (u v)))
    """

    def __init__(self):
        self.type = ''          
        self.method = ''
        self.var = ''
        self.free_vars = set({})
        self.val = None
        self.op = ''
        self.left = ''
        self.right = ''
        self.CONST = 8

    def toObj(self, n: int)->str:
        result = '{'+ ' '*n + '\n'
        tab = ' '*n
        if (self.type == 'num'):
            result += f"{tab}Type: {self.type}\n{tab}Value: {self.val}\n"
        
        elif(self.type == 'var'):
            result += f"{tab}Type: {self.type}\n{tab}Var: {self.var}\n{tab}FreeVar: {self.free_vars}\n"
        
        elif(self.type == 'oper'):
            result += f"{tab}Type: {self.type}\n{tab}FreeVar: {self.free_vars}\n{tab}Operator: {self.op}\n{tab}Left: {self.left.toObj(n+self.CONST) if self.left != '' else ''}\n{tab}Right: {self.right.toObj(n+self.CONST) if self.right != '' else ''}\n"
        
        elif(self.type == 'apply'):
            result += f"{tab}Type: {self.type}\n{tab}FreeVar: {self.free_vars}\n{tab}Left: {self.left.toObj(n+self.CONST) if self.left != '' else ''}\n{tab}Right: {self.right.toObj(n+self.CONST) if self.right != '' else ''}\n"
        
        elif(self.type == 'lambda'):
            result += f"{tab}Type: {self.type}\n{tab}BoundVar: {self.var}\n{tab}FreeVar: {self.free_vars}\n{tab}Left: {self.left.toObj(n+self.CONST) if self.left != '' else ''}\n"
        
        elif (self.type == '' and self.method == 'frV'): 
            result += f"{tab}Method: {self.method}\n{tab}Left:{self.left.toObj(n+self.CONST) if self.left != '' else ''}\n" 
        
        elif (self.type == '' and self.method == 'sub'): 
            result += f"{tab}Method: {self.method}\n{tab}Substitue Var: {self.var}\n{tab}Sub To:{self.left.toObj(n+self.CONST) if self.left != '' else ''}\n{tab}Sub From: {self.right.toObj(n+self.CONST) if self.right != '' else ''}\n" 
        
        elif (self.type == '' and self.method == 'alpha'): 
            result += f"{tab}Method: {self.method}\n{tab}Replace By: {self.var}\n{tab}Replace In:{self.left.toObj(n+self.CONST) if self.left != '' else ''}\n" 
        
        else:
            pass
            # result += f"{tab}Type: {self.type}\n{tab}BoundVar: {self.var}\n{tab}Var: {self.var}\n{tab}FreeVar: {self.free_vars}\n{tab}Value: {self.val}\n{tab}Operator: {self.op}\n{tab}Left: {self.left.toObj(n+self.CONST) if self.left != '' else ''}\n{tab}Right: {self.right.toObj(n+self.CONST) if self.right != '' else ''}\n"
        return  result + ' '*(n-2) + '}'


    def __str__(self):
        return self.toObj(2)


class Solver:
    def __init__(self):
        pass
    
    @staticmethod
    def solvethis(node: Node, exec: int):
        if node == None:
            return 
        flag = False 
        if 1 in exec:
            flag = True
        if node.method == 'frV':
            node = Solver.free_vars(node.left)
            print(f"Free variables: {node.free_vars}")
        elif node.method == 'alpha':
            node = Solver.alpha(node.left, node.var)
            print(Solver.tree_to_string(node))
        elif node.method == 'sub':
            node = Solver.substitue(node.left, [node.var, node.right])
            print(Solver.tree_to_string(node))
        elif node.type != '':
            node = Solver.beta_reduction(node, flag)
            print(f"ANSWER>> {Solver.tree_to_string(node)}")

        return node
    
    @staticmethod
    def tree_to_string(node: Node):
        if node.type == 'lambda':
            return f"(lambda {node.var} {Solver.tree_to_string(node.left)})"
        elif node.type == 'apply':
            return f"({Solver.tree_to_string(node.left)} {Solver.tree_to_string(node.right)})"
        elif node.type == 'num':
            return f"{node.val}"
        elif node.type == 'var':
            return f"{node.var}"
        elif node.type == 'oper':
            return f"({node.op} {Solver.tree_to_string(node.left)} {Solver.tree_to_string(node.right)})"
        else:
            return ""
            
    @staticmethod
    def free_vars(node: Node):
        if node.left != '':
            Solver.free_vars(node.left)
        if node.right != '':
            Solver.free_vars(node.right)
        if node.type == 'var':
            node.free_vars = set({node.var})
        elif node.type == 'apply' or node.type == 'oper':
            node.free_vars = node.left.free_vars.union(node.right.free_vars)
        elif node.type == 'lambda':
            node.free_vars = node.left.free_vars
            if node.var in node.free_vars: node.free_vars.remove(node.var)
        return node
    
    @staticmethod
    def alpha(node: Node, replace_to: str):
        replace_this = node.var
        def solve(node: Node, this: str, by: str):
            if node.left != '':
                solve(node.left, this, by)
            if node.right != '':
                solve(node.right, this, by)
            if node.var == this:
                node.var = by

        solve(node, replace_this, replace_to)
        Solver.free_vars(node)
        return node
    
    @staticmethod
    def substitue(node: Node, sub: list):
        # print(f"SUBSTITUE: {Solver.tree_to_string(node)}")
        # print(f"VAR: {sub[0]}")
        # print(f"TO: {Solver.tree_to_string(sub[1])}")
        save = node
        def solve(node: Node, sub: list):
            if(node.type == "num"): return node
            elif (node.type == 'var') and node.var == sub[0]:
                node = sub[1]
            elif (node.type == "apply"):
                node.left = solve(node.left, sub)
                node.right = solve(node.right, sub)
            elif (node.type == "oper"):
                if(node.left.type != "num"): 
                    node.left = solve(node.left, sub)
                if(node.right.type != "num"):
                    node.right = solve(node.right, sub)
            elif (node.type == "lambda"):
                if(node.var in sub[1].free_vars):
                    node = Solver.alpha(node, node.var + "'")
                    node.left = solve(node.left, sub)
                else:
                    node.left = solve(node.left, sub)
            
            return node

        node = solve(node, sub)
        Solver.free_vars(node)
        return save 

    @staticmethod
    def beta_reduction(node: Node, flag: bool):
        def solve(node: Node):
            if(node.type == "apply" and node.left.type == "lambda"):
                node.left = solve(node.left)
                # print(f"Before: {Solver.tree_to_string(node)}")
                node = Solver.substitue(copy.deepcopy(node.left), [copy.deepcopy(node.left.var), copy.deepcopy(node.right)]).left
                # print(f"After: {Solver.tree_to_string(node)}")
                return node
            elif(node.type == "lambda"):
                node.left = solve(node.left)
                return node
            elif(node.type == "oper"):
                node.left = solve(node.left)
                node.right = solve(node.right)
                if node.left.type == "num" and node.right.type =="num":
                    if node.op == '+':
                        sumthis = node.left.val + node.right.val
                        node = Node()
                        node.type = 'num'
                        node.val = sumthis
                        return node
                    elif node.op == '-':
                        subthis = node.left.val - node.right.val
                        node = Node()
                        node.type = 'num'
                        node.val = subthis
                        return node
                    elif node.op == '*':
                        multiply = node.left.val * node.right.val
                        node = Node()
                        node.type = 'num'
                        node.val = multiply
                        return node 
                    elif node.op == '/':
                        if node.right.val == 0.0:
                            raise Exception('Arithmetic Error')
                        else:
                            div = float(node.left.val // node.right.val)
                            node = Node()
                            node.type = 'num'
                            node.val = div
                        return node
                return node
            elif(node.type == "apply"):
                node.left = solve(node.left)
                # node.right = solve(node.right)
                return node
            return node
        
        prev = Solver.tree_to_string(node)
        if flag:
            print(f"INITIAL> {prev}")
        node = solve(node)
        cur = Solver.tree_to_string(node)
        while(not cur.__eq__(prev)):
            prev = cur
            if flag:
                print(f"BETA> {cur}")
            node = solve(node)
            cur = Solver.tree_to_string(node)

        return node
        
# --------------------------------------------------------------------------------------------