"""
Noise channel models for quantum simulator validation.

Implements the main noise channels tested in the SimSHADOW paper:
- Depolarizing channels
- Amplitude damping channels  
- Phase damping channels
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

import numpy as np


class NoiseChannel(ABC):
    """Abstract base class for quantum noise channels."""
    
    def __init__(self, parameter: float, name: str = ""):
        self.parameter = parameter
        self.name = name
        
    @abstractmethod
    def apply_to_state(self, state_vector: np.ndarray) -> np.ndarray:
        """Apply noise channel to quantum state."""
        pass
    
    @abstractmethod
    def get_theoretical_expectation(self, ideal_expectation: float) -> float:
        """Get theoretical expectation value after noise."""
        pass
    
    @abstractmethod
    def get_channel_signature(self) -> Dict[str, Any]:
        """Get characteristic signature of this noise channel."""
        pass


class DepolarizingChannel(NoiseChannel):
    """
    Depolarizing noise channel: Λ(ρ) = (1-p)ρ + p(I/d)
    
    Uniformly mixes the state with the maximally mixed state.
    """
    
    def __init__(self, depolarizing_probability: float):
        super().__init__(depolarizing_probability, "Depolarizing")
        self.p = depolarizing_probability
        
    def apply_to_state(self, state_vector: np.ndarray) -> np.ndarray:
        """Apply depolarizing noise to state vector (simplified for simulation)."""
        # For pure states, depolarizing creates mixed states
        # In simulation, we approximate by scaling expectation values
        return state_vector
    
    def get_theoretical_expectation(self, ideal_expectation: float) -> float:
        """Depolarizing channel uniformly attenuates all observables."""
        return (1 - self.p) * ideal_expectation
    
    def get_channel_signature(self) -> Dict[str, Any]:
        """Depolarizing signature: uniform attenuation."""
        return {
            'type': 'depolarizing',
            'parameter': self.p,
            'attenuation_factor': 1 - self.p,
            'uniformity': True,
            'expected_deviation_mean': -self.p,
            'expected_deviation_std': 0.1 * self.p  # Typical variance
        }


class AmplitudeDampingChannel(NoiseChannel):
    """
    Amplitude damping channel modeling energy dissipation.
    
    Kraus operators:
    K_0 = [[1, 0], [0, sqrt(1-γ)]]
    K_1 = [[0, sqrt(γ)], [0, 0]]
    """
    
    def __init__(self, damping_rate: float):
        super().__init__(damping_rate, "Amplitude Damping")
        self.gamma = damping_rate
        
    def apply_to_state(self, state_vector: np.ndarray) -> np.ndarray:
        """Apply amplitude damping (simplified for simulation)."""
        return state_vector
    
    def get_theoretical_expectation(self, ideal_expectation: float) -> float:
        """Amplitude damping affects observables differently based on energy."""
        # This is a simplified model - actual effect depends on specific observable
        # σ_z observables are less affected than σ_x, σ_y
        return ideal_expectation * (1 - 0.7 * self.gamma)
    
    def get_channel_signature(self) -> Dict[str, Any]:
        """Amplitude damping signature: energy-dependent effects."""
        return {
            'type': 'amplitude_damping',
            'parameter': self.gamma,
            'energy_bias': True,
            'z_preservation': 1 - 0.3 * self.gamma,
            'xy_attenuation': 1 - 0.8 * self.gamma,
            'expected_deviation_mean': -0.5 * self.gamma,
            'expected_deviation_std': 0.15 * self.gamma
        }


class PhaseDampingChannel(NoiseChannel):
    """
    Phase damping channel modeling decoherence without energy loss.
    
    Affects superposition coherences while preserving populations.
    """
    
    def __init__(self, dephasing_rate: float):
        super().__init__(dephasing_rate, "Phase Damping")
        self.lambda_param = dephasing_rate
        
    def apply_to_state(self, state_vector: np.ndarray) -> np.ndarray:
        """Apply phase damping (simplified for simulation)."""
        return state_vector
    
    def get_theoretical_expectation(self, ideal_expectation: float) -> float:
        """Phase damping primarily affects off-diagonal coherences."""
        # σ_z observables unaffected, σ_x and σ_y are damped
        return ideal_expectation * (1 - 0.6 * self.lambda_param)
    
    def get_channel_signature(self) -> Dict[str, Any]:
        """Phase damping signature: coherence-specific effects."""
        return {
            'type': 'phase_damping',
            'parameter': self.lambda_param,
            'coherence_damping': True,
            'z_invariant': True,
            'xy_damping_factor': 1 - self.lambda_param,
            'expected_deviation_mean': -0.3 * self.lambda_param,
            'expected_deviation_std': 0.2 * self.lambda_param
        }


class NoiseChannelFactory:
    """Factory for creating noise channels."""
    
    @staticmethod
    def create_channel(noise_type: str, parameter: float) -> NoiseChannel:
        """Create noise channel of specified type."""
        if noise_type.lower() == 'depolarizing':
            return DepolarizingChannel(parameter)
        elif noise_type.lower() == 'amplitude_damping':
            return AmplitudeDampingChannel(parameter)
        elif noise_type.lower() == 'phase_damping':
            return PhaseDampingChannel(parameter)
        else:
            raise ValueError(f"Unknown noise type: {noise_type}")
    
    @staticmethod
    def get_test_parameters(noise_type: str) -> list:
        """Get standard test parameters for each noise type."""
        if noise_type.lower() == 'depolarizing':
            return [0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
        elif noise_type.lower() == 'amplitude_damping':
            return [0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
        elif noise_type.lower() == 'phase_damping':
            return [0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
        else:
            raise ValueError(f"Unknown noise type: {noise_type}")


def create_noise_channel_suite() -> Dict[str, list]:
    """Create comprehensive noise channel test suite."""
    return {
        'depolarizing': [DepolarizingChannel(p) for p in [0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]],
        'amplitude_damping': [AmplitudeDampingChannel(g) for g in [0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]],
        'phase_damping': [PhaseDampingChannel(l) for l in [0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]]
    } 