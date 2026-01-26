path=$1 # /users/kevenmen/SimSHADOW_artifact-main

# Generate all the fingerprints using 1000 repeats
choices=("default" "low" "high" "ibm_boston")

for choice in "${choices[@]}"; do
    echo ">>> Generating fingerprints for choice: ${choice}"
    ./scripts/generate_n_fingerprints.sh "$path" 1000 "$choice"
done


