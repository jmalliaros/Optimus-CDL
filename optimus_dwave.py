import dimod
import minorminer
from dwave.system import DWaveSampler
from dwave.system.composites import AutoEmbeddingComposite, FixedEmbeddingComposite
from pyqubo import Binary
import matplotlib.pyplot as plt
import sys

dwaveSampler = DWaveSampler()
dimodSampler = dimod.ExactSolver()


## EXAMPLE Problem -> Replace with general form
binArr = []
index = 0
for i in range(0,5):
        binArr.append(Binary('s'+str(i+1)))
s1,s2,s3,s4,s5 = binArr[0], binArr[1], binArr[2], binArr[3], binArr[4]
H = (s1+2*s2+3*s3+4*s4+5*s5-8*3)**2 + (s1+s2+s3+s4+s5-3*3)**2

def get_embedding_with_short_chain(J: dict, tries: int = 5,
                                   processor: list = None, verbose=False)->dict:
    '''Try a few probabilistic embeddings and return the one with the shortest
    chain length

    :param J: Couplings
    :param tries: Number of probabilistic embeddings
    :param verbose: Whether to print out diagnostic information

    :return: Returns the minor embedding
    '''
    if processor is None:
        # The hardware topology: 16 by 16 pieces of K_4,4 unit cells
        processor = dnx.chimera_graph(16, 16, 4).edges()
    # Try a few embeddings
    best_chain_length = sys.maxsize
    source = list(J.keys())
    for _ in range(tries):
        try:
            emb = minorminer.find_embedding(source, processor)
            #chain_length = max_chain_length(emb)
            chain_length = max(len(chain) for chain in emb.values())
            if chain_length > 0 and chain_length < best_chain_length:
                embedding = emb
                best_chain_length = chain_length
        except ValueError:
            pass
    if verbose:
        print(best_chain_length, max_chain_length(embedding))
    if best_chain_length == sys.maxsize:
        raise Exception("Cannot find embedding")
    return embedding

from XanaduCutOffComposite import CutOffComposite
from XanaduCutOffComposite import XanaduCutOffComposite

def run_dwave(H, sampler = dwaveSampler, solve_parameters=None):
    '''Runs QUBO from a given H, on the spesified sampler.

    :param H: Hamiltoninan
    :param sampler: DWaveSampler() or dimod.ExactSolver() object

    :return: Returns the sample data for the problem
    '''
    model = H.compile()
    qubo,offset = model.to_qubo()
    print("solve_parameters", solve_parameters)
    if "prune" in solve_parameters:
        pruner = solve_parameters["prune"]
        print(str(pruner), "dsandaskjdasn")
        if "dwave" in str(pruner):
            print("WORKINGdwavedsakmadksm")
            quantumSample = CutOffComposite(AutoEmbeddingComposite(sampler), 0.75)

        if "xanadu" in str(pruner):
            print("Xanadu!!!!!!!!!!!")
            quantumSample = XanaduCutOffComposite(AutoEmbeddingComposite(sampler), 0.75)
    else:
        embedding = get_embedding_with_short_chain(J=qubo, processor=dwaveSampler.edgelist)
        quantumSample = FixedEmbeddingComposite(sampler, embedding)

    results = quantumSample.sample_qubo(qubo,annealing_time=20,num_reads=1000)

    try:
        new_qubo = quantumSample.new_qubo
    except AttributeError:
        new_qubo = None

    return results, new_qubo, model.to_dimod_bqm()
