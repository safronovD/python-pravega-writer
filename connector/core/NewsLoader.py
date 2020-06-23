from newsapi import NewsApiClient
import json
import sys
import csv
import os


class NewsLoader():

    def __init__(self, api_key, dir):
        self.newsapi = NewsApiClient(api_key)
        self.articles = []
        self.resultsDir = dir

    def _check_correct_load(self):

        assert isinstance(self.articles, list)
        assert len(self.articles) != 0
        assert isinstance(self.articles[0], dict)

    def load(self):
        try:
            self.articles = self.newsapi.get_everything(q='k8s')['articles']
        except:
            print("Unexpected error:", sys.exc_info())

        self._check_correct_load()
        print("{} articles loaded".format(len(self.articles)))

    def save_csv(self, file_name='news.csv'):
        self._check_correct_load()

        csv_columns = self.articles[0].keys()

        try:
            with open(os.path.join(self.resultsDir, file_name), 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for article in self.articles:
                    writer.writerow(article)

            print("{} articles saved in {}".format(len(self.articles), file_name))

        except:
            print("Unexpected error:", sys.exc_info())

    def save_json(self, fileName='news.json'):
        self._check_correct_load()

        try:
            with open(os.path.join(self.resultsDir, fileName), 'w') as jsonfile:
                json.dump(self.articles, jsonfile)

            print("{} articles saved in {}".format(len(self.articles), fileName))

        except:
            print("Unexpected error:", sys.exc_info())
