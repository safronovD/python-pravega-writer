from NewsLoader import NewsLoader

if __name__ == '__main__':
    loader = NewsLoader()
    loader.load()
    loader.save_csv()
    loader.save_json()