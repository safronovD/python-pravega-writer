# python-pravega-writer

## Usage

To build the image:

```bash
docker build . -t pravega-writer
```

To run the container:

```bash
 docker run -v ${Path_to_your_dir}:/usr/src/app/data/ pravega-writer
```

To deploy in k8s from local registry:

```bash
 kubectl install -f /deploy
```


##Code-style

Code-style standard - PEP 8. Link: https://www.python.org/dev/peps/pep-0008/

Linter - PyLint

##Other Links

Dataset for ML training: https://www.kaggle.com/kazanova/sentiment140