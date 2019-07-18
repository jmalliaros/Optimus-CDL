from optimus_parser import parse_optimization_model
from sympy import *

d = """
min 5*x + 8*y
subject to x + y == 1
    """
objective_function, constraints, variables = parse_optimization_model(d.strip())

obj = objective_function
conlist = constraints

def problemToH(obj, conlist):
    nc = len(conlist)
    Hlist = []
    for i in range(0,nc):
        Hlist.append((conlist[i][0]-conlist[i][2])**2)

    Hlist.append(obj)
    return sum(Hlist)

print(problemToH(obj,conlist))
