FROM maven:3.6.3-jdk-8


RUN cd /opt && \
	git clone https://github.com/luigi-asprino/TESTaLOD.git  && \
	cd /opt/TESTaLOD/inferenceServices  && \
	mvn clean install


CMD /bin/bash /opt/TESTaLOD/inferenceServices/docker/start.sh $PORT
