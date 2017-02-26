Flask-JSONPlus
==============

Flask extension for non-basic types' serialization to JSON via jsonplus_ lib.

.. _jsonplus: https://pypi.python.org/pypi/jsonplus/


Install
-------

Install from PyPI::

    pip install Flask-JSONPlus

Enable in your Flask app (probably your ``app/__init__.py``):

.. code-block:: python

    from flask_jsonplus import FlaskJSONPlus

    app = Flask(__name__)

    app.config['JSONPLUS_EXACT'] = True

    jsonplus = FlaskJSONPlus(app)


Usage
-----

After you enable FlaskJSONPlus, Flask will start to use ``jsonplus`` internally
for JSON (de-)serialization. For example, ``jsonify`` will properly serialize
your rich data:

.. code-block:: python

    import datetime, fractions, decimal, collections

    @app.route('/api/demo')
    def api_demo():
        Point = collections.namedtuple('Point', 'x y')
        data = {
            'third': fractions.Fraction(1, 3),
            'dec': decimal.Decimal('0.1'),
            'now': datetime.datetime.now(),
            'set': set(range(3)),
            'tuple': (3, 1, 4),
            'namedtuple': Point(3, 4)
        }
        return jsonify(data)
