import docker
from docker.errors import NotFound, APIError, ImageNotFound
import time
import requests
import os
import sys


class Setup():
    def __init__(self, tag, **kwargs):

        self.repo = '192.168.70.210:5000'
        self.image_name_server = '{}/ppw-server:{}'.format(self.repo, tag)
        self.container_name_server = '{}/ppw-server-{}'.format(self.repo, tag)

        self.image_name_connector = '{}/ppw-connector:{}'.format(self.repo, tag)
        self.container_name_connector = '{}/ppw-connector-{}'.format(self.repo, tag)

        self.image_name_ml_controller = '{}/ppw-ml-controller:{}'.format(self.repo, tag)
        self.container_name_ml_controller = '{}/ppw-ml-controller-{}'.format(self.repo, tag)

        self.client = docker.from_env()

        if kwargs:
            self.username = kwargs['username']
            self.password = kwargs['password']

    def get_image_full_name(self, name):
        return {
            'server': self.image_name_server,
            'connector': self.image_name_connector,
            'ml-controller': self.image_name_ml_controller,
        }.get(name, lambda: None)

    def get_container_full_name(self, name):
        return {
            'server': self.container_name_server,
            'connector': self.container_name_connector,
            'ml-controller': self.container_name_ml_controller,
        }.get(name, lambda: None)

    def build_image(self, name):
        image_name = self.get_image_full_name(name)
        if self.client.images.list(name=image_name):
            try:
                self.client.containers.get(self.get_container_full_name(name))
            except NotFound as e:
                print(e)
            else:
                self.remove_container(name)
            self.remove_image(name)

        self.client.images.build(path='./server/', tag=image_name)
        print("Image {} created".format(image_name))

    def run_container(self, name):
        try:
            container = self.client.containers.run(self.get_image_full_name(name), detach=True, ports={'666': 666}, name=self.get_container_full_name(name))
        except ImageNotFound as e:
            print(e)
        else:
            print("Container {} created".format(container.name))

    def remove_container(self, name):
        try:
            container = self.client.containers.get(self.get_container_full_name(name))
            container.remove(force=True)
        except NotFound as e:
            print(e)
        else:
            print("Container {} removed".format(container.name))

    def remove_image(self, name):
        try:
            image = self.client.images.get(self.get_image_full_name(name))
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

    def push_image(self, name):
        try:
            image_name = self.get_image_full_name(name)
            # images = self.client.images.get(self.get_image_full_name(name))
            self.client.images.push('{}'.format(image_name), auth_config={'username': self.username,
                                                                          'password': self.password})
        except NotFound as e:
            print(e)
            self.build_image(name)
            self.push_image(name)

        else:
            print("Image {} pushed".format(image_name))


if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    print(username, password)
    obj = Setup(1, username=username, password=password)
    # print(obj.get_image_full_name('server'))
    # print(obj.get_container_full_name('server'))
    obj.build_image('server')
    # obj.push_image('server')
    # obj.run_container('server')
    # time.sleep(120)
    # # print(requests.get('https://api.github.com').status_code)
    # # os.system("docker ps")
    # for i in range(1, 7):
    #     try:
    #         print(requests.get('http://192.168.70.21{}:666/v1'.format(i)).status_code)
    #     except Exception as e:
    #         print('i = {} упало'.format(i))
    #
    # try:
    #     print(requests.get('http://192.168.70.211:31511/v1/scopes').status_code)
    # except Exception as e:
    #     print('упало')
    # obj.remove_container('server')
    # print(os.environ["GIT_COMMIT"])
    obj.remove_image('server')

