# Inference Services

### Build

From ``docker'' folder

```
docker build . --no-cache -t inference_services
```


### Run

Una volta costuito il docker container ``entity_linking'' è possibile lanciare il server con comando.

```
docker run -p8080:8080 inference_services
```
