#!/usr/bin/env python3
"""
Generate three interesting quantum circuits and export them as QASM files.

Circuits use gates already in use: X, H, Z, CX (CNOT)
"""

from qiskit import QuantumCircuit
from qiskit.qasm2 import dumps
import os

def create_circuit1_entangled_rotation():
    """
    Circuit 1: Entangled state with rotation
    Creates a Bell state (|Φ⁺⟩) and applies a phase rotation on one qubit.
    This demonstrates entanglement with local phase operations.
    """
    qc = QuantumCircuit(2, name='entangled_rotation')
    
    # Create Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
    qc.h(0)           # Hadamard on qubit 0
    qc.cx(0, 1)       # CNOT: entangle qubits
    
    # Apply phase rotation (Z gate) on qubit 1
    # This creates |Φ⁻⟩ = (|00⟩ - |11⟩)/√2
    qc.z(1)
    
    return qc

def create_circuit2_superposition_chain():
    """
    Circuit 2: Superposition chain with controlled operations
    Creates superposition on both qubits, then applies controlled operations.
    Demonstrates superposition and controlled-phase effects.
    """
    qc = QuantumCircuit(2, name='superposition_chain')
    
    # Create superposition on both qubits
    qc.h(0)           # |+⟩ on qubit 0
    qc.h(1)           # |+⟩ on qubit 1
    
    # Apply CNOT to create entanglement
    qc.cx(0, 1)
    
    # Apply phase gate on qubit 1
    qc.z(1)
    
    # Apply another Hadamard on qubit 1 to mix phase effects
    qc.h(1)
    
    return qc

def create_circuit3_bell_variant():
    """
    Circuit 3: Bell state variant with additional gates
    Creates a Bell state and applies additional operations to create
    a more complex entangled state pattern.
    """
    qc = QuantumCircuit(2, name='bell_variant')
    
    # Start with Bell state preparation
    qc.h(0)           # Hadamard on qubit 0
    qc.cx(0, 1)       # CNOT: entangle
    
    # Apply X gate on qubit 1 (bit flip)
    qc.x(1)
    
    # Apply Z gate on qubit 0 (phase flip)
    qc.z(0)
    
    # Apply another Hadamard on qubit 0
    qc.h(0)
    
    return qc

def main():
    """Generate circuits, print diagrams, and export QASM files."""
    
    # Create output directory
    output_dir = 'circuits'
    os.makedirs(output_dir, exist_ok=True)
    
    # Define circuits
    circuits = [
        ('circuit1_entangled_rotation', create_circuit1_entangled_rotation()),
        ('circuit2_superposition_chain', create_circuit2_superposition_chain()),
        ('circuit3_bell_variant', create_circuit3_bell_variant())
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
