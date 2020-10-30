"""Flask server"""
from core.server import server_init, server_start
from log.logger import init_logger

import yaml

CONFIG_FILE = 'config.yaml'


def main():
    """Load config and run flask app."""

    logger = init_logger('app')
    logger.info('Hello from server')

    with open(CONFIG_FILE) as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)

    server_init(config_data)
    server_start()


if __name__ == '__main__':
    main()
