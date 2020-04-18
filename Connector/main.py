import time
from NewsLoader import NewsLoader

def main():
    loader = NewsLoader()
    while True:
        loader.load()
        loader.save_csv()
        loader.save_json()
        time.sleep(1000)

if __name__ == '__main__':
    main()