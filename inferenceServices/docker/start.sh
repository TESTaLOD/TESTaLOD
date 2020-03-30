cd /opt/TESTaLOD/inferenceServices

echo "serverPort=$1" > src/main/resources/config.properties

cat src/main/resources/config.properties

mvn clean install

mvn exec:java -Dexec.mainClass="it.cnr.istc.stlab.testalod.TestaLODServer"