import random
import string

from optimus_dwave import run_dwave
from convertToH import problemToH
from optimus_parser import parse_optimization_model
from pyqubo import Binary


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

##Get string from webapp and store here
d = """
min 5*x + 8*y
subject to x + y == 1
    """
objective_function, constraints, variables = parse_optimization_model(d.strip())

H = problemToH(objective_function, constraints)

random_string_to_variable = {}
for v in variables:
    rs = randomString()
    objective_function = objective_function.subs(v, rs)
    random_string_to_variable[rs] = v

objective_function = str(objective_function)
for v, k in random_string_to_variable.items():
    objective_function = objective_function.replace(v, "Binary('%s')" % k)

print("objective_function", objective_function)
H = eval(objective_function)

res = run_dwave(H)

for i,(smpl, energy) in enumerate(res.data(['sample','energy'])):
    print(smpl, energy)
