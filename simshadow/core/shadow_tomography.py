"""
Classical Shadow Tomography implementation for quantum state characterisation.

Based on Huang et al. "Predicting Many Properties of a Quantum System from Very Few Measurements"
"""

import numpy as np
from typing import List, Dict, Callable, Optional, Tuple
from abc import ABC, abstractmethod


class QuantumState:
    """Represents a quantum state for shadow tomography."""
    def __init__(self, state_vector: np.ndarray, name: str):
        # Add some checks here to avoid memory corruption.
        # If any of these happen, you need to use the explicit methods
        # Like this: state = QuantumState.computational_basis_state("00")
        if not isinstance(state_vector, np.ndarray):
            raise TypeError(
                "QuantumState must be constructed from a NumPy state vector"
                "Use computational_basis_state() or superposition_state()"
            )

        if not name:
            raise ValueError(
                "QuantumState.name must be provided. "
                "Use computational_basis_state() or superposition_state()"
            )

        if state_vector.ndim != 1:
            raise ValueError("state_vector must be a 1D array")

        dim = len(state_vector)
        if dim == 0 or (dim & (dim - 1)) != 0:
            raise ValueError("Length of state_vector must be a power of 2")

        self.state_vector = state_vector
        self.name = name
        self.n_qubits = int(np.log2(len(state_vector)))

    def to_string(self) -> str:
        return (
            f"QuantumState(name={self.name!r}, "
            f"n_qubits={self.n_qubits}, "
            f"state_vector={self.state_vector})"
        )
    
    @classmethod 
    def computational_basis_state(cls, bitstring: str) -> 'QuantumState':
        """Create computational basis state |bitstring>."""
        n_qubits = len(bitstring)
        state_vector = np.zeros(2**n_qubits, dtype=complex)
        state_vector[int(bitstring, 2)] = 1.0
        return cls(state_vector, f"|{bitstring}>")
    
    @classmethod
    def superposition_state(cls, qubit_states: List[str]) -> 'QuantumState':
        """Create superposition state like |+0>, |-0>, etc."""
        n_qubits = len(qubit_states)
        state_vector = np.ones(2**n_qubits, dtype=complex)
        
        for i, qubit_state in enumerate(qubit_states):
            if qubit_state == '+':
                # |+> = (|0> + |1>)/sqrt(2) 
                continue
            elif qubit_state == '-':
                # |-> = (|0> - |1>)/sqrt(2)
                for j in range(2**n_qubits):
                    if (j >> (n_qubits - 1 - i)) & 1:
                        state_vector[j] *= -1
            elif qubit_state == '0':
                # Project onto |0>
                for j in range(2**n_qubits):
                    if (j >> (n_qubits - 1 - i)) & 1:
                        state_vector[j] = 0
            elif qubit_state == '1':
                # Project onto |1>
                for j in range(2**n_qubits):
                    if not ((j >> (n_qubits - 1 - i)) & 1):
                        state_vector[j] = 0
        
        # Normalise
        norm = np.linalg.norm(state_vector)
        if norm > 0:
            state_vector /= norm
            
        name = f"|{''.join(qubit_states)}>"
        return cls(state_vector, name)
    
    @classmethod
    def ghz_state(cls, n_qubits: int) -> 'QuantumState':
        """
        Create GHZ state (|00...0> + |11...1>)/sqrt(2).
        
        Note: For n_qubits=2, this is actually the |Φ⁺⟩ Bell state, not a GHZ state.
        GHZ states require 3 or more qubits.
        """
        state_vector = np.zeros(2**n_qubits, dtype=complex)
        state_vector[0] = 1/np.sqrt(2)  # |00...0>
        state_vector[-1] = 1/np.sqrt(2)  # |11...1>
        if n_qubits == 2:
            # For 2 qubits, this is the |Φ⁺⟩ Bell state
            return cls(state_vector, "|Φ⁺>")
        else:
            # For 3+ qubits, this is a proper GHZ state
            return cls(state_vector, f"|GHZ_{n_qubits}>")


class PauliObservable:
    """Represents a Pauli observable for measurement."""
    
    def __init__(self, pauli_string: str):
        self.pauli_string = pauli_string
        self.n_qubits = len(pauli_string)
        self._matrix = self._construct_matrix()
    
    def _construct_matrix(self) -> np.ndarray:
        """Construct the matrix representation of the Pauli observable."""
        # Pauli matrices
        I = np.array([[1, 0], [0, 1]], dtype=complex)
        X = np.array([[0, 1], [1, 0]], dtype=complex)
        Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        Z = np.array([[1, 0], [0, -1]], dtype=complex)
        
        pauli_map = {'I': I, 'X': X, 'Y': Y, 'Z': Z}
        
        matrix = np.array([[1]], dtype=complex)
        for pauli in self.pauli_string:
            matrix = np.kron(matrix, pauli_map[pauli])
        
        return matrix
    
    def expectation_value(self, state: QuantumState) -> float:
        """Compute expectation value <psi|O|psi>."""
        psi = state.state_vector
        return np.real(np.conj(psi).T @ self._matrix @ psi)


class ClassicalShadowTomography:
    """
    Implements classical shadow tomography for efficient quantum state characterisation.
    
    Based on the methodology described in the SimSHADOW paper for quantum simulator validation.
    """
    
    def __init__(self, n_qubits: int, precision_target: float = 0.003):
        self.n_qubits = n_qubits
        self.precision_target = precision_target
        self.shadows = []
        self.measurement_records = []
    
    def collect_shadows(self, 
                       quantum_state: QuantumState,
                       simulator_backend,
                       n_measurements: int = 1000) -> List[Dict]:
        """
        Collect classical shadows from quantum state measurements.
        
        Args:
            quantum_state: The quantum state to measure
            simulator_backend: Platform-specific simulator backend
            n_measurements: Number of measurement shots
            
        Returns:
            List of shadow snapshots
        """
        shadows = []
        
        for _ in range(n_measurements):
            # Generate random local Pauli measurement bases (X/Y/Z per qubit)
            random_pauli = self._generate_random_pauli()
            
            # Perform measurement using simulator backend
            measurement_outcome = simulator_backend.measure_pauli(
                quantum_state, random_pauli
            )
            
            # Create classical shadow snapshot
            shadow = self._create_shadow_snapshot(random_pauli, measurement_outcome)
            shadows.append(shadow)
        
        self.shadows.extend(shadows)
        return shadows
    
    def _generate_random_pauli(self) -> str:
        """Generate random Pauli string for measurement."""
        paulis = ['X', 'Y', 'Z']
        return ''.join(np.random.choice(paulis) for _ in range(self.n_qubits))
    
    def _create_shadow_snapshot(self, pauli_string: str, outcome: str) -> Dict:
        """Create a classical shadow snapshot from measurement."""
        return {
            'pauli_string': pauli_string,   # per-qubit measurement bases
            'outcome': outcome,             # bitstring of measured bits (qubit 0 .. n-1)
            'timestamp': np.random.random() # lightweight provenance
        }
    
    def estimate_expectation_value(self, 
                                 observable: PauliObservable,
                                 shadows: Optional[List[Dict]] = None) -> Tuple[float, float]:
        """
        Estimate the expectation value of an observable using classical shadows.
        Uses the unbiased Pauli measurement estimator with median-of-means aggregation.
        
        Args:
            observable: The Pauli observable to estimate
            shadows: Shadow snapshots to use (defaults to collected shadows)
            
        Returns:
            Tuple of (expectation_value, standard_error)
        """
        if shadows is None:
            shadows = self.shadows
        
        if not shadows:
            raise ValueError("No shadows available for estimation")
        
        # Per-shot unbiased estimators
        per_shot_estimates: List[float] = []
        
        for shadow in shadows:
            estimate = self._compute_shadow_estimate(shadow, observable)
            # Shots that cannot contribute (basis mismatch) return 0 by construction
            per_shot_estimates.append(estimate)
        
        estimates = np.asarray(per_shot_estimates, dtype=float)
        
        # Median-of-means: split into equal-size blocks, take mean per block, then median
        n = len(estimates)
        # Choose ~sqrt(n) blocks, but at least 3 and at most n
        n_blocks = max(3, int(np.sqrt(n)))
        n_blocks = min(n_blocks, n)
        block_size = n // n_blocks if n_blocks > 0 else n
        if block_size == 0:
            block_size = 1
            n_blocks = n
        
        block_means = []
        for i in range(n_blocks):
            start = i * block_size
            end = n if i == n_blocks - 1 else (i + 1) * block_size
            if start >= n:
                break
            block_means.append(float(np.mean(estimates[start:end])))
        block_means = np.asarray(block_means, dtype=float)
        
        expectation_value = float(np.median(block_means))
        # Standard error proxy: std of block means over sqrt(#blocks)
        if len(block_means) > 1:
            standard_error = float(np.std(block_means, ddof=1) / np.sqrt(len(block_means)))
        else:
            standard_error = 0.0
        
        return expectation_value, standard_error
    
    def _compute_shadow_estimate(self, shadow: Dict, observable: PauliObservable) -> float:
        """Compute the unbiased Pauli-shadow estimate for a specific observable.
        For local Pauli measurements (uniform over {X,Y,Z} per qubit), the unbiased
        single-shot estimator for a Pauli string observable is:
            prod_i f_i, where
              f_i = 1 if O_i == I,
                    3 * s_i if O_i in {X,Y,Z} and measured basis equals O_i,
                    0 otherwise,
        with s_i in {+1,-1} determined by the measured bit for qubit i.
        """
        outcome_bits = shadow['outcome']
        pauli_meas = shadow['pauli_string']
        pauli_obs = observable.pauli_string
        
        estimate = 1.0
        for i, (m_i, o_i) in enumerate(zip(pauli_meas, pauli_obs)):
            if o_i == 'I':
                # Identity contributes multiplicative 1
                continue
            if m_i != o_i:
                # If measurement basis doesn't match non-identity observable, factor is 0
                return 0.0
            # Convert measured bit to eigenvalue s_i in {+1,-1}
            bit_char = outcome_bits[i]
            s_i = 1.0 if bit_char == '0' else -1.0
            # Unbiased scaling for local Pauli ensemble
            estimate *= 3.0 * s_i
        
        return float(estimate)
    
    def adaptive_precision_targeting(self,
                                   observable: PauliObservable,
                                   quantum_state: QuantumState,
                                   simulator_backend,
                                   max_measurements: int = 10000) -> Tuple[float, float]:
        """
        Adaptively collect measurements until target precision is reached.
        
        Args:
            observable: Observable to estimate
            quantum_state: Quantum state to measure
            simulator_backend: Platform-specific simulator
            max_measurements: Maximum measurements to collect
            
        Returns:
            Tuple of (expectation_value, achieved_precision)

        Called:
            generate_fingerprint from fingerprint.py
        """
        measurements_per_batch = 100
        current_measurements = 0
        
        while current_measurements < max_measurements:
            # Collect a batch of shadows
            new_shadows = self.collect_shadows(
                quantum_state, simulator_backend, measurements_per_batch
            )
            current_measurements += measurements_per_batch
            
            # Estimate with current shadows
            expectation_value, standard_error = self.estimate_expectation_value(observable)
            
            # Check if target precision achieved
            if standard_error <= self.precision_target:
                return expectation_value, standard_error
        
        # Return best estimate if max measurements reached
        expectation_value, standard_error = self.estimate_expectation_value(observable)
        return expectation_value, standard_error


def create_test_states(n_qubits: int = 2) -> List[QuantumState]:
    """
    Create the test states used in SimSHADOW experiments.
    
    Based on the paper's experimental design:
    - 4 computational basis states
    - 4 superposition states  
    - 1 entangled state: |Φ⁺⟩ Bell state for n_qubits=2, GHZ state for n_qubits≥3
    """
    test_states = []
    
    if n_qubits == 2:
        # Computational basis states
        for bitstring in ['00', '01', '10', '11']:
            test_states.append(QuantumState.computational_basis_state(bitstring))
        
        # Superposition states
        superposition_patterns = ['+0', '-0', '0+', '0-']
        for pattern in superposition_patterns:
            test_states.append(QuantumState.superposition_state(list(pattern)))
        
        # Entangled state: For 2 qubits, this is the |Φ⁺⟩ Bell state
        # For 3+ qubits, this would be a GHZ state
        test_states.append(QuantumState.ghz_state(n_qubits))
    
    return test_states


def create_pauli_observables(n_qubits: int = 2) -> List[PauliObservable]:
    """
    Create the comprehensive set of Pauli observables for fingerprinting.
    
    Based on the paper: 36 two-qubit Pauli observables covering all combinations.
    """
    observables = []
    
    if n_qubits == 2:
        # Two-qubit Pauli observables
        two_qubit_paulis = ['XX', 'XY', 'XZ', 'YX', 'YY', 'YZ', 'ZX', 'ZY', 'ZZ']
        for pauli in two_qubit_paulis:
            observables.append(PauliObservable(pauli))
        
        # Single-qubit observables with identity
        single_qubit_paulis = ['XI', 'IX', 'YI', 'IY', 'ZI', 'IZ']
        for pauli in single_qubit_paulis:
            observables.append(PauliObservable(pauli))
    
    return observables 
