cd /opt/TESTaLOD/inferenceServices

echo "serverPort=$2" > src/main/resources/config.properties

cat src/main/resources/config.properties

mvn exec:java -Dexec.mainClass="it.cnr.istc.stlab.testalod.TestaLODServer"