# SHADOWP: Live Noise Fingerprinting in Quantum Software Engineering

SHADOWP provides systematic validation of quantum simulators through a lightweight, shadow-inspired fingerprinting protocol, enabling efficient cross-platform comparison and noise characterisation without full state tomography.


## Artifact & Reproducibility

This repository is the artifact for the paper *Toward Live Noise Fingerprinting in Quantum Software Engineering*.

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


### Experimental Setup Documentation

**Test States (13):**

- 4 computational basis states: |00⟩, |01⟩, |10⟩, |11⟩
- 8 superposition states: |+0⟩, |-0⟩, |0+⟩, |0-⟩, |+1⟩, |-1⟩, |1+⟩, |1-⟩  
- 1 entangled state: |Φ⁺⟩ Bell state (for 2 qubits)

**Observables (9 per state):**

- 9 two-qubit Pauli observables: XX, XY, XZ, YX, YY, YZ, ZX, ZY, ZZ

**Noise Types (3):**

- **Depolarizing**: generic “random error” that shrinks the Bloch vector towards the origin (loss of both population + phase information).  
  Qiskit Aer definition: $$E(\rho)=(1-\lambda)\rho + \lambda\,\mathrm{Tr}[\rho]\frac{I}{2^n}$$.  
  Link: https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.depolarizing_error.html

- **Amplitude damping**: energy relaxation (T1-type), i.e. decay $$|1\rangle \rightarrow |0\rangle$$ with strength `param_amp`.  
  Qiskit Aer Kraus form and parameter definition:  
  Link: https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.amplitude_damping_error.html

- **Phase damping**: pure dephasing (T2-type), suppresses off-diagonal elements (coherences) while leaving populations largely unchanged; parameter `param_phase`.  
  Qiskit Aer Kraus form and parameter definition:  
  Link: https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.noise.phase_damping_error.html

**Configurations (4) of Noise Types (3):**

- Low Profile
  - Goal: light noise; noticeable degradation without destroying results quickly.

  ```python
  if noise_profile == "low":
      noise_configs = [
          ('depolarizing', DepolarizingChannel(5e-4)),
          ('amplitude_damping', AmplitudeDampingChannel(1e-4)),
          ('phase_damping', PhaseDampingChannel(2e-4))
      ]
      logging.info("Noise profile selected: LOW")
  ```
- High Profile
  - Goal: stress-test regime; still far below the extremely aggressive 0.1 defaults.
  
  ```python
  elif noise_profile == "high":
    noise_configs = [
        ('depolarizing', DepolarizingChannel(5e-3)),
        ('amplitude_damping', AmplitudeDampingChannel(2e-3)),
        ('phase_damping', PhaseDampingChannel(5e-3))
    ]
    logging.info("Noise profile selected: HIGH")
  ```
  
  IBM Aer noise simulation guide (context for “high” noise examples):
  [https://quantum.cloud.ibm.com/docs/guides/simulate-with-qiskit-aer](https://quantum.cloud.ibm.com/docs/guides/simulate-with-qiskit-aer)

- Quantinuum H2 Profile
  - Anchors: typical 1Q gate infidelity ~3e-5; memory error at depth-1 ~2e-4 (used as dephasing proxy).
  - Trapped-ion platforms don’t usually present T1/T2 in the same way as superconducting devices; this is an approximate mapping.
  
  ```python
  elif noise_profile == "quantinuum_h2":
    # Quantinuum H2 (typical) from product data sheet
    # 1Q gate infidelity ~3e-5, memory error depth-1 ~2e-4
    noise_configs = [
        ('depolarizing', DepolarizingChannel(6e-5)),          # ~2 * (1Q infidelity) proxy
        ('amplitude_damping', AmplitudeDampingChannel(1e-5)), # small; relaxation not usually dominant proxy here
        ('phase_damping', PhaseDampingChannel(2e-4))          # memory-error-as-dephasing proxy
    ]
    logging.info("Noise profile selected: QUANTINUUM_H2 (datasheet-typical)")
  ```
  
  - [Quantinuum H2 product datasheet (PDF)](https://docs.quantinuum.com/systems/data_sheets/Quantinuum%20H2%20Product%20Data%20Sheet.pdf)

  - [Quantinuum performance validation overview](https://docs.quantinuum.com/systems/user_guide/hardware_user_guide/performance_validation.html)


- IBM Boston Profile
  - Depolarizing parameter is set from a 1Q gate-error proxy (e.g., SX median error).
  - Amplitude/phase damping are set from T1/T2 mapped per ~50 ns 1Q gate step.
  
  ```python
  elif noise_profile == "ibm_boston":
    # IBM Boston 1Q-mapped values (SX error + T1/T2 mapped per ~50ns step)
    noise_configs = [
        ('depolarizing', DepolarizingChannel(2.824e-4)),
        ('amplitude_damping', AmplitudeDampingChannel(1.98e-4)),
        ('phase_damping', PhaseDampingChannel(1.54e-4))
    ]
    logging.info("Noise profile selected: IBM_BOSTON (1Q mapped)")
  ```
  
  - IBM guide (building/using device-like noise models): [https://quantum.cloud.ibm.com/docs/guides/build-noise-models](https://quantum.cloud.ibm.com/docs/guides/build-noise-models)

**Platforms (2):**

- Qiskit AerSimulator
- Cirq DensityMatrixSimulator

**Measurement Protocol:**

- 10000 quantum shots per measurement configuration
- Direct measurement in each observable's eigenbasis (no full classical shadow reconstruction)
- Ideal expectations computed analytically (from theory; no 10k-shot noiseless runs)

### Noise Fingerprints' Results

Each figue states the configuration, split into low, high, IBM profiles etc. 
The first 9 figures are the mean over 1000 repeats of each experiment. The next 9 figures (in Green) are the standard deviation.

_Visualisation note._
Heatmaps use a fixed colour scale in $[-0.002,0.002]$ for readability; values outside this range (e.g., $-0.003$) are clipped and shown at the extreme colour. 
This prevents a small number of outliers from compressing the colour range and obscuring structure in the remaining entries.
Clipping occurs only for the synthetic Low/High profiles; the IBM Boston and Quantinuum H2 results (our main focus) fall within the plotted range.

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

## Replication Package:

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
cd ~/SHADOWP_artifact
```

**3. Activate the experiment environment**

The authors used Python 3.12 in a local virtual environment named `.venv312`:

```bash
source .venv312/bin/activate
```

If you prefer to create your own environment instead:

```bash
python -m venv SHADOWP_env
source SHADOWP_env/bin/activate  # On Windows: SHADOWP_env\Scripts\activate

pip install -r requirements.txt
pip install -e .
```

**4. Reproduce Results**

Follow Sections 5--7 below to generate fresh data, create figures, and verify outputs.

**5. Run the complete experiment (generate fresh data)**

```bash
python run_SHADOWP.py
```

This will:

- Generate **13** test quantum states
- Utilise **9** observables
- Perform **10000** shots per configuration
- Generate fingerprint matrices for **2** platforms: Qiskit and Cirq
- Compute cross-platform Frobenius distances between fingerprints
- Run physics-informed noise channel classification and parameter estimation
- Save timestamped results to `results/SHADOWP_results_*.json` and detailed logs to `logs/`

The New Idea/Vision Paper results repeated the steps above 1000 times to gain statistical confidence, as detailed here [Evaluation_NIER/README.md](Evaluation_NIER/README.md). We add here the parts relevant to EQ1 and EQ2.

***5.1 EQ1 run_SHADOWP.py over many repeats***

#### Execute
From the root of the project run:
```
./Evaluation_NIER/scripts_RQ1/generate_n_fingerprints.sh <ROOT-FOLDER-OF-THIS-PROJECT> <REAPEATS>
```
For example:
```
nohup ./Evaluation_NIER/scripts_RQ1/generate_n_fingerprints.sh /users/kevenmen/SHADOWP_artifact-main 1000 > all_16012026.log 2>&1 &
```

#### HeatMaps
From a machine with a GUI, run:
```
python3 Evaluation_NIER/scripts_RQ1/generated_heatmap_presentaion.py
```
We used this script for quick debugging and visualisation of the results. You will need to edit the path in the script. 
**See Section 6 for the full automation for generating the paper's official figures.**

***5.2 EQ2 Testing Aspects of SHADOWP***
#### Get and Fix the Benchmarking
Download a subset of benchmarks from its scalable benchmarks: [MQT Bench](https://www.cda.cit.tum.de/mqtbench/).

Then use this zip to fix the syntax to work with Cirq:
```
./Evaluation_NIER/scripts_RQ2/openNfix_bench.sh <zip-file-from-mqtbench.zip>
```
Copy the results (unzip fixed QASM files) into 'MQTBench/' folder and run:
```
python3 Evaluation_NIER/scripts_RQ2/RQ2-in-wild.py
```

We utilised these MQTBench benchmarks with qubits 5-11:
```
ghz_indep_tket_*.qasm        
grover-noancilla_indep_tket_*.qasm  
qftentangled_indep_tket_*.qasm  
random_indep_tket_*.qasm        
su2random_indep_tket_*.qasm
graphstate_indep_tket_*.qasm  
qaoa_indep_tket_*.qasm              
qft_indep_tket_*.qasm          
realamprandom_indep_tket_*.qasm  
twolocalrandom_indep_tket_*.qasm
```
(except one of the 11 qubits, which was running for days.)

#### Execute the Benchmarking

**6. Generate figures from the latest results**

Use the artifact plotting entrypoint:

```bash
python -m Documentation.gen_figures
```

This generates:

- `figures/figure2_fingerprints_IBM.pdf`
- `figures/figure2_fingerprints_IBM_QuantinuumH2.pdf`
- `figures/figure3_scaling.pdf`

Notes:

- Figure generation uses the profile means loaded by `Documentation/visualization/plotting.py`.
- Preferred input is the aggregated 1000-run profile data for:
  - IBM Boston
  - Quantinuum H2


To regenerate data + figures for repeated runs:

```bash
for i in 1 2 3; do
  python run_SHADOWP.py
  python -m Documentation.gen_figures
  cp figures/figure2_fingerprints_IBM_QuantinuumH2.pdf figures/figure2_fingerprints_IBM_QuantinuumH2_run${i}.pdf
done
```

**7. Verify expected outputs**

After running Sections 5 and 6, verify files exist:

```bash
ls -1 results/SHADOWP_results_*.json | head -n 3
ls -1 results/SHADOWP_report_*.txt | head -n 3
ls -1 logs/SHADOWP_experiment_*.log | head -n 3
ls -1 figures/figure2_fingerprints_IBM.pdf
ls -1 figures/figure2_fingerprints_IBM_QuantinuumH2.pdf
ls -1 figures/figure3_scaling.pdf
```

Expected artifacts:

- `results/SHADOWP_results_*.json` (experiment outputs)
- `results/SHADOWP_report_*.txt` (human-readable summaries)
- `logs/SHADOWP_experiment_*.log` (execution logs)
- `figures/figure2_fingerprints_IBM.pdf`
- `figures/figure2_fingerprints_IBM_QuantinuumH2.pdf`
- `figures/figure3_scaling.pdf`
- `figures/figure3_scaling.pdf`

For the paper-reported distances and uncertainty as a standalone check, use:

```bash
python -m Documentation.report_frobenius_stats --ibm-runs /path/to/results-1000-ibm_boston --qh2-runs /path/to/results-1000-quantinuum_h2 --bootstrap 2000
```

### What Gets Generated

**Experimental Data:**

- `results/SHADOWP_results_*.json` (raw experiment outputs)
- `results/SHADOWP_report_*.txt` (human-readable summaries)
- `logs/SHADOWP_experiment_*.log` (execution logs)
- Cross-platform metrics (including Frobenius distances) in result JSONs/reports
- Optional analysis outputs (classification/parameter-estimation fields) included in result JSONs

**Figures (from `python -m Documentation.gen_figures`):**

- `figures/figure2_fingerprints_IBM.pdf`
- `figures/figure2_fingerprints_IBM_QuantinuumH2.pdf`
- `figures/figure3_scaling.pdf`

**Results:**

- JSON files with complete experimental data
- Text reports with human-readable summaries
- Log files with detailed execution traces

---

### Step-by-Step Process

**1. Test Suite Design**

- **13 quantum states**: 4 computational basis states (|00⟩, |01⟩, |10⟩, |11⟩), 8 superposition states (|+0⟩, |-0⟩, |0+⟩, |0-⟩, |+1⟩, |-1⟩, |1+⟩, |1-⟩), and 1 entangled state (|Φ⁺⟩ for 2 qubits; GHZ for 3+ qubits).
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

## Validated current configuration and outputs

The sections above describe the current reproducibility path. The canonical settings used by the
artifact workflow are:

- **13** reference states
- **9** Pauli observables
- **10,000** shots per state-observable measurement
- **2** simulator ecosystems (Qiskit, Cirq)
- **2** hardware-informed profiles (IBM Boston, Quantinuum H2)
- **3** noise channels (depolarizing, amplitude damping, phase damping)

Fingerprint entries are defined as:

```text
F[i, j] = E_noisy(state_i, observable_j) - E_ideal(state_i, observable_j)
```

### Figure generation (current)

```bash
python -m Documentation.gen_figures
```

Expected figure outputs:

- `figures/figure2_fingerprints_IBM.pdf`
- `figures/figure2_fingerprints_IBM_QuantinuumH2.pdf`
- `figures/figure3_scaling.pdf`

### Standalone Frobenius and bootstrap check

To reproduce paper-reported Frobenius distances and bootstrap uncertainty from run-level profile files:

```bash
python -m Documentation.report_frobenius_stats \
  --ibm-runs /path/to/results-1000-ibm_boston \
  --qh2-runs /path/to/results-1000-quantinuum_h2 \
  --bootstrap 2000
```

If only mean-profile JSON files are available, the same script reports distance values (without bootstrap SE):

```bash
python -m Documentation.report_frobenius_stats
```
