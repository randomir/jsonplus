from datetime import datetime

from flask import Flask, jsonify

app = Flask(__name__)


### jsonplus-driven jsonification

from jsonplus import JSONEncoder, JSONDecoder

app.json_encoder = JSONEncoder
app.json_decoder = JSONDecoder


@app.route('/')
def hello_world():
    data = {
        'num': 1.23,
        'now': datetime.now()
    }
    return jsonify(data)
