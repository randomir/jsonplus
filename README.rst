JSON+
=====

Serialization of common data types (which are out of the JSON specs_) that works
out of the box (batteries included).

So far, modules (packages) for Python_ and Flask_ are implemented, and they
support (de-)serialization of types like ``tuple``/``namedtuple``,
``set``/``frozenset``, ``complex``/``Decimal``/``Fraction``,
and ``datetime``/``date``/``time``/``timedelta`` (in addition to basic JSON
types).

.. _specs: https://tools.ietf.org/html/rfc7159.html
.. _Python: https://github.com/randomir/jsonplus/tree/master/python
.. _Flask: https://github.com/randomir/jsonplus/tree/master/python-flask
