import docker
from docker.errors import NotFound, APIError, ImageNotFound

# TODO: Спросить у Феди про имена контейнеров


class Setup():
    def __init__(self, tag):
        self.name_for_image = 'ppw-server:{}'.format(tag)
        self.name_for_container = 'ppw-server_{}'.format(tag)
        self.client = docker.from_env()

    def build_image(self):
        if self.client.images.list(name=self.name_for_image):
            try:
                self.client.containers.get(self.name_for_container)
            except NotFound as e:
                print(e)
            else:
                self.remove_container()
            self.remove_image()

        self.client.images.build(path='./server/', tag=self.name_for_image)
        print("Image {} created".format(self.name_for_image))

    def run_container(self):
        try:
            container = self.client.containers.run(self.name_for_image, detach=True, ports={'666': 666}, name=self.name_for_container)
        except ImageNotFound as e:
            print(e)
        else:
            print("Container {} created".format(container.name))

    def remove_container(self):
        try:
            container = self.client.containers.get(self.name_for_container)
            container.remove(force=True)
        except NotFound as e:
            print(e)
        else:
            print("Container {} removed".format(container.name))

    def remove_image(self):
        try:
            image = self.client.images.get(self.name_for_image)
            tag = image.tags[0]
            self.client.images.remove(tag)
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
