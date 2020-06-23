import requests
import os
import zipfile


class DataSetLoader:
    def __init__(self):
        pass

    @staticmethod
    def  load_and_save(link, dir, file_name, zip_file_name='dataset.zip'):
        r = requests.get(link)

        with open(os.path.join(dir, zip_file_name), 'wb') as file:
            file.write(r.content)

        with zipfile.ZipFile(os.path.join(dir, zip_file_name), 'r') as zip_ref:
            for file in zip_ref.namelist():
                zip_ref.extract(file, dir)
                os.rename(os.path.join(dir, file), os.path.join(dir, file_name))
