from flask import Flask, jsonify
import os
import json

app = Flask(__name__)

@app.route('/')
def index(fileName="news.json"):
    with open(os.path.join(os.path.join(os.path.dirname(os.path.realpath('__file__')), 'results'), fileName), "r") as file:
      dataSet = json.load(file)
    return jsonify(dataSet)

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=666)