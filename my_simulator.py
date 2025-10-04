#
# A Quantum Simulator with a Bit of Soul
# Written on a quiet Saturday afternoon in Salem.
#
# The whole idea here is to make the logic as clear as possible,
# as if we're explaining it to a friend. We'll favour readability
# over raw, blistering speed.
#

import math
import random

class QuantumComputer:
    """
    This is our imaginary quantum computer. It holds a register of qubits
    and lets us perform operations on them. Its 'brain' is a dictionary
    that maps each quantum state to its complex amplitude.
    """
    def __init__(self, num_qubits):
        """A good story starts at the beginning. Ours starts in the |0...0> state."""
        print(f"Powering on a new {num_qubits}-qubit quantum computer...")
        self.num_qubits = num_qubits
        
        # The heart of our computer: a dictionary holding the quantum state.
        # It's like a list of residents in a building, where each resident is a basis state
        # (e.g., '01') and their 'volume' is their amplitude.
        self.amplitudes = {}
        
        # We start with only one resident: the |00...0> state, with a volume of 1.
        initial_state = '0' * self.num_qubits
        self.amplitudes[initial_state] = complex(1.0, 0.0)

    def _get_amplitude(self, basis_state):
        """A helper to safely get an amplitude, returning 0 if a state isn't present."""
        return self.amplitudes.get(basis_state, complex(0.0, 0.0))

    def apply_gate(self, gate_matrix, target_qubit):
        """
        This is where the magic happens. We apply a gate to a single qubit.
        Instead of giant matrix multiplication, we'll think about it state by state.
        We calculate where the amplitude of each resident state 'leaks' to.
        """
        
        # We build a new dictionary for the next state of our universe.
        next_amplitudes = {}
        
        # We go through every state that currently has a non-zero amplitude.
        for basis_state, current_amp in self.amplitudes.items():
            
            # Figure out which bit we are focusing on.
            bit_to_change = int(basis_state[target_qubit])
            
            # The two rows of the gate matrix tell us what happens if the bit
            # is 0, and what happens if it's 1.
            for row_index in range(2):
                # Calculate the new amplitude contribution
                amp_contribution = gate_matrix[row_index][bit_to_change] * current_amp
                
                # If this contribution is basically zero, no need to store it.
                if abs(amp_contribution) < 1e-9:
                    continue

                # Figure out the new state this contribution belongs to.
                # It's the same as the old state, but with the target bit
                # potentially flipped to the value of our current row_index.
                state_list = list(basis_state)
                state_list[target_qubit] = str(row_index)
                new_basis_state = "".join(state_list)
                
                # Add our calculated amplitude to the new state's total amplitude.
                # This is like multiple waves interfering at the same point.
                current_total = next_amplitudes.get(new_basis_state, complex(0.0, 0.0))
                next_amplitudes[new_basis_state] = current_total + amp_contribution
                
        # The future is now the present.
        self.amplitudes = next_amplitudes

    def entangle_qubits(self, control_qubit, target_qubit):
        """
        This is our CNOT gate. It's a special, beautiful operation where
        one qubit's state dictates a change in another.
        """
        
        # We find all states where the control qubit is '1'.
        states_to_swap = []
        for basis_state in self.amplitudes.keys():
            if basis_state[control_qubit] == '1':
                # If the control is 1, we find its partner state where the target is flipped.
                state_list = list(basis_state)
                state_list[target_qubit] = '1' if state_list[target_qubit] == '0' else '0'
                partner_state = "".join(state_list)
                
                # We only need to register each pair once for swapping.
                if (partner_state, basis_state) not in states_to_swap:
                    states_to_swap.append((basis_state, partner_state))
        
        # Now, we perform the elegant swap of amplitudes for each pair.
        for state_a, state_b in states_to_swap:
            amp_a = self._get_amplitude(state_a)
            amp_b = self._get_amplitude(state_b)
            self.amplitudes[state_a] = amp_b
            self.amplitudes[state_b] = amp_a


    def read_state(self):
        """Let's peek at the quantum state without disturbing it."""
        print("\n--- Current Quantum State ---")
        if not self.amplitudes:
            print("The universe is empty.")
            return
            
        # We sort the states to make it look nice and orderly.
        sorted_states = sorted(self.amplitudes.items())
        
        for basis_state, amp in sorted_states:
            # We only care about things that might actually happen.
            probability = abs(amp)**2
            if probability > 1e-9:
                print(f"  State |{basis_state}> has amplitude {amp.real:.4f} + {amp.imag:.4f}i  (Prob: {probability:.2%})")
        print("--------------------------")

    def collapse_to_measurement(self):
        """
        The act of observation. The universe must choose a single state to exist in,
        based on the probabilities we've calculated.
        """
        rand = random.random()
        cumulative_prob = 0.0
        
        # We sort to ensure the outcome is deterministic for a given random number.
        sorted_states = sorted(self.amplitudes.items())

        for basis_state, amp in sorted_states:
            cumulative_prob += abs(amp)**2
            if rand < cumulative_prob:
                print(f"\n...Collapse! The universe has chosen state |{basis_state}>.")
                self.amplitudes = {basis_state: complex(1.0, 0.0)}
                return basis_state
        
        # Fallback in case of rounding errors
        return sorted_states[-1][0] if sorted_states else ""


# --- Let's define the tools we can use ---
Hadamard = [[1/math.sqrt(2), 1/math.sqrt(2)], [1/math.sqrt(2), -1/math.sqrt(2)]]
PauliX = [[0, 1], [1, 0]]


# ===================================================================
# --- Our Story: The Creation of an Entangled Pair ---
# ===================================================================
if __name__ == "__main__":
    
    # Act 1: Setting the Stage. We bring our computer to life with two qubits.
    my_computer = QuantumComputer(2)
    my_computer.read_state()
    
    # Act 2: The Twist. We put the first qubit into a superposition of worlds.
    print("\nApplying a Hadamard to the first qubit (qubit 0)...")
    my_computer.apply_gate(Hadamard, 0)
    my_computer.read_state()

    # Act 3: The Connection. We link the fate of the second qubit to the first.
    print("\nEntangling qubit 1 with qubit 0...")
    my_computer.entangle_qubits(control_qubit=0, target_qubit=1)
    my_computer.read_state()
    
    # The Final Scene: Observation. We look at the qubits and see what story they tell.
    final_outcome = my_computer.collapse_to_measurement()
    my_computer.read_state()