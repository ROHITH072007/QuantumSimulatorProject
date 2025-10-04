Project Goal:
>>>This project is an implementation of a statevector-based quantum simulator in Python. The primary objective was to build the simulation engine from the ground up, using only standard Python libraries, to demonstrate a foundational understanding of the underlying quantum mechanical principles and linear algebra.

Design and Thought Process:
>>>The design of the simulator is centered around a few key decisions to adhere to the project's constraints while maintaining clarity.

Core Data Structures:
>>>Statevector Representation: The quantum statevector for an N-qubit system is represented as a flat Python list of 2^N complex numbers. The mapping from a computational basis state to a list index is done via its integer representation. For example, the amplitude for the basis state ∣101⟩ (binary for 5) is stored at statevector[5]. The system is always initialized to the ∣0…0⟩ state, represented by a 1.0 at index 0.

Gate Representation: 
>>>Quantum gates are represented as matrices using a list of lists of complex numbers.

Gate Application Logic:
>>>Single-Qubit Gates: The central challenge is applying a 2×2 gate matrix to a single qubit within a larger 2^N dimensional statevector. The chosen approach was to "promote" the single-qubit gate to a full 2^N×2^N unitary operator that acts on the entire system. This is achieved by constructing an operator using the tensor product.

>>>CNOT Gate Optimization: Instead of building the full 2^N×2^N matrix for the CNOT gate, a more computationally efficient method was implemented. The cx method operates directly on the statevector list. It iterates through the basis states, and for each state where the control qubit is ∣1⟩, it swaps the amplitudes with its corresponding partner state where the target qubit has been flipped.
      

Features:
The simulator's QuantumCircuit class exposes the following core functionalities:
Initialization of an N-qubit register to the ∣0…0⟩ state.
Application of arbitrary single-qubit gates to any target qubit.
Application of a CNOT gate between any control and target qubit.
Inspection of the final statevector's non-zero amplitudes.
Probabilistic measurement of the entire system, resulting in a state collapse.

How to Run
Prerequisites:

Python 3

Execution:
Save the code as my_simulator.py and run the following command in your terminal from the same directory:
"python my_simulator.py"


Example: Creating a Bell State
The following code snippet from the main execution block shows how to use the simulator to create an entangled Bell state.

if __name__ == "__main__":
    # Create a 2-qubit circuit
    my_circuit = QuantumCircuit(2)
    
    # Apply a Hadamard gate to the first qubit
    my_circuit.apply_gate(H, 0)
    
    # Apply a CNOT gate controlled by the first qubit
    my_circuit.cx(0, 1)
    
    # View the final entangled state
    my_circuit.view()
    
    # Measure the system
    result = my_circuit.measure()


Expected Result for my_simulator.py
When you run the command python my_simulator.py in your terminal, the output will be printed directly to the terminal window. It should look exactly like this:

--- Let's build a Bell State with our simulator ---
Initial State:
Current Statevector:
  |00> : 1.0000

Applying Hadamard gate to qubit 0...
Current Statevector:
  |00> : 0.7071
  |10> : 0.7071

Applying CNOT(0, 1)...
Final Statevector (The Bell State):
Current Statevector:
  |00> : 0.7071
  |11> : 0.7071

Measuring the system...
Result of measurement: |00>
Statevector after collapse:
Current Statevector:
  |00> : 1.0000

A Note on the Final Measurement:
The final line, Result of measurement:, is the most interesting part. Because a Bell state is a perfect 50/50 superposition of ∣00⟩ and ∣11⟩, the outcome of the measurement is completely random.

About 50% of the time you run the script, the result will be |00>.

The other 50% of the time, the result will be |11>.

Both outcomes are correct! This randomness is a real feature of quantum mechanics, and it proves that your simulator has successfully captured it.