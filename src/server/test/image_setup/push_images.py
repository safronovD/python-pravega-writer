import os
import sys
from src.server.test.image_setup.container_setup import ContainerSetup

if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]

    obj = ContainerSetup(os.environ["GIT_COMMIT"], username=username, password=password)
    obj.build_image('server')
    obj.push_image('server')
    obj.remove_image('server')

    obj.build_image('connector')
    obj.push_image('connector')
    obj.remove_image('connector')

    obj.build_image('ml-controller')
    obj.push_image('ml-controller')
    obj.remove_image('ml-controller')