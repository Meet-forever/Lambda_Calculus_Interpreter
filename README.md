# Lambda Calculus Interpreter
Project idea and instruction taken from: [PLC-Lambda-Calculus-Project](https://tinman.cs.gsu.edu/~raj/4330/sp22/honors-grad-project/)

<blockquote>"Lambda calculus (also written as λ-calculus) is a formal system in mathematical logic for expressing computation based on function abstraction and application using variable binding and substitution." -- Wikipedia </blockquote> 

This project converts the theoretical idea of lambda calculus into a programming language. The main aim of this program is to apply beta reductions on a lambda expression to reduce its form.  

## Optional Flags:
```
-steps (prints steps of solving)
-tree (prints AST)
Both can also be used together!
```

## Sample Run:
### Normal Mode
```bash
E:\lambda> python .\Lambda.py
LAMBDA> ((((lambda f (lambda x ((f x) f))) (lambda y (lambda g (g (* y y))))) 2) (lambda a a));
ANSWER>> 16.0
LAMBDA> exit;
```

### Steps Mode 
```bash
E:\lambda> python .\Lambda.py -steps
LAMBDA> ((((lambda f (lambda x ((f x) f))) (lambda y (lambda g (g (* y y))))) 2) (lambda a a));
INITIAL> ((((lambda f (lambda x ((f x) f))) (lambda y (lambda g (g (* y y))))) 2.0) (lambda a a))
BETA> (((lambda x (((lambda y (lambda g (g (* y y)))) x) (lambda y (lambda g (g (* y y)))))) 2.0) (lambda a 
a))
BETA> (((lambda g (g (* 2.0 2.0))) (lambda y (lambda g (g (* y y))))) (lambda a a))
BETA> (((lambda y (lambda g (g (* y y)))) (* 2.0 2.0)) (lambda a a))
BETA> ((lambda g (g (* (* 2.0 2.0) (* 2.0 2.0)))) (lambda a a))
BETA> ((lambda a a) (* (* 2.0 2.0) (* 2.0 2.0)))
BETA> (* (* 2.0 2.0) (* 2.0 2.0))
BETA> 16.0
ANSWER>> 16.0
LAMBDA> exit;
```


### AST Mode
```bash
E:\lambda> python .\Lambda.py -tree
LAMBDA> ((lambda x (* x x)) 4);
ANSWER>> {  
  Type: apply
  FreeVar: set()
  Left: {
          Type: lambda
          BoundVar: x
          FreeVar: set()
          Left: {
                  Type: oper
                  FreeVar: {'x'}
                  Operator: *
                  Left: {
                          Type: var
                          Var: x
                          FreeVar: {'x'}
                        }
                  Right: {
                          Type: var
                          Var: x
                          FreeVar: {'x'}
                        }
                }
        }
  Right: {
          Type: num
          Value: 4.0
        }
}
ANSWER>> 16.0
LAMBDA>exit;
```
