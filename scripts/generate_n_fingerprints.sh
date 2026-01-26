simPath=$1 # Abs. path to run_simshadow script (main entry)
n=$2 # how many fingerprints to generate for the statistical analysis later
noise=$3

echo ">> Executing $n repeats of run_simshadow.py with noise configuration $noise"
mkdir $simPath/results/
mkdir $simPath/logs/
for i in $(seq 1 $n); do
  echo ">> Executing run $i at $(date)"
  SIMSHADOW_RUN_ID=$i python $simPath/run_simshadow.py --noise-profile $noise --debug > logs/run_$i.log 2>&1
done
mv $simPath/results/ $simPath/results-$n-$noise/
mv $simPath/logs/ $simPath/logs-$n-$noise/
echo ">> DONE ($n, $noise)"
echo "..."

