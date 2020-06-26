"""Flask server"""

import os
import pickle
import random
import string
from flask import Flask, jsonify, request
import eli5
import yaml

CONFIG_FILE = 'config.yaml'
app = Flask(__name__)
model = None
message_id_dict = {}
id_expl_dict = {}


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    """Generate random id."""
    return ''.join(random.choice(chars) for _ in range(size))


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
    content = request.get_json()

    if content['text'] in message_id_dict:
        content['id'] = message_id_dict[content['text']]
    else:
        new_id = id_generator()
        message_id_dict[content['text']] = new_id
        content['id'] = new_id

    return content


@app.route('/v1/p/<message_id>', methods=["GET"])
def get_result(message_id):
    """Create HTML page with ML-model result."""
    html_page = None

    if message_id in id_expl_dict:
        html_page = eli5.formatters.html.format_as_html(id_expl_dict[message_id])
    else:
        for message, search_id in message_id_dict.items():
            if search_id == message_id:
                id_expl_dict[message_id] = eli5.sklearn.explain_prediction_linear_regressor(model['cls'],
                                                                                            message,
                                                                                            model['vec'])
                html_page = eli5.formatters.html.format_as_html(id_expl_dict[message_id])
                break

    if html_page is not None:
        return html_page

    return 'Id not found', 400


def main():
    """Load config and run flask app."""
    global model
    with open(CONFIG_FILE) as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)

    model = pickle.load(open(os.path.join(config_data['common_dir'], config_data['model_name']), 'rb'))

    app.run(debug=True, host='0.0.0.0', port=config_data['port'])


if __name__ == '__main__':
    main()
