"""Model trainer."""

import os
import pickle

from pandas import read_csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, log_loss
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


class ModelTrainer:
    """Train and save ml-model. Using tf-idf + logistic regression."""

    def __init__(self, logger):
        self.logger = logger

        self.data_train = []
        self.data_test = []
        self.label_train = []
        self.label_test = []

        self.logger.info('Object initialization is completed')

    def prepare_data_set(self, common_dir, data_set_file, data_col=1, label_col=0, test_size=0.05):
        """Read dataset created by Connector module."""

        self.logger.info('Attempt to create dataset')

        dataset = read_csv(os.path.join(common_dir, data_set_file),
                           encoding="ISO-8859-1",
                           engine='python',
                           header=None)

        self.logger.info('Dataset is loaded')
        self.logger.info('Dataset len: %d', len(dataset))

        self.logger.info('Start dataset splitting')
        dataset_train, dataset_test = train_test_split(dataset, test_size=test_size)

        self.data_train = dataset_train.iloc[:, data_col]
        self.data_test = dataset_test.iloc[:, data_col]
        self.label_train = dataset_train.iloc[:, label_col]
        self.label_test = dataset_test.iloc[:, label_col]

        self.logger.info('End of dataset splitting')

    def train(self, common_dir, model_file, max_df=0.8, min_count=5, max_iter=10000):
        """Train model."""
        self.logger.info('Attempt to create sklearn pipeline')

        sklearn_pipeline = Pipeline((('vec', TfidfVectorizer(max_df=max_df, min_df=min_count)),
                                    ('cls', LogisticRegression(max_iter=max_iter))))

        self.logger.info('Pipeline is created')

        self.logger.info('Starting regressor training')
        sklearn_pipeline.fit(self.data_train, self.label_train)
        self.logger.info('Regressor is trained')

        self.logger.info('Starting regressor predictions on train dataset')
        sklearn_train_pred = sklearn_pipeline.predict(self.data_train)
        sklearn_train_loss = log_loss(self.label_train, sklearn_train_pred)
        self.logger.info('Prediction is completed')

        self.logger.info('Train log_less: %f', float(sklearn_train_loss))
        self.logger.info('Train f1: %f', f1_score(self.label_train, sklearn_train_pred, pos_label=0))

        self.logger.info('Starting regressor predictions on test dataset')
        sklearn_test_pred = sklearn_pipeline.predict(self.data_test)
        sklearn_test_loss = log_loss(self.label_test, sklearn_test_pred)
        self.logger.info('Prediction is completed')

        self.logger.info('test log_less: %f', float(sklearn_test_loss))
        self.logger.info('test f1: %f', f1_score(self.label_test, sklearn_test_pred, pos_label=0))

        self.logger.info('Predict for [i hate everyone]: %d', sklearn_pipeline.predict(['i hate you']))

        pickle.dump(sklearn_pipeline, open(os.path.join(common_dir, model_file), 'wb'))
        self.logger.info('Model is saved in %s', os.path.join(common_dir, model_file))
