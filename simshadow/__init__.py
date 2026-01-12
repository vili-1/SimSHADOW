"""
SimSHADOW: Cross-Platform Quantum Simulator Validation through Classical Shadow Fingerprinting

A framework for efficient characterization and validation of quantum simulator noise models
across different platforms using classical shadow tomography.
"""

__version__ = "1.0.0"
__author__ = "Anonymous"

from .core.shadow_tomography import ClassicalShadowTomography
from .core.fingerprint import NoiseFingerprint, FingerprintMatrix
from .core.noise_models import NoiseChannel, DepolarizingChannel, AmplitudeDampingChannel, PhaseDampingChannel
from .platforms.qiskit_platform import QiskitPlatform
from .platforms.cirq_platform import CirqPlatform
from .experiments.validation_suite import ValidationSuite
__all__ = [
    "ClassicalShadowTomography",
    "NoiseFingerprint", 
    "FingerprintMatrix",
    "NoiseChannel",
    "DepolarizingChannel",
    "AmplitudeDampingChannel", 
    "PhaseDampingChannel",
    "QiskitPlatform",
    "CirqPlatform", 
    "ValidationSuite"
] 