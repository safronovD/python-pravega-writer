from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss, f1_score
from pandas import read_csv
import logging
import pickle
import os


class ModelTrainer:
    def __init__(self):
        self.data_train = []
        self.data_test = []
        self.label_train = []
        self.label_test = []

    def get_data_set(self,  dir, data_set_file, data_col, label_col, test_size=0.05):
        dataset = read_csv(os.path.join(dir, data_set_file), encoding="ISO-8859-1", engine='python', header=None)

        logging.info('Dataset loaded')
        logging.info('Dateset len: {0}'.format(len(dataset)))

        dataset_train, dataset_test = train_test_split(dataset, test_size=test_size)
        self.data_train = dataset_train.iloc[:, data_col]
        self.data_test = dataset_test.iloc[:, data_col]
        self.label_train = dataset_train.iloc[:, label_col]
        self.label_test = dataset_test.iloc[:, label_col]

    def train(self, dir, model_file, max_df=0.8, min_count=5, max_iter=10000):
        sklearn_pipeline = Pipeline((('vec', TfidfVectorizer(max_df=max_df,
                                                              min_df=min_count)),
                                     ('cls', LogisticRegression(max_iter=max_iter))))

        sklearn_pipeline.fit(self.data_train, self.label_train)
        logging.info('Regressor trained')

        sklearn_train_pred = sklearn_pipeline.predict(self.data_train)
        sklearn_train_loss = log_loss(self.label_train, sklearn_train_pred)
        logging.info('train log_less: {0}'.format(float(sklearn_train_loss)))
        logging.info(
            'train f1: {0}'.format(f1_score(self.label_train, sklearn_train_pred, pos_label=0)))

        sklearn_test_pred = sklearn_pipeline.predict(self.data_test)
        sklearn_test_loss = log_loss(self.label_test, sklearn_test_pred)
        logging.info('test log_less: {0}'.format(float(sklearn_test_loss)))
        logging.info(
            'test f1: {0}'.format(f1_score(self.label_test, sklearn_test_pred, pos_label=0)))

        logging.info('Predict for [i hate everyone]: {0}'.format(sklearn_pipeline.predict(['i hate you'])))

        pickle.dump(sklearn_pipeline, open(os.path.join(dir, model_file), 'wb'))