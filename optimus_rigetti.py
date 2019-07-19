import networkx as nx
import numpy as np
from pyquil.api import get_qc
from pyquil.paulis import PauliTerm, PauliSum
from scipy.optimize import minimize

from grove.pyqaoa.qaoa import QAOA

from pyqubo import Binary

# EXAMPLE Problem -> Replace with general form
binArr = []
variable = []
index = 0
for i in range(0,5):
    binArr.append(Binary('s'+str(i+1)))
    variable.append('s' + str(i+1))
s1,s2,s3,s4,s5 = binArr[0], binArr[1], binArr[2], binArr[3], binArr[4]
H = (s1+2*s2+3*s3+4*s4+5*s5-3*3)**2 + (s1+s2+s3+s4+s5-3)**2


def ising_qaoa(model, variables, steps=1, rand_seed=None, connection=None, samples=None,
               initial_beta=None, initial_gamma=None, minimizer_kwargs=None,
               vqe_option=None):
    """
    Max cut set up method
    :param model: a pyqubo model.  This will be the cost hamiltonian
    :param num_variables: the number of variables in the compiled model.  This might be computable from compiled_model
    :param steps: (Optional. Default=1) Trotterization order for the QAOA algorithm.
    :param rand_seed: (Optional. Default=None) random seed when beta and gamma angles
        are not provided.
    :param connection: (Optional) connection to the QVM. Default is None.
    :param samples: (Optional. Default=None) VQE option. Number of samples
        (circuit preparation and measurement) to use in operator averaging.
    :param initial_beta: (Optional. Default=None) Initial guess for beta parameters.
    :param initial_gamma: (Optional. Default=None) Initial guess for gamma parameters.
    :param minimizer_kwargs: (Optional. Default=None). Minimizer optional arguments.  If None set to
        ``{'method': 'Nelder-Mead', 'options': {'ftol': 1.0e-2, 'xtol': 1.0e-2, 'disp': False}``
    :param vqe_option: (Optional. Default=None). VQE optional arguments.  If None set to
        ``vqe_option = {'disp': print_fun, 'return_all': True, 'samples': samples}``
    """
    num_variables = len(variables)
    var_to_int = dict(zip(variables, range(num_variables)))

    compiled_model = model
    linear, quadratic, offset = compiled_model.to_ising()

    cost_operators = []
    driver_operators = []
    # We still need to figure out what the variables are encoded as.  I'd like to get out integer variables
    for (i, j), weight in quadratic.items():
        cost_operators.append(PauliSum([PauliTerm("Z", var_to_int[i], weight) * PauliTerm("Z", var_to_int[j])]))
    for i, weight in linear.items():
        cost_operators.append(PauliSum([PauliTerm("Z", var_to_int[i], weight)]))
    cost_operators.append(PauliSum([PauliTerm("I", 0, offset / 2)]))

    for i in range(num_variables):
        driver_operators.append(PauliSum([PauliTerm("X", i, -1.0)]))

    if connection is None:
        connection = get_qc(f"{num_variables}q-qvm")

    if minimizer_kwargs is None:
        minimizer_kwargs = {'method': 'Nelder-Mead',
                            'options': {'ftol': 1.0e-2, 'xtol': 1.0e-2,
                                        'disp': False}}
    if vqe_option is None:
        vqe_option = {'disp': print, 'return_all': True,
                      'samples': samples}

    ising_inst = QAOA(connection, list(range(num_variables)), steps=steps, cost_ham=cost_operators,
                      ref_ham=driver_operators, store_basis=True,
                      rand_seed=rand_seed,
                      init_betas=initial_beta,
                      init_gammas=initial_gamma,
                      minimizer=minimize,
                      minimizer_kwargs=minimizer_kwargs,
                      vqe_options=vqe_option)

    return ising_inst


def run_Rigetti(H=H, connection=None, num_samples=100, qaoa_steps=1):
    variables = variable  # We need to get something like H.variables()
    inst = ising_qaoa(H, variables, connection=connection, steps=qaoa_steps)

    betas, gammas = inst.get_angles()

    sampled_strings, frequency = inst.get_string(betas, gammas, samples=num_samples)

    return sampled_strings, frequency
