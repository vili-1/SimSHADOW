zipname=$1
mkdir MQTBench
cd MQTBench
unzip ../$zipname
sed -i "s:barrier://barrier:g" *
sed -i "s:creg c://creg c:g" *
