import yaml
from core.DataSetLoader import DataSetLoader


CONFIG_FILE = 'config.yaml'

def main():
    with open(CONFIG_FILE) as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)

    DataSetLoader.load_and_save(config_data['link'], config_data['common_dir'], config_data['dataset_file'])

if __name__ == '__main__':
    main()
