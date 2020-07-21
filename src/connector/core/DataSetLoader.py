"""Data set loader."""

import os
import zipfile
import requests


class DataSetLoader:
    """Implement function for load."""

    def __init__(self):
        pass

    @staticmethod
    def load_and_save(link, save_dir, file_name, zip_file_name='dataset.zip'):
        """Load ZIP from link in config. Save it as csv."""

        rea_response = requests.get(link)

        with open(os.path.join(save_dir, zip_file_name), 'wb') as file:
            file.write(rea_response.content)

        with zipfile.ZipFile(os.path.join(save_dir, zip_file_name), 'r') as zip_ref:
            for file in zip_ref.namelist():
                zip_ref.extract(file, save_dir)
                os.rename(os.path.join(save_dir, file), os.path.join(save_dir, file_name))
