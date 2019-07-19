import numpy as np
from qiskit import BasicAer, ClassicalRegister, QuantumRegister, QuantumCircuit, execute
from qiskit.aqua import Operator, run_algorithm
from qiskit.aqua.algorithms import QAOA
from qiskit.aqua.components.optimizers import SPSA
from qiskit.aqua import QuantumInstance
from qiskit.quantum_info import Pauli
from qiskit.aqua.components.variational_forms import RY
from qiskit.visualization import *
from pyqubo import Binary

## EXAMPLE Problem -> Replace with general form
# binArr = []
# variable = []
# index = 0
# for i in range(0,2):
#     binArr.append(Binary('s'+str(i+1)))
#     variable.append('s' + str(i+1))
# print(variable)
# s1,s2 = binArr[0], binArr[1]
# H = (s1+s2-1)**2 + s1

def get_ising_opt_qubitops(model, variables):

    num_variables = len(variables)
    var_to_int = dict(zip(variables, range(num_variables)))

    linear, quadratic, offset = model.to_ising()

    pauli_list = []
    xs = np.zeros(num_variables, dtype=np.bool)
    for (i,j),weight in quadratic.items():
        zs = np.zeros(num_variables, dtype=np.bool)
        zs[var_to_int[i]] = True
        zs[var_to_int[j]] = True
        pauli_list.append([weight, Pauli(zs, xs)])

    for (i,weight) in linear.items():
        zs = np.zeros(num_variables, dtype=np.bool)
        zs[var_to_int[i]] = True
        pauli_list.append([weight, Pauli(zs, xs)])

    return Operator(paulis=pauli_list), offset

def run_IBM(H=None, backend = None, num_samples=100,qaoa_steps=20, variables=None):

    num_vars = len(variables)

    qubit_op, offset = get_ising_opt_qubitops(H,variables)

    if backend == None:
        backend = BasicAer.get_backend('qasm_simulator')
    quantum_instance = QuantumInstance(backend)

    spsa = SPSA(max_trials=30)
    qaoa = QAOA(qubit_op, spsa, qaoa_steps)
    result = qaoa.run(quantum_instance)

    circ = qaoa.get_optimal_circuit()
    q = circ.qregs[0]
    c = ClassicalRegister(num_vars, 'c')
    circ.cregs.append(c)
    circ.measure(q,c)

    job=execute(circ,backend,shots=num_samples, memory=True)

    return job.result().get_counts(circ)
