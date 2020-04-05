from newsapi import NewsApiClient
import json
import sys
import csv
import os

class NewsLoader():

    def __init__(self):
        with open("news_credentials.json", "r") as file:
            creds = json.load(file)
       
        self.newsapi = NewsApiClient(creds['API_KEY'])
        self.articles = []
        self.resultsDir = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'results')

    def __check_correct_load(self):
        if not isinstance(self.articles, list):
            print("Loading failed. Try again")
            return 0

        if len(self.articles) == 0:
            print("Loaded array is empty. Try again")
            return 0
        
        if not isinstance(self.articles[0], dict):
            print("Loaded array is corrupted. Try again")
            return 0

        return 1

    def load(self):
        try:
            self.articles = self.newsapi.get_everything(q='k8s')['articles']
        except:
            print("Unexpected error:", sys.exc_info())

        self.__check_correct_load()
        print("{} articles loaded".format(len(self.articles)))

    def save_csv(self, fileName='news.csv'):
        if not self.__check_correct_load():
            return

        csv_columns = self.articles[0].keys()
            
        try:
            with open(os.path.join(self.resultsDir, fileName), 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for article in self.articles:
                    writer.writerow(article)

            print("{} articles saved in {}".format(len(self.articles), fileName))

        except:
            print("Unexpected error:", sys.exc_info())

    def save_json(self, fileName='news.json'):
        if not self.__check_correct_load():
            return

        try:
            with open(os.path.join(self.resultsDir, fileName), 'w') as jsonfile:
                json.dump(self.articles, jsonfile)

            print("{} articles saved in {}".format(len(self.articles), fileName))
    
        except:
            print("Unexpected error:", sys.exc_info())
