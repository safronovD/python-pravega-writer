import docker
from docker.errors import NotFound, APIError, ImageNotFound
from log.logger import init_logger
import os
import re
import time


class ContainerSetup:
    def __init__(self, tag, **kwargs):

        self.logger = init_logger('dev')

        self.logger.info('Object initialization is started')

        self.repo = '192.168.70.210:5000'
        self.image_name_server = '{}/ppw-server:{}'.format(self.repo, tag)
        self.container_name_server = 'ppw-server-{}'.format(tag)

        self.image_name_connector = '{}/ppw-connector:{}'.format(self.repo, tag)
        self.container_name_connector = 'ppw-connector-{}'.format(tag)

        self.image_name_ml_controller = '{}/ppw-ml-controller:{}'.format(self.repo, tag)
        self.container_name_ml_controller = 'ppw-ml-controller-{}'.format(tag)

        self.client = docker.from_env()

        if kwargs:
            self.username = kwargs['username']
            self.password = kwargs['password']

        self.logger.info('Object initialization is complete')

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
        container_name = self.get_container_full_name(name)

        if self.client.images.list(name=image_name):
            self.logger.warning('Image {} already exists'.format(image_name))
            try:
                self.client.containers.get(self.get_container_full_name(name))
            except NotFound:
                self.logger.info('Container {} not found'.format(container_name))
            else:
                self.logger.info('Old container {} removed'.format(container_name))
            self.remove_image(name)
            self.logger.info('Old image {} removed'.format(image_name))

        try:
            self.logger.info('Attempt to create image {}'.format(image_name))
            self.client.images.build(path='./{}/'.format(name), tag=image_name)
        except NotFound:
            self.logger.error('Dockerfile not found')
            self.logger.exception('Image {} is not created'.format(image_name))
        else:
            self.logger.warning('Image {} is created'.format(image_name))
        #     return 1
        # return 0

    def run_container(self, name):
        container_name = self.get_container_full_name(name)
        try:
            self.logger.info('Attempt to create container {}'.format(container_name))
            container = self.client.containers.run(self.get_image_full_name(name), detach=True, ports={'666': 666},
                                                   name=container_name)
        except ImageNotFound:
            self.logger.error('Image not found')
            self.logger.exception('Container is not created')
        except APIError:
            self.logger.exception('Container {} already exists'.format(container_name))
            self.remove_container(name)
        else:
            self.logger.warning('Container {} is created'.format(container.name))

    def remove_container(self, name):
        container_name = self.get_container_full_name(name)
        try:
            self.logger.info('Attempt to remove container {}'.format(container_name))
            container = self.client.containers.get(container_name)
            container.remove(force=True)
        except NotFound:
            self.logger.exception('Container {} not found'.format(container_name))
        else:
            self.logger.warning("Container {} is removed".format(container.name))

    def remove_image(self, name):
        image_name = self.get_image_full_name(name)
        try:
            self.logger.info('Attempt to remove image {}'.format(image_name))
            tag = self.client.images.get(image_name).tags[0]
            self.client.images.remove(tag)
            self.client.containers.prune()
        except APIError:
            self.logger.exception('Image {} is not removed'.format(image_name))
            self.remove_container(name)
            self.remove_image(name)

        else:
            self.logger.warning("Image {} is removed".format(tag))

    def push_image(self, name):
        image_name = self.get_image_full_name(name)
        try:
            self.logger.info('Attempt to push image {}'.format(image_name))
            self.client.images.push('{}'.format(image_name), auth_config={'username': self.username,
                                                                          'password': self.password})
        except AttributeError:
            # self.logger.exception('Username or password not found')
            self.logger.exception('Image {} is not pushed'.format(image_name))
        except NotFound:
            # self.logger.error('Image {} not found'.format(image_name))
            self.logger.exception('Image {} is not pushed'.format(image_name))

            self.build_image(name)
            self.push_image(name)
        except APIError:
            self.logger.exception('Image {} is not pushed'.format(image_name))
        else:
            self.logger.warning("Image {} is pushed".format(image_name))

    def run_pod(self, name):
        pod_name = self.get_container_full_name(name)
        image_name = self.get_image_full_name(name)
        command = 'kubectl run {} --image={} --port=666 --wait=true'.format(pod_name, image_name)
        self.logger.warning(command)

        answer = os.popen(command).read()
        self.logger.warning(answer)
        self.logger.warning('Pod {} is created')

    def delete_pod(self, name):
        command = 'kubectl delete pod {}'.format(self.get_container_full_name(name))
        self.logger.warning(command)
        answer = os.popen(command).read()
        self.logger.warning(answer)

    def get_pod_ip(self, name):
        command = 'kubectl describe pod {}'.format(self.get_container_full_name(name))
        self.logger.warning(command)
        answer = os.popen(command).read()

        self.logger.warning(answer)
        # with open('./server/test/answer.txt', 'r') as f:
        #     answer = f.read()
            # print(answer)
        match = re.findall(r'IP:\s+(\d{2,3}.\d{2,3}.\d{2,3}.\d{2,3})', answer)
        if match:
            self.logger.warning(match[0])
            return match[0]

    def get_pod(self, name):
        command = 'kubectl get pod {}'.format(self.get_container_full_name(name))
        self.logger.warning(os.popen(command).read())


if __name__ == "__main__":

    obj = ContainerSetup(os.environ["GIT_COMMIT"])
    # obj.build_image('server')
    # obj.push_image('server')
    # obj.run_container('server')
    # obj.remove_container('server')
    obj.run_pod('server')
    for _ in range(10):
        obj.get_pod('server')
        time.sleep(2)
    time.sleep(20)
    obj.get_pod_ip('server')
    obj.delete_pod('server')
    # obj.remove_image('server')
    #
    # obj.build_image('connector')
    # # obj.push_image('connector')
    # obj.remove_image('connector')
    #
    # obj.build_image('ml-controller')
    # obj.run_container('ml-controller')
    #
    # # obj.push_image('ml-controller')
    # obj.remove_image('ml-controller')
