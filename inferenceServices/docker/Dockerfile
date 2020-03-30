FROM openjdk:8-alpine

RUN apk add curl && \
	curl -OL https://www.dropbox.com/s/pssf870uxnwern2/inference-service-0.0.1.jar


CMD java -jar inference-service-0.0.1.jar $PORT
