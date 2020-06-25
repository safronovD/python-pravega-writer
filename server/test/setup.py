import docker


class Setup():
    def __init__(self, tag):
        self.tag = 'ppw-server:{}'.format(tag)

    def build_image(self):
        client = docker.from_env()
        client.images.build(path='./server/', tag=self.tag)
        print("Image {} created".format(self.tag))

    def run_container(self):
        client = docker.from_env()
        if client.containers.list():
            print(client.containers.list())
            # self.remove_container()
        container = client.containers.run(self.tag, detach=True, ports={'666': 666}, name=self.tag[0:10])
        print("Container {} created".format(container.name))

    def remove_container(self):
        client = docker.from_env()
        container = client.containers.get(self.tag[0:10])
        container.kill()
        print("Container {} stopped".format(container.name))
        client.containers.prune()
        print("Container {} removed".format(container.name))

    def remove_image(self):
        client = docker.from_env()
        image = client.images.get(self.tag)
        tag = image.tags[0]
        client.images.remove(tag)
        print("Image {} removed".format(tag))


if __name__ == "__main__":
    obj = Setup(123)
    obj.build_image()
    obj.run_container()
    obj.remove_container()
    obj.remove_image()