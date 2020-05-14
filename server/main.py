from flask import Flask, jsonify
import os
import json

app = Flask(__name__)


@app.route('/')
def index(file_name="news.json"):
    data_set = {}

    if os.path.exists(file_name):
        with open(os.path.join(os.path.join(os.path.dirname(os.path.realpath('__file__')), 'data'), file_name)) as file:
            data_set = json.load(file)

    return jsonify(data_set)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=666)
