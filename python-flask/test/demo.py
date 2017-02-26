from datetime import datetime
from collections import namedtuple
from fractions import Fraction
from decimal import Decimal

from flask import Flask, jsonify
from flask_jsonplus import FlaskJSONPlus

app = Flask(__name__)
app.config['JSONPLUS_EXACT'] = True

jsonplus = FlaskJSONPlus(app)


@app.route('/')
def hello_world():
    Point = namedtuple('Point', 'x y')
    data = {
        'third': Fraction(1, 3),
        'dec': Decimal('0.1'),
        'now': datetime.now(),
        'set': set(range(3)),
        'tuple': (3, 1, 4),
        'namedtuple': Point(3, 4)
    }
    return jsonify(data)
