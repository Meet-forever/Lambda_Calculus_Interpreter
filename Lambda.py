from LambdaParser import parser
from LambdaNode import Solver
import sys

exec = [0]
if len(sys.argv) > 1:
    if '-steps' in sys.argv:
        exec.append(1)
    if '-tree' in sys.argv:
        exec.append(2)


def read_input():
    result = ''
    while True:
        data = input('LAMBDA> ').strip()
        if ';' in data:
            i = data.index(';')
            result += data[0 : i+1]
            break
        else:
            result += data + ' '
    return result


def main():
    while True:
        data = read_input()
        if data == 'exit;':
            print("GoodBye!\n")
            break
        try:
            tree = parser.parse(data)
            if tree != None and 2 in exec:
                print(f"ANSWER>> {tree}")
            tree = Solver.solvethis(tree, exec)
        except Exception as inst:
            print(inst.args[0])
            continue

main()