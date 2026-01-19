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
        

class DepolarizingChannel(NoiseChannel):
    """
    Depolarizing noise channel: Λ(ρ) = (1-p)ρ + p(I/d)
    
    Uniformly mixes the state with the maximally mixed state.
    """
    
    def __init__(self, depolarizing_probability: float):
        super().__init__(depolarizing_probability, "Depolarizing")
        self.p = depolarizing_probability
        
class AmplitudeDampingChannel(NoiseChannel):
    """
    Amplitude damping channel modeling energy dissipation.
    """
    
    def __init__(self, damping_rate: float):
        super().__init__(damping_rate, "Amplitude Damping")
        self.gamma = damping_rate
        
class PhaseDampingChannel(NoiseChannel):
    """
    Phase damping channel modeling decoherence without energy loss.
    
    Affects superposition coherences while preserving populations.
    """
    
    def __init__(self, dephasing_rate: float):
        super().__init__(dephasing_rate, "Phase Damping")
        self.lambda_param = dephasing_rate
        
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
