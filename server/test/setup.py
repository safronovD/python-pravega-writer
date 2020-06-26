import docker


def build_image():
    client = docker.from_env()
    tag = "pravega-writer:latest"
    client.images.build(path='../', tag=tag)
    print("Image {} created".format(tag))


def run_container():
    client = docker.from_env()
    if client.containers.list():
        remove_container()
    container = client.containers.run("pravega-writer:latest", detach=True, ports={'666': 666}, name='pravega-writer')
    print("Container {} created".format(container.name))


def remove_container():
    client = docker.from_env()
    container = client.containers.get("pravega-writer")
    container.kill()
    print("Container {} stopped".format(container.name))
    client.containers.prune()
    print("Container {} removed".format(container.name))


def remove_image():
    client = docker.from_env()
    image = client.images.get("pravega-writer:latest")
    tag = image.tags[0]
    client.images.remove(tag)
    print("Image {} removed".format(tag))


if __name__ == "__main__":
    build_image()
    run_container()
    remove_container()
    remove_image()
