import docker
from docker.errors import APIError, ImageNotFound, NotFound

from src.common.log.logger import init_logger


class ContainerSetup:
    def __init__(self, tag, repo,  **kwargs):

        self.logger = init_logger('ci')

        self.logger.info('Object initialization is started')

        self.image_name_server = '{}/ppw-server:{}'.format(repo, tag)
        self.container_name_server = 'ppw-server-{}'.format(tag)

        self.image_name_connector = '{}/ppw-connector:{}'.format(repo, tag)
        self.container_name_connector = 'ppw-connector-{}'.format(tag)

        self.image_name_ml_controller = '{}/ppw-ml-controller:{}'.format(repo, tag)
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
            self.client.images.build(path='./src', tag=image_name, dockerfile='./{}/Dockerfile'.format(name))
        except NotFound:
            self.logger.error('Dockerfile not found')
            self.logger.exception('Image {} is not created'.format(image_name))
        except TypeError:
            self.logger.exception('Error!')
        else:
            self.logger.info('Image {} is created'.format(image_name))

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
            self.logger.info('Container {} is created'.format(container.name))

    def remove_container(self, name):
        container_name = self.get_container_full_name(name)
        try:
            self.logger.info('Attempt to remove container {}'.format(container_name))
            container = self.client.containers.get(container_name)
            container.remove(force=True)
        except NotFound:
            self.logger.exception('Container {} not found'.format(container_name))
        else:
            self.logger.info("Container {} is removed".format(container.name))

    def remove_image(self, name):
        image_name = self.get_image_full_name(name)
        try:
            self.logger.info('Attempt to remove image {}'.format(image_name))
            tag = self.client.images.get(image_name).tags[0]
            self.client.images.remove(tag)
            self.client.containers.prune()
        except APIError:
            self.logger.exception('Image {} is not removed'.format(image_name))
            # self.remove_container(name)
            # self.remove_image(name)

        else:
            self.logger.info("Image {} is removed".format(tag))

    def show_all_containers(self):

        if self.client.containers.list():
            for id, item in enumerate(self.client.containers.list()):
                print('{}-{}'.format(id, item.name))
        else:
            print('The list of containers is empty')

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
            self.logger.info("Image {} is pushed".format(image_name))


if __name__ == "__main__":

    obj = ContainerSetup(123)
    obj.build_image('server')
    # obj.push_image('server')
    obj.run_container('server')
    obj.remove_container('server')
    obj.remove_image('server')
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
