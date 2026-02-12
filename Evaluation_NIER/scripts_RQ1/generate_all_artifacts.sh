#!/usr/bin/env bash
simPath=$1 # /users/kevenmen/SimSHADOW_artifact-main
cd $simPath
pathFull=`pwd`

# Generate all the fingerprints using 1000 repeats
choices=("default" "low" "high" "ibm_boston" "quantinuum_h2")

for choice in "${choices[@]}"; do
    echo ">>> Generating fingerprints for choice: ${choice}"
    echo "$pathFull/scripts/generate_n_fingerprints.sh $pathFull 1000 $choice"
    $pathFull/scripts/generate_n_fingerprints.sh "$pathFull" 1000 "$choice"
done


