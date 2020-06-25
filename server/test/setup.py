import docker


class Setup():
    def __init__(self, tag):
        self.name_for_image = 'ppw-server:{}'.format(tag)
        self.name_for_container = 'ppw-server_{}'.format(tag)

    def build_image(self):
        client = docker.from_env()
        client.images.build(path='./server/', tag=self.name_for_image)
        print("Image {} created".format(self.name_for_image))

    def run_container(self):
        client = docker.from_env()
        for c in client.containers.list():
            print(c.name, end='')
            # self.remove_container()
        container = client.containers.run(self.name_for_image, detach=True, ports={'666': 666}, name=self.name_for_container)
        print("Container {} created".format(container.name))

    def remove_container(self):
        client = docker.from_env()
        container = client.containers.get(self.name_for_container)
        container.kill()
        print("Container {} stopped".format(container.name))
        client.containers.prune()
        print("Container {} removed".format(container.name))

    def remove_image(self):
        client = docker.from_env()
        image = client.images.get(self.name_for_image)
        tag = image.tags[0]
        client.images.remove(tag)
        print("Image {} removed".format(tag))


if __name__ == "__main__":
    obj = Setup(123)
    obj.build_image()
    obj.run_container()
    obj.remove_container()
    obj.remove_image()