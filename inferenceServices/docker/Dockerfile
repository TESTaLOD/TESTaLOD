FROM maven:3.6.3-jdk-8


RUN cd /opt && \
	git clone https://github.com/luigi-asprino/TESTaLOD.git  && \
	cd /opt/TESTaLOD/inferenceServices  && \
	mvn clean install

EXPOSE 8080


# mvn exec:java -Dexec.mainClass="it.cnr.istc.stlab.ecodigit.entitylinking.EcodigitServer" -Dexec.args="/opt/entitylinking/config.properties"

CMD /bin/bash /opt/TESTaLOD/inferenceServices/docker/start.sh $PORT
