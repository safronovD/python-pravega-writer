import logging
import logging.config
import os

import yaml


def init_logger(*args):
    name = 'logger_config.yaml'
    path_to_config_file = find_path(name, '.')

    with open(path_to_config_file, 'r') as file:
        log_cfg = yaml.safe_load(file.read())
    logging.config.dictConfig(log_cfg)

    if args:
        return logging.getLogger(args[0])
    return logging.getLogger()


def find_path(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
