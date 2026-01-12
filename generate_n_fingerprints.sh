n=$1 # how many fingerprints to generate for the statistical analysis later
for i in $(seq 1 $n); do
  echo ">> Executing run $i at $(date)"
  SIMSHADOW_RUN_ID=$i python run_simshadow.py > logs/run_$i.log 2>&1
done
