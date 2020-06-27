import docker
from docker.errors import NotFound, APIError, ImageNotFound
import time
# TODO: Спросить у Феди про имена контейнеров


class Setup():
    def __init__(self, tag):
        self.image_name = 'ppw-server:{}'.format(tag)
        self.container_name = 'ppw-server_{}'.format(tag)
        self.client = docker.from_env()

    def build_image(self):
        if self.client.images.list(name=self.image_name):
            try:
                self.client.containers.get(self.container_name)
            except NotFound as e:
                print(e)
            else:
                self.remove_container()
            self.remove_image()

        self.client.images.build(path='./server/', tag=self.image_name)
        print("Image {} created".format(self.image_name))

    def run_container(self):
        self.show_all_containers()
        try:
            container = self.client.containers.run(self.image_name, detach=True, ports={'666': 666}, name=self.container_name)
        except ImageNotFound as e:
            print(e)
        else:
            print("Container {} created".format(container.name))
            time.sleep(20)
            self.show_all_containers()

    def remove_container(self):
        try:
            container = self.client.containers.get(self.container_name)
            container.remove(force=True)
        except NotFound as e:
            print(e)
        else:
            print("Container {} removed".format(container.name))

    def remove_image(self):
        try:
            image = self.client.images.get(self.image_name)
            tag = image.tags[0]
            self.client.images.remove(tag)
            self.client.containers.prune()
        except APIError as e:

            print(e)
        else:
            print("Image {} removed".format(tag))

    def show_all_containers(self):

        if self.client.containers.list():
            for c in self.client.containers.list():
                print(c.name)
        else:
            print('The list of containers is empty')


if __name__ == "__main__":
    obj = Setup(123)
    obj.build_image()
    obj.run_container()
    obj.remove_container()
    obj.remove_image()
