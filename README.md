# python-pravega-writer

## Usage

To build the image:

```bash
docker build . -t pravega-writer
```

To run the container:

```bash
 docker run -v {$Path_to_your_dir}:/usr/src/app/results/ pravega-writer
```

To deploy in k8s:

```bash
 kubectl install -f deployment.yaml
```
