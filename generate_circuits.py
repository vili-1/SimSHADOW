#!/usr/bin/env python3
"""
Generate three interesting quantum circuits and export them as QASM files.

Constraint: avoid Hadamard; use rotations (RY/RZ), X, Z, CX.
"""

import math
import os
from qiskit import QuantumCircuit
from qiskit.qasm2 import dumps


def create_circuit1_entangled_rotation():
    """
    Circuit 1: Entangle then add asymmetric rotations.
    - RY(pi/2) to build superposition without H
    - CX to entangle
    - RZ(pi/3) on target to inject relative phase
    - X on control to flip phase sector
    """
    qc = QuantumCircuit(2, name="entangled_rotation")

    qc.ry(math.pi / 2, 0)
    qc.cx(0, 1)
    qc.rz(math.pi / 3, 1)
    qc.x(0)

    return qc


def create_circuit2_rotation_chain():
    """
    Circuit 2: Rotation chain with interleaved CX.
    - Local RY/RZ to set amplitudes/phases
    - CX to spread phases
    - Opposite-side RY to skew entanglement weight
    """
    qc = QuantumCircuit(2, name="rotation_chain")

    qc.ry(math.pi / 4, 0)
    qc.rz(math.pi / 6, 1)
    qc.cx(0, 1)
    qc.ry(-math.pi / 3, 1)
    qc.cx(1, 0)

    return qc


def create_circuit3_phase_kickback():
    """
    Circuit 3: Phase-kickback style without H.
    - RZ then CX to share phase
    - Counter-phase on target
    - X + RY to alter population and phase jointly
    """
    qc = QuantumCircuit(2, name="phase_kickback")

    qc.rz(math.pi / 2, 0)
    qc.cx(0, 1)
    qc.rz(-math.pi / 2, 1)
    qc.x(1)
    qc.ry(math.pi / 3, 0)

    return qc

def main():
    """Generate circuits, print diagrams, and export QASM files."""
    
    # Create output directory
    output_dir = 'circuits'
    os.makedirs(output_dir, exist_ok=True)
    
    # Define circuits
    circuits = [
        ('circuit1_entangled_rotation', create_circuit1_entangled_rotation()),
        ('circuit2_rotation_chain', create_circuit2_rotation_chain()),
        ('circuit3_phase_kickback', create_circuit3_phase_kickback())
    ]
    
    print("=" * 70)
    print("Generating Quantum Circuits")
    print("=" * 70)
    print()
    
    for name, qc in circuits:
        print(f"\n{name.upper().replace('_', ' ')}")
        print("-" * 70)
        
        # Print circuit diagram
        print("\nCircuit Diagram:")
        print(qc.draw(output='text'))
        
        # Export to QASM
        qasm_str = dumps(qc)
        qasm_file = os.path.join(output_dir, f'{name}.qasm')
        
        with open(qasm_file, 'w') as f:
            f.write(qasm_str)
        
        print(f"\n✓ Exported to: {qasm_file}")
        print(f"  Gates: {qc.size()} operations")
        print(f"  Depth: {qc.depth()}")
    
    print("\n" + "=" * 70)
    print(f"All circuits exported to '{output_dir}/' directory")
    print("=" * 70)

if __name__ == "__main__":
    main()
