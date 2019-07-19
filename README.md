# Optimus - Creative Destruction Labs Quantum Hackathon

A novel interactive console for quantum optimization.

We designed an interface for submitting binary optimization tasks for optimization through quantum devices.  Our console allows for the choice of processor including the DWave, Rigetti, and IBM devices.  Additionally, we allow an option for choosing a dense subgraph of the interaction graph through gaussian boson sampling on the Xanadu device.

Interaction with our console is done through a custom and straightforward modeling language, including options to choose the expected backend.  The console parses its given input, and outputs the corresponding list of interactions and variables.  From here, depending on the processor passed as an option, we perform the optimization on a qubo via the DWave machine or on a QAOA algorithm on the IBM or Rigetti machines.  Finally, the optimized state is sampled and the relative frequencies of the sampled strings are returned in a visual manner.

The Xanadu machine is used to simplify the underlying interactions, by trying to optimize an induced problem with variables whose interactions are dense.  This could give a nice starting point for futere optimizations on the same problem.
