#!/usr/bin/env bash
simPath=$1 # Abs. path to run_simshadow script (main entry)
n=$2 # how many fingerprints to generate for the statistical analysis later
noise=$3

cd $simPath
pathFull=`pwd`

echo ">> Executing $n repeats of run_simshadow.py with noise configuration $noise"
mkdir -p $pathFull/results/
mkdir -p $pathFull/logs/
for i in $(seq 1 $n); do
  echo ">> Executing run $i at $(date)"
  SIMSHADOW_RUN_ID=$i python $pathFull/run_simshadow.py --noise-profile $noise --debug > logs/run_$i.log 2>&1
done
mv $pathFull/results/ $pathFull/results-$n-$noise/
mv $pathFull/logs/ $pathFull/logs-$n-$noise/
echo ">> DONE ($n, $noise)"
echo "..."

