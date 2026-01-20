simPath=$1 # Abs. path to run_simshadow script (main entry)
n=$2 # how many fingerprints to generate for the statistical analysis later

mkdir $simPath/results/
for i in $(seq 1 $n); do
  echo ">> Executing run $i at $(date)"
  SIMSHADOW_RUN_ID=$i python $simPath/run_simshadow.py > logs/run_$i.log 2>&1
done
