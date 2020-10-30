from flask import Flask, jsonify, request
from kafka import KafkaConsumer, KafkaProducer

from .util import id_generator

app = Flask(__name__)

config_data = None
producer = None


def server_init(config):
    global config_data
    global producer

    config_data = config
    producer = KafkaProducer(bootstrap_servers=[config_data['kafka_server']],
                             value_serializer=lambda x: x.encode('utf-8'),
                             key_serializer=lambda x: x.encode('utf-8')
                             )


def server_start():
    app.run(debug=True, host='0.0.0.0', port=config_data['port'])


@app.route('/v1', methods=["GET"])
def info_view():
    """List of routes."""
    output = {
        'info': 'GET /v1',
        'get json template': 'GET /v1/p',
        'add new, return json with id': 'POST /v1/p',
        'view result': 'GET /v1/p/<id>'
    }
    return jsonify(output)


@app.route('/v1/p', methods=["GET"])
def json_template():
    """Return JSON template for POST."""
    output = {
        'id': '',
        'text': ''
    }
    return jsonify(output)


@app.route('/v1/p', methods=["POST"])
def add_message():
    """Return new id."""

    content = request.get_json(force=True)
    if content is None:
        return 'Empty request', 400

    new_id = id_generator()
    content['id'] = new_id

    producer.send(config_data['new_issues_topic'], key=new_id, value=content['text'])

    return content


@app.route('/v1/p/<message_id>', methods=["GET"])
def get_result(message_id):
    """Create HTML page with ML-model result."""

    # TODO: refactor: one initialization
    consumer = KafkaConsumer(config_data['processed_issues_topic'],
                             auto_offset_reset='earliest',
                             bootstrap_servers=[config_data['kafka_server']],
                             # value_deserializer=lambda x: loads(x.decode('utf-8')),
                             key_deserializer=lambda x: x.decode('utf-8'),
                             consumer_timeout_ms=300
                             )

    for msg in consumer:
        print(msg.value)
        if msg.key == message_id:
            return msg.value
    consumer.close()

    return 'Id not found', 400
