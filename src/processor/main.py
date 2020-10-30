import os
from json import dumps
from pickle import load as pickle_load

import eli5
from kafka import KafkaConsumer, KafkaProducer
import yaml

CONFIG_FILE = 'config.yaml'


def main():
    with open(CONFIG_FILE) as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)

    if os.path.exists(os.path.join(config_data['common_dir'], config_data['model_name'])):
        model = pickle_load(open(os.path.join(config_data['common_dir'], config_data['model_name']), 'rb'))

    consumer = KafkaConsumer(
        config_data['new_issues_topic'],
        auto_offset_reset='latest',
        bootstrap_servers=[config_data['kafka_server']],
        value_deserializer=lambda x: x.decode('utf-8', 'ignore'))

    producer = KafkaProducer(
        bootstrap_servers=[config_data['kafka_server']],
        value_serializer=lambda x:
        dumps(x).encode('utf-8'))

    for msg in consumer:
        expl = eli5.sklearn.explain_prediction_linear_regressor(model['cls'],
                                                                msg.value,
                                                                model['vec'])
        response = eli5.formatters.as_dict.format_as_dict(expl)

        print(response)

        producer.send(config_data['processed_issues_topic'], key=msg.key, value=response)

    consumer.close()


if __name__ == '__main__':
    main()
