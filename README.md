# python-pravega-writer

## Standalone run

To build the image:

```bash
docker build -t ppw-ml-controller -f ./src/ml-controller/Dockerfile ./src
docker build -t ppw-processor -f ./src/processor/Dockerfile ./src
docker build -t ppw-server -f ./src/server/Dockerfile ./src
```

To run the container:

```bash
docker run -v ${Path_to_your_dir}:/usr/src/app/data/ ppw-ml-controller
docker run -v ${Path_to_your_dir}:/usr/src/app/data/ ppw-processor
docker run -p 666:666 ppw-server
```

## Deploy in k8s

!!! Please, specify pvc.yaml or StorageClassName in values.yaml first.

With kubectl:

```bash
kubectl apply -f /deploy
```

With helm:

```bash
helm install ppw /ppw-chart
```

## Operator

https://github.com/safronovD/ppw-operator (In progress!!)

## Code-style

Code-style standard - PEP 8. Link: https://www.python.org/dev/peps/pep-0008/

Linter - PyLint

## Other Links

Dataset for ML training: https://www.kaggle.com/kazanova/sentiment140