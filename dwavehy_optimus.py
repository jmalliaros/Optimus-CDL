import dimod
import hybrid
import minorminer
from dwave.system import DWaveSampler, FixedEmbeddingComposite
from pyqubo import Binary
import matplotlib.pyplot as plt
import sys

dwaveSampler = DWaveSampler()
dimodSampler = dimod.ExactSolver()

## EXAMPLE Problem -> Replace with general form
binArr = []
index = 0
for i in range(0,2):
        binArr.append(Binary('s'+str(i+1)))
s1,s2 = binArr[0], binArr[1]# binArr[2], binArr[3], binArr[4]
#H = (s1+2*s2+3*s3+4*s4+5*s5-8*3)**2 + (s1+s2+s3+s4+s5-3*3)**2
H = (s1 + s2 - 1)**2
# Construct a problem
model = H.compile()
bqm = model.to_dimod_bqm()

# Define the workflow
iteration = hybrid.RacingBranches(
    hybrid.Identity(),
    hybrid.InterruptableTabuSampler(),
    hybrid.EnergyImpactDecomposer(size=2)
    | hybrid.QPUSubproblemAutoEmbeddingSampler()
    | hybrid.SplatComposer()
) | hybrid.ArgMin()
workflow = hybrid.LoopUntilNoImprovement(iteration, convergence=10)

# Solve the problem
init_state = hybrid.State.from_problem(bqm)
final_state = workflow.run(init_state).result()

# Print results
print("Solution: sample={.samples.first}".format(final_state))
