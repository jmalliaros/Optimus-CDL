from optimus_parser import parse_optimization_model
from sympy import *

def problemToH(obj, conlist):
    nc = len(conlist)
    Hlist = []
    for i in range(0,nc):
        Hlist.append((conlist[i][0]-conlist[i][2])**2)

    Hlist.append(obj)
    return sum(Hlist)
