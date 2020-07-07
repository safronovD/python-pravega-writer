import logging
from os import path, remove


def init_logger():
    logger = logging.getLogger()
    filename = './log/logging.log'

    if path.isfile(filename):
        remove(filename)

    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename)
    stream_handler = logging.StreamHandler()

    file_handler.setLevel(logging.INFO)
    stream_handler.setLevel(logging.WARNING)

    file_handler_formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)-8s - %(module)s.%(funcName)s - %(message)s',
                                               datefmt='%Y-%m-%d %H:%M:%S')
    stream_handler_formatter = logging.Formatter(fmt='%(message)s')

    file_handler.setFormatter(file_handler_formatter)
    stream_handler.setFormatter(stream_handler_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
