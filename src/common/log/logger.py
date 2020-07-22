import logging
import logging.config
import yaml
import os


def init_logger(*args):
    if args[0] == 'ci':
        with open('./src/common/log/logger_config.yaml', 'r') as f:
            log_cfg = yaml.safe_load(f.read())
    elif args[0] == 'app':
        with open('./log/logger_config.yaml', 'r') as f:
            log_cfg = yaml.safe_load(f.read())
    logging.config.dictConfig(log_cfg)

    return logging.getLogger(args[0])

