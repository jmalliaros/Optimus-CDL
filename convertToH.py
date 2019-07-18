from sympy import *

x,y = symbols('x y')
obj = 2*x + y
conlist = [[x+2*y,3],[x+y,1]]

def problemToH(obj, conlist):
    nc = len(conlist)
    Hlist = []
    for i in range(0,nc):
        Hlist.append((conlist[i][0]-conlist[i][1])**2)

    Hlist.append(obj)
    return sum(Hlist)

print(problemToH(obj,conlist))
