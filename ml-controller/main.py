from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss, f1_score
from pandas import read_csv
import logging
import pickle

MAX_DF = 0.8
MIN_COUNT = 5

MAX_ITER = 10000


def main():
    dataset = read_csv('data/training.1600000.processed.noemoticon.csv', encoding="ISO-8859-1", engine='python', header=None)
    dataset.columns = ['target', 'ids', 'date', 'flag', 'user', 'text']

    logging.info('Dataset loaded')
    logging.info('Dateset len: {0}'.format(len(dataset)))

    dataset_train, dataset_test = train_test_split(dataset, test_size=0.05)

    sklearn_pipeline = Pipeline((('vec', TfidfVectorizer(max_df=MAX_DF,
                                                          min_df=MIN_COUNT)),
                                 ('cls', LogisticRegression(max_iter=MAX_ITER))))
    sklearn_pipeline.fit(dataset_train['text'], dataset_train['target'])
    logging.info('Regressor trained')

    sklearn_train_pred = sklearn_pipeline.predict(dataset_train['text'])
    sklearn_train_loss = log_loss(dataset_train['target'], sklearn_train_pred)
    logging.info('train log_less: {0}'.format(float(sklearn_train_loss)))
    logging.info(
        'train f1: {0}'.format(f1_score(dataset_train['target'], sklearn_train_pred, pos_label=0)))

    sklearn_test_pred = sklearn_pipeline.predict(dataset_test['text'])
    sklearn_test_loss = log_loss(dataset_test['target'], sklearn_test_pred)
    logging.info('test log_less: {0}'.format(float(sklearn_test_loss)))
    logging.info(
        'test f1: {0}'.format(f1_score(dataset_test['target'], sklearn_test_pred, pos_label=0)))

    logging.info('Predict for [i hate everyone]: {0}'.format(sklearn_pipeline.predict(['i hate you'])))

    pickle.dump(sklearn_pipeline, open('data/pipe.zip', 'wb'))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
