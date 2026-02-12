from typing import Dict, Optional

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, amplitude_damping_error, phase_damping_error
import sys
import re
import glob, os

import cirq
from cirq import DensityMatrixSimulator
from cirq.circuits import InsertStrategy
from cirq.contrib.qasm_import import circuit_from_qasm
from collections import Counter

from noise import NoiseChannel, DepolarizingChannel, AmplitudeDampingChannel, PhaseDampingChannel
from stat4noise import js_divergence

import time

def get_noise_model_cirq(noise_channel: NoiseChannel):
  noise_config = {
            'type': noise_channel.name,
            'parameter': noise_channel.parameter
        }
  return noise_config

def _add_noise_to_circuit(current_noise_channel: NoiseChannel, circuit: cirq.Circuit) -> cirq.Circuit:
  if current_noise_channel is None:
      return circuit

  noisy_circuit = cirq.Circuit()

  for moment in circuit:
    # Add the original operations
    noisy_circuit.append(moment, strategy=InsertStrategy.NEW_THEN_INLINE)

    # Add noise after each gate
    for operation in moment:
      if isinstance(current_noise_channel, DepolarizingChannel):
        # Add depolarizing noise to each qubit involved
        for qubit in operation.qubits:
            noise_op = cirq.depolarize(p=current_noise_channel.p).on(qubit)
            noisy_circuit.append(noise_op, strategy=InsertStrategy.INLINE)

      elif isinstance(current_noise_channel, AmplitudeDampingChannel):
        # Add amplitude damping noise
        for qubit in operation.qubits:
            noise_op = cirq.amplitude_damp(gamma=current_noise_channel.gamma).on(qubit)
            noisy_circuit.append(noise_op, strategy=InsertStrategy.INLINE)

      elif isinstance(current_noise_channel, PhaseDampingChannel):
        # Add phase damping noise
        for qubit in operation.qubits:
            noise_op = cirq.phase_damp(gamma=current_noise_channel.lambda_param).on(qubit)
            noisy_circuit.append(noise_op, strategy=InsertStrategy.INLINE)
      else:
        raise ValueError(
            "NoiseModel.name must be valid. ",
            "Use DepolarizingChannel, AmplitudeDampingChannel, or PhaseDampingChannel"
        )

  return noisy_circuit

def get_noise_model_qiskit(noise_channel: NoiseChannel):
  noise_model = NoiseModel()

  if isinstance(noise_channel, DepolarizingChannel):
      # Add depolarising errors to all single and two-qubit gates
      error_1q = depolarizing_error(noise_channel.p, 1)
      error_2q = depolarizing_error(noise_channel.p, 2)

      # Apply to common gates
      noise_model.add_all_qubit_quantum_error(error_1q, ['id', 'u1', 'u2', 'u3', 'h', 'x', 'y', 'z'])
      noise_model.add_all_qubit_quantum_error(error_2q, ['cx', 'cy', 'cz'])

  elif isinstance(noise_channel, AmplitudeDampingChannel):
      # Add amplitude damping errors
      error_1q = amplitude_damping_error(noise_channel.gamma)

      # Apply to all single-qubit gates
      noise_model.add_all_qubit_quantum_error(error_1q, ['id', 'u1', 'u2', 'u3', 'h', 'x', 'y', 'z'])

  elif isinstance(noise_channel, PhaseDampingChannel):
      # Add phase damping errors
      error_1q = phase_damping_error(noise_channel.lambda_param)

      # Apply to all single-qubit gates
      noise_model.add_all_qubit_quantum_error(error_1q, ['id', 'u1', 'u2', 'u3', 'h', 'x', 'y', 'z'])

  else:
      raise ValueError(
          "NoiseModel.name must be valid. ",
          noise_channel.name,
          "Use DepolarizingChannel, AmplitudeDampingChannel, or PhaseDampingChannel"
      )

  return noise_model

def read_QASM2_to_Qiskit(qasm2_file):
  # Read and print QASM 2.0 code as plain text
  try:
      with open(qasm2_file, "r") as f:
          qasm2_raw = f.read()
  except Exception as e:
      print(f"Error reading QASM 2.0 file: {e}")
      sys.exit(1)

  # Load QASM 2.0 into a QuantumCircuit
  try:
      qc = QuantumCircuit.from_qasm_str(qasm2_raw)
      qc = qc.remove_final_measurements(inplace=False)
      #print("\n--- Parsed QASM 2.0 as QuantumCircuit ---\n")
      #print(qc)
  except Exception as e:
      print(f"Error parsing QASM 2.0 file: {e}")
      sys.exit(1)

  return qc

def read_QASM2_to_Cirq(qasm2_file):
  # Read QASM 2.0 file
  try:
      with open(qasm2_file, "r") as f:
          qasm2_raw = f.read()
  except Exception as e:
      print(f"Error reading QASM 2.0 file: {e}")
      sys.exit(1)

  # Parse QASM into Cirq circuit
  try:
      circuit = circuit_from_qasm(qasm2_raw)
      #print("\n--- Parsed QASM 2.0 as Cirq circuit ---\n")
      #print(circuit)
  except Exception as e:
      print(f"Error parsing QASM 2.0 file with Cirq: {e}")
      sys.exit(1)

  return circuit

def get_qubit_count_from_name(filename):
  m = re.search(r'_(\d+)\.qasm$', filename)
  return int(m.group(1)) if m else None

def align_counts(counts_qiskit, counts_cirq):
  keys = sorted(set(counts_qiskit) | set(counts_cirq))

  q_vals = [counts_qiskit.get(k, 0) for k in keys]
  c_vals = [counts_cirq.get(k, 0) for k in keys]

  return keys, q_vals, c_vals

###########################################################################

noise_configs_ibm = [
            ('depolarizing', DepolarizingChannel(2.824e-4)),
            ('amplitude_damping', AmplitudeDampingChannel(1.98e-4)),
            ('phase_damping', PhaseDampingChannel(1.54e-4))
        ]

noise_configs_quantinuum_h2 = [
            ('depolarizing', DepolarizingChannel(6e-5)),        # ~2 * (1Q infidelity) proxy
            ('amplitude_damping', AmplitudeDampingChannel(1e-5)), # small; trapped-ion relaxation not usually dominant
            ('phase_damping', PhaseDampingChannel(2e-4))        # memory-error-as-dephasing proxy
        ]

path = 'MQTBench/'

start = time.time()

## Just to do: sed -i "s:barrier://barrier:g" * -> to avoid cirq problem with it.
## Fix of exta regs: sed -i "s:creg c://creg c:g" *
all_done=0
JS_i_total = []
JS_i_std = []
R = 30
for qasm_filename in glob.glob(os.path.join(path, '*.qasm')):

  size = get_qubit_count_from_name(qasm_filename)
  if (size > 11) or (size < 5):
    #print(f">> Skip {size} of name {qasm_filename}")
    continue
  else:
    print(f">> Read {size} of name {qasm_filename}")

  # Read both:
  all_done = all_done+1
  qiskitC = read_QASM2_to_Qiskit(qasm_filename)
  cirqC = read_QASM2_to_Cirq(qasm_filename)

  # Qiskit - build current test
  #noise_qiskit = get_noise_model_qiskit(DepolarizingChannel(2.824e-4))
  noise_qiskit = get_noise_model_qiskit(PhaseDampingChannel(2e-4))
  qiskitC.measure_all()
  simulator = AerSimulator()

  # CirQ - build current test
  simulator_cirq = DensityMatrixSimulator()
  n_qubits=size
  qubits = sorted(cirqC.all_qubits())
  #cirqC = _add_noise_to_circuit(DepolarizingChannel(2.824e-4), cirqC)
  cirqC = _add_noise_to_circuit(PhaseDampingChannel(1.54e-4), cirqC)
  for i in range(n_qubits - 1, -1, -1):
    cirqC.append(cirq.measure(qubits[i], key=f'q{i}'))

  divergance_vals = []
  for r in range(R): # to 30
    qiskitCi = qiskitC.copy()
    cirqCi = cirqC.copy()

    # Qiskit - Results
    job = simulator.run(
        transpile(qiskitCi, simulator,optimization_level=0),
        shots=10000,
        noise_model=noise_qiskit
    )
    result = job.result()
    counts = result.get_counts()
    #print(counts)

    # Cirq - Results
    result = simulator_cirq.run(cirqCi, repetitions=10000)

    # Stack per-qubit measurement results: shape (shots, n_qubits)
    bits = np.column_stack([
        result.measurements[f"q{k}"][:, 0]
        for k in range(n_qubits)
    ])
    # Convert each shot to a bitstring
    bitstrings = ["".join(str(int(b)) for b in row[::-1]) for row in bits]
    # Equivalent of value_counts().to_dict()
    __counts = dict(Counter(bitstrings))
    print(counts, __counts)

    keys, q_vals, c_vals = align_counts(counts, __counts)
    if not bool(divergance_vals): # Just print once
      print("First set: (skip printing the rest)")
      print(keys, q_vals, c_vals)

    js_i = js_divergence(q_vals, c_vals, outcomes=keys, base=2)
    print("JS(A1,A2) =",js_i)
    divergance_vals.append(js_i)

  # Wrapping up for this circuit:
  avg_JS = np.mean(divergance_vals)
  JS_i_total.append(avg_JS)
  print(f"JS AVG: {avg_JS} JS STD: {np.std(divergance_vals)}")
  print ("")
###### END OF LOOP



### END
print(f">> END. Read {all_done} test cases.")
print(f"Avg: {np.mean(JS_i_total)} and STD: {np.std(JS_i_total)}")
end = time.time()
print(end - start)
