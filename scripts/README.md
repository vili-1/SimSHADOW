# Scripts for the evaluation of the paper

This code will generate the six figures for RQ1 and RQ2.

## Install
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12
whereis python3.12 10
| /usr/bin/python3.12 ## for example
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1
sudo update-alternatives --config python

sudo apt-get install python3.12-venv
python3.12 -m venv ~/.venv/mypythonapp
source ~/.venv/mypythonapp/bin/activate
sudo apt install nano unzip
```
Then pull the SimShadow repository:
```
cd SimSHADOW_artifact-main/
pip install -r requirements.txt
pip install openfermion
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
pip install qiskit_qasm3_import
pip install --quiet ply
pip install -e .
```
At this point, all requirements and SimShadow are installed.

## Execute
From the root of the project run:
```
./scripts/generate_n_fingerprints.sh <ROOT-FOLDER-OF-THIS-PROJECT> <REAPEATS>
```
For example:
```
nohup ./scripts/generate_n_fingerprints.sh /users/kevenmen/SimSHADOW_artifact-main 1000 > all_16012026.log 2>&1 &
```

## HeatMaps
From a machine with a GUI, run:
```
python3 scripts/generated_heatmap_presentaion.py
```
