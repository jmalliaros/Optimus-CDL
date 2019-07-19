import random
import string

from dwave.system import CutOffComposite
from optimus_dwave import run_dwave
from optimus_ibm import run_IBM
from optimus_rigetti import run_Rigetti
from convertToH import problemToH
from optimus_parser import parse_optimization_model
from pyqubo import Binary


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def route(input_string):
	##Get string from webapp and store here
	d = input_string
	objective_function, constraints, variables, solve_parameters = parse_optimization_model(d.strip())

	print("solve_parameters2", solve_parameters)

	H = problemToH(objective_function, constraints)

	# random_string_to_variable = {}
	# for v in variables:
	#     rs = randomString()
	#     objective_function = objective_function.subs(v, rs)
	#     random_string_to_variable[rs] = v

	# objective_function = str(objective_function)
	# for v, k in random_string_to_variable.items():
	#     objective_function = objective_function.replace(v, "Binary('%s')" % k)

	# print("objective_function", objective_function)
	# H = eval(objective_function)

	try:
		run_on = solve_parameters["run_on"]
		run_on = list(map(lambda a: a.label, run_on))
	except KeyError:
		run_on = ["dwave"]

	print("run_on", run_on)

	res, qubo, old_qubo = run_dwave(H, solve_parameters=solve_parameters)
	if "dwave" not in run_on:
		res = None

	qubo_to_use = old_qubo
	print("res, qubo, old_qubo", res, qubo, old_qubo)	

	if qubo:
		qubo_to_use = qubo

	if "ibm" in run_on:
		res_ibm = run_IBM(qubo_to_use, variables=variables.keys())
	else:
		res_ibm = None

	if "rigetti" in run_on:
		res_rig = run_Rigetti(qubo_to_use, variables=variables.keys())
	else:
		res_rig = None


	shots = []
	# for i,(smpl, energy) in enumerate(res.data(['sample','energy'])):
	#     shots.append([smpl, energy])

	return res, shots, qubo, old_qubo, res_ibm, res_rig
