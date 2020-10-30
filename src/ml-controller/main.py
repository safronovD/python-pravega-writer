"""Module for train and save ml-model."""
import os

from core.DataSetLoader import CSVDataSetLoader
from core.ModelTrainer import ModelTrainer
from log.logger import init_logger
import yaml

CONFIG_FILE = 'config.yaml'


def load(config_data, logger):
    """Load config and run module."""

    if config_data['loader']['type'] == 'csv':
        CSVDataSetLoader.load(
            config_data['loader']['csv_loader']['link'],
            config_data['common_dir'],
            config_data['dataset']['file_name'])

    logger.info('Dataset is loaded and saved in %s',
                os.path.join(config_data['common_dir'], config_data['dataset']['file_name']))


def train(config_data, logger):
    """Load config. Start trainer."""

    if os.path.exists(os.path.join(config_data['common_dir'], config_data['dataset']['file_name'])) is not True:
        logger.error("Dataset is not found")
    else:
        trainer = ModelTrainer(logger)
        trainer.prepare_data_set(
            config_data['common_dir'],
            config_data['dataset']['file_name'])
        trainer.train(
            config_data['common_dir'],
            config_data['trainer']['model']['model_file'],
            max_df=config_data['trainer']['model']['max_df'],
            min_count=config_data['trainer']['model']['min_count'],
            max_iter=config_data['trainer']['model']['max_iter'])


def main():
    """Load config. Start trainer."""

    logger = init_logger('app')
    logger.info('Start job')

    with open(CONFIG_FILE) as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)
    logger.info('Config is loaded')

    load(config_data, logger)

    train(config_data, logger)


if __name__ == '__main__':
    main()
