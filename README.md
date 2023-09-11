<img src="https://user-images.githubusercontent.com/3848298/61548833-965d1680-aa1c-11e9-876e-a7335ec3a530.png"/>

# Optimus - Creative Destruction Lab Quantum Hackathon 

A novel interactive console for quantum optimization.

We designed an interface for submitting binary optimization tasks for optimization through quantum devices.  Our console allows for the choice of processor including the DWave, Rigetti, and IBM devices.  Additionally, we allow an option for choosing a dense subgraph of the interaction graph through gaussian boson sampling on the Xanadu device.

Interaction with our console is done through a custom and straightforward modeling language, including options to choose the expected backend.  The console parses its given input, and outputs the corresponding list of interactions and variables.  From here, depending on the processor passed as an option, we perform the optimization on a qubo via the DWave machine or on a QAOA algorithm on the IBM or Rigetti machines.  Finally, the optimized state is sampled and the relative frequencies of the sampled strings are returned in a visual manner.

The Xanadu machine is used to simplify the underlying interactions, by trying to optimize an induced problem with variables whose interactions are dense.  This could give a nice starting point for future optimizations on the same problem.

<a href="https://drive.google.com/uc?export=view&id=1OQ8iNH6bQEag8G8hJr_e60oPtQkVaCpR"><img src="https://drive.google.com/uc?export=view&id=1OQ8iNH6bQEag8G8hJr_e60oPtQkVaCpR" style="width: 650px; max-width: 100%; height: auto" />
