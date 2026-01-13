"""
Qiskit platform implementation for SimSHADOW quantum simulator validation.

Provides Qiskit-specific quantum circuit execution and noise model integration.
"""

import numpy as np
from typing import List, Dict, Optional
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, Operator, DensityMatrix
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, amplitude_damping_error, phase_damping_error
from qiskit.quantum_info import state_fidelity

from ..core.shadow_tomography import QuantumState, PauliObservable
from ..core.noise_models import NoiseChannel, DepolarizingChannel, AmplitudeDampingChannel, PhaseDampingChannel


class QiskitPlatform:
    """
    Qiskit simulator platform for SimSHADOW experiments.
    
    Handles circuit construction, noise model configuration, and measurement execution
    specifically for Qiskit-based simulations.
    """
    
    def __init__(self, n_qubits: int = 2):
        self.platform_name = "Qiskit"
        self.n_qubits = n_qubits
        self.simulator = AerSimulator()
        self.noise_model: Optional[NoiseModel] = None
        self.current_noise_config: Optional[Dict] = None
        
    def configure_noise(self, noise_channel: NoiseChannel):
        """Configure Qiskit noise model based on SimSHADOW noise channel."""
        self.current_noise_config = {
            'type': noise_channel.name,
            'parameter': noise_channel.parameter
        }
        
        # Create Qiskit noise model
        noise_model = NoiseModel()
        
        if isinstance(noise_channel, DepolarizingChannel):
            # Add depolarizing errors to all single and two-qubit gates
            error_1q = depolarizing_error(noise_channel.p, 1)
            error_2q = depolarizing_error(noise_channel.p, 2)
            
            # Apply to common gates
            noise_model.add_all_qubit_quantum_error(error_1q, ['u1', 'u2', 'u3', 'h', 'x', 'y', 'z'])
            noise_model.add_all_qubit_quantum_error(error_2q, ['cx', 'cy', 'cz'])
            
        elif isinstance(noise_channel, AmplitudeDampingChannel):
            # Add amplitude damping errors
            error_1q = amplitude_damping_error(noise_channel.gamma)
            
            # Apply to all single-qubit gates
            noise_model.add_all_qubit_quantum_error(error_1q, ['u1', 'u2', 'u3', 'h', 'x', 'y', 'z'])
            
        elif isinstance(noise_channel, PhaseDampingChannel):
            # Add phase damping errors
            error_1q = phase_damping_error(noise_channel.lambda_param)
            
            # Apply to all single-qubit gates
            noise_model.add_all_qubit_quantum_error(error_1q, ['u1', 'u2', 'u3', 'h', 'x', 'y', 'z'])
        
        self.noise_model = noise_model
    
    def prepare_state_circuit(self, quantum_state: QuantumState) -> QuantumCircuit:
        """Create Qiskit circuit to prepare the specified quantum state."""
        circuit = QuantumCircuit(self.n_qubits)
        
        # Initialize circuit to prepare the target state
        if quantum_state.name.startswith("|0") or quantum_state.name.startswith("|1"):
            # Computational basis states
            bitstring = quantum_state.name[1:-1]  # Remove |⟩
            for i, bit in enumerate(bitstring):
                if bit == '1':
                    circuit.x(i)
                    
        elif "+" in quantum_state.name or "-" in quantum_state.name:
            # Superposition states
            state_desc = quantum_state.name[1:-1]  # Remove |⟩
            for i, char in enumerate(state_desc):
                if char == '+':
                    circuit.h(i)
                elif char == '-':
                    circuit.h(i)
                    circuit.z(i)
                # '0' and '1' are handled above or left as |0⟩
                    
        elif "GHZ" in quantum_state.name:
            # GHZ state preparation
            circuit.h(0)
            for i in range(1, self.n_qubits):
                circuit.cx(0, i)
        
        return circuit
    
    def measure_pauli(self, quantum_state: QuantumState, pauli_string: str) -> str:
        """
        Measure quantum state in specified Pauli basis and return outcome.
        
        Args:
            quantum_state: The quantum state to measure
            pauli_string: Pauli string like 'XY', 'ZZ', etc.
            
        Returns:
            Measurement outcome as bitstring
        """
        # Prepare initial state
        circuit = self.prepare_state_circuit(quantum_state)
        
        # Add Pauli basis rotations
        for i, pauli in enumerate(pauli_string):
            if pauli == 'X':
                circuit.ry(-np.pi/2, i)  # Rotate Y by -π/2 to measure X
            elif pauli == 'Y':
                circuit.rx(np.pi/2, i)   # Rotate X by π/2 to measure Y
            # Z measurement is in computational basis (no rotation needed)
        
        # Add measurements  
        circuit.measure_all()
        
        # Execute circuit with noise
        if self.noise_model:
            job = self.simulator.run(
                transpile(circuit, self.simulator),
                shots=10000,
                noise_model=self.noise_model
            )
        else:
            job = self.simulator.run(
                transpile(circuit, self.simulator),
                shots=10000
            )
        
        result = job.result()
        counts = result.get_counts()
        
        # Return the measured bitstring (Qiskit returns counts dict)
        # Normalize bit order to little-endian qubit index order q0..q{n-1}
        raw = list(counts.keys())[0]
        outcome = raw[::-1]
        return outcome
    
    def compute_expectation_value(self, 
                                quantum_state: QuantumState, 
                                observable: PauliObservable,
                                shots: int = 10000) -> float:
        """
        Compute expectation value of Pauli observable with proper noise simulation.
        
        Args:
            quantum_state: The quantum state
            observable: Pauli observable to measure
            shots: Number of measurement shots
            
        Returns:
            Estimated expectation value
        """
        # Prepare state circuit
        circuit = self.prepare_state_circuit(quantum_state)
        
        # Add Pauli basis rotations for measurement
        for i, pauli in enumerate(observable.pauli_string):
            if pauli == 'X':
                circuit.ry(-np.pi/2, i)
            elif pauli == 'Y':
                circuit.rx(np.pi/2, i)
        
        # Add measurements
        circuit.measure_all()
        
        # Execute with noise model
        if self.noise_model:
            job = self.simulator.run(
                transpile(circuit, self.simulator),
                shots=shots,
                noise_model=self.noise_model
            )
        else:
            job = self.simulator.run(
                transpile(circuit, self.simulator),
                shots=shots
            )
        
        result = job.result()
        counts = result.get_counts()
        
        # Compute expectation value from measurement statistics
        # For Pauli observables, eigenvalue is product of individual qubit eigenvalues
        # After rotating to measurement basis: |0⟩ → +1, |1⟩ → -1
        # For identity (I): eigenvalue is always +1
        expectation = 0.0
        total_shots = sum(counts.values())
        
        for bitstring, count in counts.items():
            # Compute eigenvalue as product of individual qubit eigenvalues
            eigenvalue = 1.0
            for i, pauli in enumerate(observable.pauli_string):
                if pauli == 'I':
                    # Identity always has eigenvalue +1
                    continue
                else:
                    # After rotation to Pauli basis, |0⟩ → +1, |1⟩ → -1
                    bit = int(bitstring[i])
                    qubit_eigenvalue = 1.0 if bit == 0 else -1.0
                    eigenvalue *= qubit_eigenvalue
            
            expectation += eigenvalue * count / total_shots
        
        return expectation
    
    def get_ideal_expectation(self, quantum_state: QuantumState, 
                            observable: PauliObservable) -> float:
        """Get ideal (noiseless) expectation value."""
        # Temporarily disable noise
        original_noise = self.noise_model
        self.noise_model = None
        
        expectation = self.compute_expectation_value(quantum_state, observable, shots=10000)
        
        # Restore noise model
        self.noise_model = original_noise
        
        return expectation
    
    def validate_state_preparation(self, quantum_state: QuantumState) -> float:
        """Validate that state preparation circuit produces correct state."""
        # Create circuit without noise
        circuit = self.prepare_state_circuit(quantum_state)
        
        # Get statevector
        statevector_sim = AerSimulator(method='statevector')
        job = statevector_sim.run(transpile(circuit, statevector_sim))
        result = job.result()
        final_statevector = result.get_statevector()
        
        # Compute fidelity with target state
        target_sv = Statevector(quantum_state.state_vector)
        fidelity = state_fidelity(final_statevector, target_sv)
        
        return float(fidelity)
    
    def get_platform_info(self) -> Dict:
        """Get platform-specific information for debugging."""
        return {
            'platform': self.platform_name,
            'backend': 'AerSimulator',
            'noise_model_active': self.noise_model is not None,
            'current_noise_config': self.current_noise_config,
            'n_qubits': self.n_qubits
        } 
