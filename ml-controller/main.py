import logging
import yaml
from core.ModelTrainer import ModelTrainer

CONFIG_FILE = 'config.yaml'


def main():
    with open(CONFIG_FILE) as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)

    trainer = ModelTrainer()
    trainer.get_data_set(config_data['common_dir'],
                         config_data['dataset']['file_name'],
                         config_data['dataset']['data_col'],
                         config_data['dataset']['label_col'])
    trainer.train(config_data['common_dir'],
                  config_data['model']['model_file'],
                  max_df=config_data['model']['max_df'],
                  min_count=config_data['model']['min_count'],
                  max_iter=config_data['model']['max_iter'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
