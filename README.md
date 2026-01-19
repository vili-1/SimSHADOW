# SimSHADOW: Live Noise Fingerprinting in Quantum Software Engineering

SimSHADOW provides systematic validation of quantum simulators through a lightweight, shadow-inspired fingerprinting protocol, enabling efficient cross-platform comparison and noise characterisation without full state tomography.


## Artifact & Reproducibility

This repository is the artifact for the paper *Toward Live Noise Fingerprinting in Quantum Software Engineering*.

### Quick Start (local execution)

**1. Requirments**

```
sudo apt-get install python3-pip
python3 -m pip --version
python3 -m pip install "qiskit~=2.2" "qiskit-aer~=0.17" "qiskit-nature~=0.7" scipy
pip install openfermion
pip install --upgrade cirq
pip install --quiet ply
pip install qiskit_qasm3_import
pip install qiskit

# Test all ok
python -c "import qiskit, cirq; print('ok')"
```

**2. Navigate to the artifact directory**

```bash
cd ~/SimSHADOW_artifact
```

**3. Activate the experiment environment**

The authors used Python 3.12 in a local virtual environment named `.venv312`:

```bash
source .venv312/bin/activate
```

If you prefer to create your own environment instead:

```bash
python -m venv simshadow_env
source simshadow_env/bin/activate  # On Windows: simshadow_env\Scripts\activate

pip install -r requirements.txt
pip install -e .
```

**4. Reproduce Results**

To reproduce the figures in the paper, follow the instructions in [scripts](https://github.com/vili-1/SimSHADOW_artifact/blob/main/scripts/README.md).

**5. Run the complete experiment (generate fresh data)**

```bash
python run_simshadow.py
```

This will:

- Generate **9** test quantum states
- Utilise **15** observables
- Perform **10000** shots per configuration
- Generate fingerprint matrices for **2** platforms: Qiskit and Cirq
- Compute cross-platform Frobenius distances between fingerprints
- Run physics-informed noise channel classification and parameter estimation
- Save timestamped results to `results/simshadow_results_*.json` and detailed logs to `logs/`

**6. Generate figures from the latest results**

```bash
python Documentation/gen_figures.py 2>&1 | grep -v "UserWarning"
```

This creates:

- `figures/figure2_fingerprints.pdf` (Figure 2 from the paper)
- `figures/figure3_scaling.pdf` (Figure 3 from the paper)

To reproduce multiple (for e.g., three) independent runs:

```bash
for i in 1 2 3; do
  python run_simshadow.py
  python Documentation/gen_figures.py 2>&1 | grep -v "UserWarning"
  cp figures/figure2_fingerprints.pdf figures/figure2_fingerprints_run${i}.pdf
done
```

**7. Verify expected outputs**

```bash
python verify.py
```

Expected outputs:

- `results/simshadow_results_*.json` (experimental data)
- `results/simshadow_report_*.txt` (human-readable summaries)
- `logs/simshadow_experiment_*.log` (detailed execution traces)
- `results/table1_identification.txt`
- `figures/figure2_fingerprints.pdf`
- `figures/figure3_scaling.pdf`

### What Gets Generated

**Experimental Data:**

- **810 measurements** across 9 states, 15 observables, 3 noise types, 2 platforms
- **405,000 quantum shots** with real Qiskit and Cirq execution
- **Cross-platform distances** (Frobenius norms between platforms)
- **Performance metrics** (execution times, throughput)

**Figures:**

- **Figure 2**: Fingerprint visualizations showing noise patterns
- **Figure 3**: Scaling comparison (SimSHADOW vs Process Tomography)

**Results:**

- JSON files with complete experimental data
- Text reports with human-readable summaries
- Log files with detailed execution traces

### Experimental Setup Details

**Test States (9):**

- 4 computational basis states: |00⟩, |01⟩, |10⟩, |11⟩
- 4 superposition states: |+0⟩, |-0⟩, |0+⟩, |0-⟩  
- 1 entangled state: |Φ⁺⟩ Bell state (for 2 qubits)

**Observables (15 per state):**

- 9 two-qubit Pauli observables: XX, XY, XZ, YX, YY, YZ, ZX, ZY, ZZ
- 6 single-qubit observables: XI, IX, YI, IY, ZI, IZ

**Noise Types (3):**

- Depolarizing noise (parameter: 0.05)
- Amplitude damping (parameter: 0.10)
- Phase damping (parameter: 0.08)

**Platforms (2):**

- Qiskit AerSimulator
- Cirq DensityMatrixSimulator

**Measurement Protocol:**

- 10000 quantum shots per measurement configuration
- Direct measurement in each observable's eigenbasis (no full classical shadow reconstruction)
- Ideal expectations computed analytically (no 10k-shot noiseless runs)

## How Fingerprints Are Generated

### Core Concept

A **noise fingerprint** is a quantitative signature that captures how noise affects quantum measurements. It's a matrix where each entry represents the deviation between what we observe with noise versus what we'd expect ideally.

**Fingerprint Formula:**

```
F[state_i, observable_j] = E_noisy - E_ideal
```

Where:

- `E_noisy` = expectation value measured with noise
- `E_ideal` = expectation value computed without noise

### Step-by-Step Process

**1. Test Suite Design**

- **9 quantum states**: 4 computational basis states (|00⟩, |01⟩, |10⟩, |11⟩), 4 superposition states (|+0⟩, |-0⟩, |0+⟩, |0-⟩), and 1 entangled state (|GHZ⟩)
- **15 Pauli observables**: 9 two-qubit observables (XX, XY, XZ, YX, YY, YZ, ZX, ZY, ZZ) and 6 single-qubit observables (XI, IX, YI, IY, ZI, IZ)

**2. For Each State-Observable Pair (9 × 15 = 135 measurements per platform):**

   **a) Noisy Measurement:**
   
   - Prepare the quantum state on the simulator
   - Apply the configured noise model (depolarizing, amplitude damping, or phase damping)
   - Rotate into the appropriate Pauli basis for the observable
   - Measure the observable using 500 quantum shots
   - Compute expectation value: `E_noisy = ⟨ψ|O|ψ⟩` from measurement statistics, with eigenvalues in [-1, +1]
   
   **b) Ideal Expectation:**
   
   - Same state and observable, but evaluated analytically (no noise, no sampling error)
   - Compute expectation value: `E_ideal = ⟨ψ|O|ψ⟩` from the state vector and operator definition

   **c) Fingerprint Entry:**
   
   ```
   F[state_i, observable_j] = E_noisy - E_ideal
   ```
   This quantifies the deviation caused by noise.

**3. Result:**

- A 9×15 matrix per platform per noise type
- Each entry quantifies how noise affects that specific state-observable combination
- Patterns in the matrix reveal noise characteristics and platform differences

**4. Cross-Platform Comparison:**

- Compute Frobenius distance between Qiskit and Cirq fingerprints
- Large distances indicate implementation differences between platforms

### Classification and Parameter Estimation

After constructing the fingerprint matrices, SimSHADOW:

- Extracts statistical features (mean deviation, standard deviation, Frobenius norm, sparsity, max deviation, variance pattern)
- Applies **physics-informed decision rules** to classify the dominant noise type (depolarizing, amplitude damping, phase damping)
- Uses **calibrated formulas** to estimate noise parameters:
  - Depolarizing: $p \approx |\mu_F| / C_{\text{dep}}$ with $C_{\text{dep}} \approx 2.14$
  - Amplitude damping: $\gamma \approx \tfrac{1}{2}(|\mu_F| / C_{\text{amp}} + \text{var}_{\text{pattern}}/0.001)$ with $C_{\text{amp}} \approx 1.44$
  - Phase damping: $\lambda \approx (1 - s) \cdot C_{\text{phase}}$ with $C_{\text{phase}} \approx 0.094$

These thresholds and constants are **tuned for the specific parameters used in the experiments** (0.05, 0.10, 0.08). They demonstrate feasibility (e.g., phase damping is correctly identified on both platforms and estimated within ~3% error), but they are **not universal**; applying the same rules to different parameter ranges would require re-calibration or automated adaptation (left as future work).

### Why This Works

- Different noise types affect states/observables in distinct ways
- Each platform implements noise models with slight variations
- The fingerprint matrix captures these systematic differences quantitatively

### Example 1: Computational Basis State |00⟩ with XX Observable

**State-Observable Pair:**

- **State:** |00⟩ (computational basis state)
- **Observable:** XX (two-qubit Pauli operator X ⊗ X)
- **Matrix Position:** F[0, 0] in the fingerprint matrix

**State Preparation:**

- State vector: `[1, 0, 0, 0]` (normalized)
- Circuit: No gates needed (qubits initialize to |0⟩)

**Observable:**

- Operator: X ⊗ X
- Matrix:
  
  ```
  [[0  0  0  1]
   [0  0  1  0]
   [0  1  0  0]
   [1  0  0  0]]
  ```

**Ideal Expectation Value (Noiseless):**

- Computation: `E_ideal = ⟨00|XX|00⟩ = 0.000000`
- Interpretation: For |00⟩, the XX expectation is 0 (no correlation)

**Noisy Measurement Process:**

1. Prepare |00⟩ on simulator
2. Apply 5% depolarizing noise (after each gate)
3. Rotate to X-basis: Apply `RY(-π/2)` to both qubits
4. Measure both qubits in computational basis
5. Execute 500 shots, collect bitstring statistics
6. Compute expectation from measurement outcomes

**Expectation Value Calculation:**

```
E = Σ (parity(bitstring) × count(bitstring)) / total_shots
```

Where parity = +1 for even parity (00, 11), -1 for odd parity (01, 10)

**Fingerprint Computation:**

```
F[0, 0] = E_noisy - E_ideal
```

**Actual Values from Experiment:**

- **Qiskit fingerprint:** F[0,0] = 0.029800
- **Cirq fingerprint:** F[0,0] = 0.032000
- **Cross-platform difference:** 0.002200

**Physical Interpretation:**

- The ideal XX expectation for |00⟩ is 0
- With 5% depolarizing noise, both platforms show small positive deviations (~0.03)
- The difference (0.0022) reflects platform-specific noise implementation differences
- This entry captures how depolarizing noise affects the |00⟩ state when measuring XX

### Example 2: GHZ Entangled State with ZZ Observable

**State-Observable Pair:**

- **State:** |GHZ⟩ = (|00⟩ + |11⟩)/√2 (maximally entangled Bell state)
- **Observable:** ZZ (two-qubit Pauli operator Z ⊗ Z)
- **Matrix Position:** F[8, 8] in the fingerprint matrix

**State Preparation:**

- State vector: `[0.707, 0, 0, 0.707]` (normalised: 1/√2 for |00⟩ and |11⟩)
- Preparation circuit:
  ```
  |0⟩ ────[H]───*─── |GHZ⟩
  |0⟩ ────────[X]─── |GHZ⟩
  ```
  (H on qubit 0, then CNOT from 0→1)
- This state is maximally entangled: measuring one qubit determines the other

**Observable:**

- Operator: Z ⊗ Z
- Matrix:
  ```
  [[ 1  0  0  0]
   [ 0 -1  0  0]
   [ 0  0 -1  0]
   [ 0  0  0  1]]
  ```
- Measures correlation: +1 if qubits are the same (|00⟩, |11⟩), -1 if different (|01⟩, |10⟩)

**Ideal Expectation Value (Noiseless):**

- Computation: `E_ideal = ⟨GHZ|ZZ|GHZ⟩ = +1.000000`
- Interpretation:
  - |00⟩ has ZZ = +1 (both qubits in |0⟩)
  - |11⟩ has ZZ = +1 (both qubits in |1⟩)
  - GHZ = (|00⟩ + |11⟩)/√2, so ⟨ZZ⟩ = +1
  - This measures perfect correlation!

**Noisy Measurement Process:**

1. Prepare GHZ state with noise after each gate:
   ```
   |0⟩ ────[H]───[Noise]───*───[Noise]─── |GHZ⟩
   |0⟩ ───────────────────[X]───[Noise]─── |GHZ⟩
   ```
2. Apply 5% depolarizing noise after each gate (H, CNOT)
3. Measure in Z-basis (no rotation needed for ZZ)
4. Execute 500 shots, collect bitstring statistics
5. Compute expectation from outcomes

**Expectation Value Calculation:**

```
E = (counts[00] + counts[11] - counts[01] - counts[10]) / total_shots
```

- For ideal GHZ, expect mostly |00⟩ and |11⟩
- Noise causes some |01⟩ and |10⟩ (decoherence/entanglement loss)

**Fingerprint Computation:**

```
F[8, 8] = E_noisy - E_ideal
```

Since E_ideal = +1, the fingerprint shows how much noise reduces the perfect correlation.

**Actual Values from Experiment:**

- **Qiskit fingerprint:** F[8,8] = -0.036000
- **Cirq fingerprint:** F[8,8] = -0.140000
- **Cross-platform difference:** 0.104000

**Physical Interpretation:**

- Ideal correlation: +1.0 (perfect entanglement)
- Qiskit: E_noisy ≈ 0.964 (noise reduces correlation by ~3.6%)
- Cirq: E_noisy ≈ 0.860 (noise reduces correlation by ~14.0%)
- The fingerprint is negative because noise degrades entanglement
- The larger magnitude for Cirq suggests different noise implementation or modeling


This entry captures how depolarizing noise affects entangled states when measuring correlation, which is crucial for quantum algorithms that rely on entanglement.


## Experimental Results (summary)

The full numerical results are stored in the timestamped JSON files in `results/` (for example `results/simshadow_results_20251215_181631.json`). Below we summarise the most recent run.

### Cross-platform distances (Frobenius norm)

For fingerprints $F^{(A)}$ and $F^{(B)}$ from Qiskit and Cirq, we use the Frobenius distance $\lVert F^{(A)} - F^{(B)} \rVert_F$. For the three tested noise types:

| Noise Type        | Frobenius Distance (Qiskit vs Cirq) |
|-------------------|--------------------------------------|
| Depolarising      | 7.18                                 |
| Amplitude damping | 6.67                                 |
| Phase damping     | 7.33                                 |

These distances are roughly an order of magnitude larger than the expected contribution from statistical noise alone (≈0.74 in Frobenius norm for 135 measurements with 500 shots each), indicating systematic implementation differences between the two simulators even under identical nominal parameters.

### Performance benchmarks (real circuit execution)

Using 810 measurements (9 states × 15 observables × 3 noise types × 2 platforms) with 500 shots each:

| Platform               | Total time (s) | Shots/sec  |
|------------------------|----------------|-----------:|
| Qiskit AerSimulator    | 77.0           |   2,629    |
| Cirq DensityMatrixSimulator | 1.57      | 129,319    |

This corresponds to a ~49× speedup for Cirq over Qiskit for this noisy validation workload.

### Noise identification accuracy

From quantum measurements and the current **physics‑informed rules**:

| Noise Channel     | Qiskit | Cirq  | Combined |
|-------------------|--------|-------|----------|
| Depolarising      | 0.0%   | 0.0%  | 0.0%     |
| Amplitude damping | 84.0%  | 83.5% | 83.8%    |
| Phase damping     | 63.3%  | 62.8% | 63.1%    |
| **Overall average** | **49.1%** | **48.8%** | **49.0%** |

These results reflect both strengths and limitations of the current heuristic classifier:

- Phase damping is reliably identified on both platforms, and amplitude damping is correctly identified on Qiskit, showing that the fingerprints contain informative structure.
- Depolarising noise is not predicted by the current rules in our test grid (0.05, 0.10, 0.08), hence the 0.0% entries. This exposes a limitation of the simple thresholds rather than a property of the fingerprints themselves.
- The thresholds and calibration constants are tuned for this specific experiment; applying them to different parameter ranges or additional noise types would require re‑calibration or a more sophisticated learning‑based classifier.
