# Inference Services

### Build

From ``docker'' folder

```
docker build . --no-cache -t inference_services
```


### Run

```
docker run --name inference_services -p 8080:8080 -e PORT=8080 inference_services
```

At this point the server will be listening on port 8080.
The REST services responds to GET requests on path ``/consistencyCheck''.
It accepts the IRI of a test-case as parameter.
You can simply test the service by accessing the following URL with you browser 
[http://localhost:8080/consistencyCheck?IRI=https://raw.githubusercontent.com/ICCD-MiBACT/ArCo/master/ArCo-release/test/VI/testcase-01.owl](http://localhost:8080/consistencyCheck?IRI=https://raw.githubusercontent.com/ICCD-MiBACT/ArCo/master/ArCo-release/test/VI/testcase-01.owl).
