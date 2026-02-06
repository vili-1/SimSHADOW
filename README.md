# SimSHADOW: Live Noise Fingerprinting in Quantum Software Engineering

SimSHADOW provides systematic validation of quantum simulators through a lightweight, shadow-inspired fingerprinting protocol, enabling efficient cross-platform comparison and noise characterisation without full state tomography.


## Artifact & Reproducibility

This repository is the artifact for the paper *Toward Live Noise Fingerprinting in Quantum Software Engineering*.

### Experimental Setup Documentation

**Test States (13):**

- 4 computational basis states: |00⟩, |01⟩, |10⟩, |11⟩
- 8 superposition states: |+0⟩, |-0⟩, |0+⟩, |0-⟩, |+1⟩, |-1⟩, |1+⟩, |1-⟩  
- 1 entangled state: |Φ⁺⟩ Bell state (for 2 qubits)

**Observables (9 per state):**

- 9 two-qubit Pauli observables: XX, XY, XZ, YX, YY, YZ, ZX, ZY, ZZ

**Noise Types (3):**

- Depolarizing noise
- Amplitude damping 
- Phase damping

**Configurations (4) of Noise Types (3):**

TODO: Elena, please add the description. Elaborate more on the real ones, Quantinuum and IBM
- Low
- High
- Quantinuum H2
- IBM Boston

**Platforms (2):**

- Qiskit AerSimulator
- Cirq DensityMatrixSimulator

**Measurement Protocol:**

- 10000 quantum shots per measurement configuration
- Direct measurement in each observable's eigenbasis (no full classical shadow reconstruction)
- Ideal expectations computed analytically (from theory; no 10k-shot noiseless runs)

### Noise Finger Print Results

#### Low:

<p align="center">
  <img src="https://github.com/user-attachments/assets/ee262a25-62c6-41f9-8b7d-2baa74b16ac0" width="250"/>
  <img src="https://github.com/user-attachments/assets/a19c346c-b142-4fd1-9c78-bf41b148e5fe" width="250"/>
  <img src="https://github.com/user-attachments/assets/9b421888-2a18-4bfa-be1a-3f289e2cac5b" width="250"/>
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/ac292f05-d729-4baf-832a-4f594ed3b712" width="250"/>
  <img src="https://github.com/user-attachments/assets/399e1575-0f1c-4818-a3e2-ea6669929a3e" width="250"/>
  <img src="https://github.com/user-attachments/assets/ef05752a-4d2f-4155-90c7-061c6d42f20d" width="250"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/706cd7b6-be95-49bf-a6e6-663e8207fc46" width="250"/>
  <img src="https://github.com/user-attachments/assets/5f3cd0e9-a373-437f-9bc5-80d16d93a605" width="250"/>
  <img src="https://github.com/user-attachments/assets/61f6b22f-fb82-4008-997e-32ab505c100e" width="250"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/43bf1d3d-49a7-4bd9-982e-ea8d5eb7a539" width="250"/>
  <img src="https://github.com/user-attachments/assets/837a8ab8-c257-4477-8c73-7598d303b9e9" width="250"/>
  <img src="https://github.com/user-attachments/assets/840d5c3b-1c67-43c8-8001-c15a5e46157e" width="250"/>
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/68367837-8ae7-41b3-b5b1-14d7b9611819" width="250"/>
  <img src="https://github.com/user-attachments/assets/50c815dd-20c5-4ad8-86c0-da78e237a393" width="250"/>
  <img src="https://github.com/user-attachments/assets/b6ebfde5-01c3-49d2-9335-fb7faba7f3cb" width="250"/>
</p>




#### High:

<p align="center">
  <img src="https://github.com/user-attachments/assets/0ff7a4c7-1f94-4787-b683-bb22efcc49c3" width="250"/>
  <img src="https://github.com/user-attachments/assets/bf44e632-7240-437a-aece-4a8a837f6016" width="250"/>
  <img src="https://github.com/user-attachments/assets/1a8341db-48c3-4415-9e78-e19aa83a9316" width="250"/>
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/7bd2732e-1b9a-4b2e-b497-57b14d2dd1b8" width="250"/>
  <img src="https://github.com/user-attachments/assets/9587f4f6-2b6e-4a0b-a075-114d7b2944bd" width="250"/>
  <img src="https://github.com/user-attachments/assets/53fb37ae-0350-4433-b359-860b282805ad" width="250"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/5de069cf-692d-4d7a-86bd-9e898f3e077f" width="250"/>
  <img src="https://github.com/user-attachments/assets/4474a94c-c8b1-44b9-8136-ce1c4e1afee6" width="250"/>
  <img src="https://github.com/user-attachments/assets/3b8a0de1-4d53-4618-9498-4f0d3ecd8e60" width="250"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/827ff25d-8855-4780-92f4-bb4c339196c5" width="250"/>
  <img src="https://github.com/user-attachments/assets/117095bc-f1ad-4689-b103-466c9018d7cf" width="250"/>
  <img src="https://github.com/user-attachments/assets/4f70a7f9-39d7-4f10-91b1-79d7e228f6e1" width="250"/>
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/e3488cab-9c1a-4962-9a5b-08ad306796ae" width="250"/>
  <img src="https://github.com/user-attachments/assets/43755da0-df71-45cc-965b-7a009dd1c7ad" width="250"/>
  <img src="https://github.com/user-attachments/assets/f29f54d1-6ec4-461e-b56e-db647bbe9a7e" width="250"/>
</p>


#### Quantinuum H2:

<p align="center">
  <img src="https://github.com/user-attachments/assets/45a4a8f6-a5d7-4c6c-a889-0210b060bf25" width="250"/>
  <img src="https://github.com/user-attachments/assets/49abb699-0753-4ef1-a627-774f85be0d29" width="250"/>
  <img src="https://github.com/user-attachments/assets/84ee411c-6fe5-4397-8bcb-68f12542bb49" width="250"/>
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/27db3e51-2f66-4ea2-ba34-ede9ef3f8c0b" width="250"/>
  <img src="https://github.com/user-attachments/assets/44c46519-ed70-42d7-a1cd-8209bb556662" width="250"/>
  <img src="https://github.com/user-attachments/assets/bd084be0-cca1-4db1-9849-211fa0157c3a" width="250"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/7e84141d-c606-45ec-980d-8c8f6db576bb" width="250"/>
  <img src="https://github.com/user-attachments/assets/f2078fb4-3c31-4ade-b7a1-4b1ff8efef66" width="250"/>
  <img src="https://github.com/user-attachments/assets/31e29409-218d-4d11-9507-7ebbc0ad15d7" width="250"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/734eb572-3e06-4352-b80a-4ec5c828a4ad" width="250"/>
  <img src="https://github.com/user-attachments/assets/fa0bc544-b936-4d74-8137-2612f6127577" width="250"/>
  <img src="https://github.com/user-attachments/assets/c9abef3d-ac92-4fbb-bec5-3031a51c68d0" width="250"/>
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/092bdab8-870e-467c-b71a-076bff06f2c2" width="250"/>
  <img src="https://github.com/user-attachments/assets/0c04a477-10ce-42f5-8b0b-37cb980968f5" width="250"/>
  <img src="https://github.com/user-attachments/assets/d00dbd8b-eeef-4564-80c3-4d62c6afaec5" width="250"/>
</p>


#### IBM Boston:

<p align="center">
  <img src="https://github.com/user-attachments/assets/9a9e0a14-de9a-482c-8394-0da0dd308f78" width="250"/>
  <img src="https://github.com/user-attachments/assets/1f51bcf1-7862-4bb9-9497-7ed90e532f51" width="250"/>
  <img src="https://github.com/user-attachments/assets/a211a5ad-facf-442c-a110-558dccf7827d" width="250"/>
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/308910e7-3d59-4cd6-8bb9-75e02df890b0" width="250"/>
  <img src="https://github.com/user-attachments/assets/46772ab1-66e6-4add-9e54-3c3c9018cbd3" width="250"/>
  <img src="https://github.com/user-attachments/assets/15d98aa2-0b0c-4a53-a99e-f3435b8d159c" width="250"/>
</p>


<p align="center">
  <img src="https://github.com/user-attachments/assets/c4cd381b-d10a-4f47-ab10-baea0ec3474f" width="250"/>
  <img src="https://github.com/user-attachments/assets/694f92dc-3122-4381-b95e-d289ac3482ac" width="250"/>
  <img src="https://github.com/user-attachments/assets/576cfe1b-a00b-4248-bcf6-1f94368710b1" width="250"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/7ac9fb0e-832f-45c8-a937-d08ab2514700" width="250"/>
  <img src="https://github.com/user-attachments/assets/b1e4cafd-570b-47f0-91a5-daa58d6bdfc1" width="250"/>
  <img src="https://github.com/user-attachments/assets/ac256ed8-eff9-457a-a4b5-f24a8c64f144" width="250"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/1ab894e0-92bf-4fd1-a216-2230a7a4be56" width="250"/>
  <img src="https://github.com/user-attachments/assets/df2ea1f0-db87-4025-a23b-0cd1fa0c9e51" width="250"/>
  <img src="https://github.com/user-attachments/assets/c8523f24-8d5f-452d-8385-0569ed2822dc" width="250"/>
</p>

---

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

---

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

- Generate **13** test quantum states
- Utilise **9** observables
- Perform **10000** shots per configuration
- Generate fingerprint matrices for **2** platforms: Qiskit and Cirq
- Compute cross-platform Frobenius distances between fingerprints
- Run physics-informed noise channel classification and parameter estimation
- Save timestamped results to `results/simshadow_results_*.json` and detailed logs to `logs/`

**6. Generate figures from the latest results**

TODO: Vasilis, can you fix 6-7 documentation?

```bash
python Documentation/gen_figures.py 2>&1 | grep -v "UserWarning"
```

This creates:

- `figures/figure2_fingerprints.pdf` (Figure 2 from the paper)
- `figures/figure3_scaling.pdf` (Figure 3 from the paper)

To reproduce multiple (for, e.g., three) independent runs:

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

- **2808 measurements each with 10000 shots** across 13 states, 9 observables, 3 noise types, 4 noise configurations, 2 platforms
- **28,080,000 quantum shots** with real Qiskit and Cirq execution
- **Cross-platform distances** (Frobenius norms between platforms)
- **Performance metrics** (execution times, throughput)
- **1000 Repeats** to achieve statistical confidance
  
**Figures:**

Figures are the mean of 1000 repeats per noise type, noise configuration and platform (1000 repeats of 24 experiments)

TODO: Vasilis, we need to fix the figures and results text/code.
- **Figure 2**: Fingerprint visualizations showing noise patterns
- **Figure 3**: Scaling comparison (SimSHADOW vs Process Tomography)

**Results:**

- JSON files with complete experimental data
- Text reports with human-readable summaries
- Log files with detailed execution traces

---

### Step-by-Step Process

**1. Test Suite Design**

- **13 quantum states**: 4 computational basis states (|00⟩, |01⟩, |10⟩, |11⟩), 8 superposition states (|+0⟩, |-0⟩, |0+⟩, |0-⟩, |+1⟩, |-1⟩, |1+⟩, |1-⟩), and 1 entangled state (|GHZ⟩)
- **9 Pauli observables**: 9 two-qubit observables (XX, XY, XZ, YX, YY, YZ, ZX, ZY, ZZ)

**2. For Each State-Observable Pair (13 × 9 = 117 measurements per platform):**

   **a) Noisy Measurement:**
   
   - Prepare the quantum state on the simulator
   - Apply the configured noise model (depolarizing, amplitude damping, or phase damping)
   - Rotate into the appropriate Pauli basis for the observable
   - Measure the observable using 10000 quantum shots
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

- A 13×9 matrix per platform per noise type
- Each entry quantifies how noise affects that specific state-observable combination
- Patterns in the matrix reveal noise characteristics and platform differences

**4. Cross-Platform Comparison:**

- Compute Frobenius distance between Qiskit and Cirq fingerprints
- Large distances indicate implementation differences between platforms


### Why This Works

- Different noise types affect states/observables in distinct ways
- Each platform implements noise models with slight variations
- The fingerprint matrix captures these systematic differences quantitatively


----
TODO: Check from this point on:
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
