"""Data set loader."""

import os

import requests


class CSVDataSetLoader:
    """Implement function for load."""

    @staticmethod
    def load(link, save_dir, file_name):
        """Load ZIP from link in config. Save it as csv."""

        req_response = requests.get(link)

        with open(os.path.join(save_dir, file_name), 'wb') as file:
            file.write(req_response.content)
