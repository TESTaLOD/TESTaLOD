cd /opt/TESTaLOD/inferenceServices

echo $0

echo $1

echo $2

echo "serverPort=$1" > src/main/resources/config.properties

cat src/main/resources/config.properties

mvn exec:java -Dexec.mainClass="it.cnr.istc.stlab.testalod.TestaLODServer"