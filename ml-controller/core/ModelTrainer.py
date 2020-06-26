"""Model trainer."""

import logging
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss, f1_score
from pandas import read_csv


class ModelTrainer:
    """Train and save ml-model. Using tf-idf + logistic regression."""

    def __init__(self):
        self.data_train = []
        self.data_test = []
        self.label_train = []
        self.label_test = []

    def get_data_set(self, common_dir, data_set_file, data_col, label_col, test_size=0.05):
        """Read dataset created by Connector module."""

        dataset = read_csv(os.path.join(common_dir, data_set_file),
                           encoding="ISO-8859-1",
                           engine='python',
                           header=None)

        logging.info('Dataset loaded')
        logging.info('Dataset len: %d', len(dataset))

        dataset_train, dataset_test = train_test_split(dataset, test_size=test_size)
        self.data_train = dataset_train.iloc[:, data_col]
        self.data_test = dataset_test.iloc[:, data_col]
        self.label_train = dataset_train.iloc[:, label_col]
        self.label_test = dataset_test.iloc[:, label_col]

    def train(self, common_dir, model_file, max_df=0.8, min_count=5, max_iter=10000):
        """Train model."""

        sklearn_pipeline = Pipeline((('vec', TfidfVectorizer(max_df=max_df,
                                                             min_df=min_count)),
                                     ('cls', LogisticRegression(max_iter=max_iter))))

        sklearn_pipeline.fit(self.data_train, self.label_train)
        logging.info('Regressor trained')

        sklearn_train_pred = sklearn_pipeline.predict(self.data_train)
        sklearn_train_loss = log_loss(self.label_train, sklearn_train_pred)
        logging.info('train log_less: %f', float(sklearn_train_loss))
        logging.info('train f1: %f', f1_score(self.label_train, sklearn_train_pred, pos_label=0))

        sklearn_test_pred = sklearn_pipeline.predict(self.data_test)
        sklearn_test_loss = log_loss(self.label_test, sklearn_test_pred)
        logging.info('test log_less: %f', float(sklearn_test_loss))
        logging.info('test f1: %f', f1_score(self.label_test, sklearn_test_pred, pos_label=0))

        logging.info('Predict for [i hate everyone]: %d', sklearn_pipeline.predict(['i hate you']))

        pickle.dump(sklearn_pipeline, open(os.path.join(common_dir, model_file), 'wb'))
