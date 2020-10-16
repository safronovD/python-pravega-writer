"""Connector module."""

import yaml


CONFIG_FILE = 'config.yaml'


def main():
    """Load config and run module."""

    with open(CONFIG_FILE) as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)


if __name__ == '__main__':
    main()
