"""
Cirq platform implementation for SimSHADOW quantum simulator validation.

Provides Cirq-specific quantum circuit execution and noise model integration.
"""
from typing import Dict, Optional

import cirq
import numpy as np
from cirq import DensityMatrixSimulator
from cirq.circuits import InsertStrategy

from simshadow.core.noise_models import NoiseChannel, DepolarizingChannel, AmplitudeDampingChannel, PhaseDampingChannel
from simshadow.core.shadow_tomography import QuantumState, PauliObservable


class CirqPlatform:
    """
    Cirq simulator platform for SimSHADOW experiments.
    Handles circuit construction, noise model configuration, and measurement execution
    specifically for Cirq-based simulations.
    """
    
    def __init__(self, n_qubits: int = 2):
        self.platform_name = "Cirq"
        self.n_qubits = n_qubits
        self.qubits = cirq.LineQubit.range(n_qubits)
        self.simulator = DensityMatrixSimulator()  # Use density matrix for noise
        self.noise_config: Optional[Dict] = None
        self.current_noise_channel: Optional[NoiseChannel] = None
        
    def configure_noise(self, noise_channel: NoiseChannel):
        """
        Configure Cirq noise model based on SimSHADOW noise channel.
        Called from run_simshadow.py
        """
        self.current_noise_channel = noise_channel
        self.noise_config = {
            'type': noise_channel.name,
            'parameter': noise_channel.parameter
        }
    
    def _add_noise_to_circuit(self, circuit: cirq.Circuit) -> cirq.Circuit:
        """
        Add noise to circuit based on current noise configuration.
        Interal function only
        """
        if self.current_noise_channel is None:
            return circuit
        
        noisy_circuit = cirq.Circuit()
        
        for moment in circuit:
            # Add the original operations
            noisy_circuit.append(moment, strategy=InsertStrategy.NEW_THEN_INLINE)
            
            # Add noise after each gate
            for operation in moment:
                if isinstance(self.current_noise_channel, DepolarizingChannel):
                    # Add depolarizing noise to each qubit involved
                    for qubit in operation.qubits:
                        noise_op = cirq.depolarize(p=self.current_noise_channel.p).on(qubit)
                        noisy_circuit.append(noise_op, strategy=InsertStrategy.INLINE)
                        
                elif isinstance(self.current_noise_channel, AmplitudeDampingChannel):
                    # Add amplitude damping noise
                    for qubit in operation.qubits:
                        noise_op = cirq.amplitude_damp(gamma=self.current_noise_channel.gamma).on(qubit)
                        noisy_circuit.append(noise_op, strategy=InsertStrategy.INLINE)
                        
                elif isinstance(self.current_noise_channel, PhaseDampingChannel):
                    # Add phase damping noise
                    for qubit in operation.qubits:
                        noise_op = cirq.phase_damp(gamma=self.current_noise_channel.lambda_param).on(qubit)
                        noisy_circuit.append(noise_op, strategy=InsertStrategy.INLINE)
                else:
                    raise ValueError(
                        "NoiseModel.name must be valid. ",
                        "Use DepolarizingChannel, AmplitudeDampingChannel, or PhaseDampingChannel"
                    )
        
        return noisy_circuit
    
    def prepare_state_circuit(self, quantum_state: QuantumState) -> QuantumCircuit:
        """
        Create a Qiskit circuit to prepare the specified quantum state.
        Internal function only.
        """
        # Here we will store the state!
        circuit = cirq.Circuit()

        if "GHZ" in quantum_state.name or "Φ" in quantum_state.name:
            # GHZ state preparation
            circuit.append(cirq.H(self.qubits[0]))
            for i in range(1, self.n_qubits):
                circuit.append(cirq.CNOT(self.qubits[0], self.qubits[i]))
        else: # We only have 0,1,+ and -

            # Explicitly keep only valid single-qubit symbols
            bitstring = [ch for ch in quantum_state.name if ch in {'0', '1', '+', '-'}]
            if len(bitstring) != self.n_qubits:
                raise ValueError(
                    f"State {quantum_state.name} does not match n_qubits={self.n_qubits}"
                )

            for i, ch in enumerate(bitstring):
                if ch == '0': 
                    pass
                elif ch == '1':
                    circuit.append(cirq.X(self.qubits[i]))
                elif ch == '+':
                    circuit.append(cirq.H(self.qubits[i]))
                elif ch == '-':
                    circuit.append([cirq.H(self.qubits[i]), cirq.Z(self.qubits[i])])
                else:
                    raise ValueError(
                        "QuantumState.name must be valid. "
                        "Use 0, 1, +, - or GHZ only."
                    )
        return circuit
    
    def measure_pauli(self, quantum_state: QuantumState, pauli_string: str) -> str:
        """
        Measure quantum state in specified Pauli basis and return outcome.
        
        Args:
            quantum_state: The quantum state to measure
            pauli_string: Pauli string like 'XY', 'ZZ', etc.
            
        Returns:
            Measurement outcome as bitstring

        Called:
            measure_pauli from shadow_tomography.py
        """
        # Prepare initial state
        circuit = self.prepare_state_circuit(quantum_state)
        
        # Add Pauli basis rotations
        for i, pauli in enumerate(pauli_string):
            if pauli == 'X':
                circuit.append(cirq.ry(-np.pi/2)(self.qubits[i]))
            elif pauli == 'Y':
                circuit.append(cirq.rx(np.pi/2)(self.qubits[i]))
            # Leave this to the full paper, with a proper theorem.    
            #elif pauli == 'I' or pauli == 'Z':
            #    circuit.append(cirq.I(self.qubits[i]))
            # Z measurement is in computational basis (no rotation needed)
        
        # Add noise if configured
        if self.current_noise_channel:
            circuit = self._add_noise_to_circuit(circuit)
        
        # Add measurements
        for i in range(self.n_qubits):
            circuit.append(cirq.measure(self.qubits[i], key=f'q{i}'))
        
        # Execute circuit
        result = self.simulator.run(circuit, repetitions=1)
        
        # Extract measurement outcome
        outcome_bits = []
        for i in range(self.n_qubits):
            outcome_bits.append(str(result.measurements[f'q{i}'][0][0]))
        #print(outcome_bits)

        return ''.join(outcome_bits)
    
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

        Called:
            main from run_simshadow.py
        """
        # Prepare state circuit
        circuit = self.prepare_state_circuit(quantum_state)
        
        # Add Pauli basis rotations for measurement
        for i, pauli in enumerate(observable.pauli_string):
            if pauli == 'X':
                circuit.append(cirq.ry(-np.pi/2)(self.qubits[i]))
            elif pauli == 'Y':
                circuit.append(cirq.rx(np.pi/2)(self.qubits[i]))
            # Leave this to the full paper, with a proper theorem.     
            #elif pauli == 'I' or pauli == 'Z':
            #    circuit.append(cirq.I(self.qubits[i]))

        # Add noise if configured
        if self.current_noise_channel:
            circuit = self._add_noise_to_circuit(circuit)
        
        # Add measurements
        for i in range(self.n_qubits):
            circuit.append(cirq.measure(self.qubits[i], key=f'q{i}'))

        # Execute circuit with multiple shots
        result = self.simulator.run(circuit, repetitions=shots)
        
        # Compute expectation value from measurement statistics
        # For Pauli observables, eigenvalue is product of individual qubit eigenvalues
        # After rotating to measurement basis: |0⟩ → +1, |1⟩ → -1
        # For identity (I): eigenvalue is always +1
        expectation = 0.0
        for shot in range(shots):
            # Get measurement outcome for this shot
            outcome_bits = []
            for i in range(self.n_qubits):
                outcome_bits.append(result.measurements[f'q{i}'][shot][0])
            
            # Compute eigenvalue as product of individual qubit eigenvalues
            eigenvalue = 1.0
            for i, pauli in enumerate(observable.pauli_string):
                if pauli == 'I':
                    # Identity always has eigenvalue +1
                    continue
                else:
                    # After rotation to Pauli basis, |0⟩ → +1, |1⟩ → -1
                    bit = outcome_bits[i]
                    qubit_eigenvalue = 1.0 if bit == 0 else -1.0
                    eigenvalue *= qubit_eigenvalue
            
            expectation += eigenvalue / shots
        
        return expectation

    ## WORKING VERSION OF IDEAL
    def get_ideal_expectation(self, quantum_state: QuantumState, 
                              observable: PauliObservable,
                              shots: int = 10000) -> float:
        """Get ideal (noiseless) expectation value."""
        # Temporarily disable noise
        original_channel = self.current_noise_channel
        self.current_noise_channel = None
        
        expectation = self.compute_expectation_value(quantum_state, observable, shots)
        
        # Restore noise configuration
        self.current_noise_channel = original_channel
        
        return expectation
