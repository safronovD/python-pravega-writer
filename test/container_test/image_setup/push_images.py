import os
import sys
from test.container_test.image_setup.container_setup import ContainerSetup

if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    tag = sys.argv[3]
    if sys.argv[4]:
        repo = sys.argv[4]
    else:
        repo = '192.168.70.210:5000'
    # os.environ["GIT_COMMIT"] tag
    obj = ContainerSetup(tag, username=username, password=password, repo=repo)

    obj.build_image('server')
    obj.push_image('server')
    obj.remove_image('server')

    obj.build_image('processor')
    obj.push_image('processor')
    obj.remove_image('processor')

    obj.build_image('ml-controller')
    obj.push_image('ml-controller')
    obj.remove_image('ml-controller')
