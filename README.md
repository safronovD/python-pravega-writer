# python-pravega-writer

## Standalone run

To build the image:

```bash
docker build -t ppw-connector -f ./src/connector/Dockerfile ./src
docker build -t ppw-ml-controller -f ./src/ml-controller/Dockerfile ./src
docker build -t ppw-server -f ./src/server/Dockerfile ./src
```

To run the container:

```bash
docker run -v ${Path_to_your_dir}:/usr/src/app/data/ ppw-connector
docker run -v ${Path_to_your_dir}:/usr/src/app/data/ ppw-ml-controller
docker run -v ${Path_to_your_dir}:/usr/src/app/data/ -p 666:666 ppw-server
```

## Deploy in k8s

!!! Please, check all manifests and values.yaml first.

With kubectl:

```bash
kubectl install -f /deploy
```

With helm:

```bash
helm install ppw /ppw-chart
```

## Code-style

Code-style standard - PEP 8. Link: https://www.python.org/dev/peps/pep-0008/

Linter - PyLint

## Other Links

Dataset for ML training: https://www.kaggle.com/kazanova/sentiment140