import logging
import logging.config
import yaml
import os


def init_logger(*args):

    print(os.listdir(path="./src"))
    print(os.listdir(path="./src/common"))
    print(os.listdir(path="./src/common/log"))
    with open('./src/common/log/logger_config.yaml', 'r') as f:
        log_cfg = yaml.safe_load(f.read())
    logging.config.dictConfig(log_cfg)
    if args:
        return logging.getLogger(args[0])
    return logging.getLogger()
