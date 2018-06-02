JSON+
=====

Serialization of common data types (which are out of the JSON specs_) that works
out of the box (batteries included).

So far, modules (packages) for Python_, Flask_ and Django_ are implemented, and
they support (de-)serialization of types like:

- ``tuple`` and ``namedtuple``
- ``set`` and ``frozenset``
- ``complex``, ``Decimal``, and ``Fraction``
- ``datetime``, ``date``, ``time``, and ``timedelta``
- ``UUID``, ``moneyed.Money``, ``moneyed.Currency``

(in addition to basic JSON supported-types like integers, floats, lists, and dictionaries).

Also, encoder and decoder for custom (user) types can easily be registered (see python_ example).

Overview
--------

+----------------------+----------------+--------------------------------------------------------------+
| Language/Framework   | Source         | Implemented                                                  |
+======================+================+==============================================================+
| Python 2.6+, 3.3+    | python_        | (De-)Serialization drop-in replacement for ``simplejson``.   |
|                      |                | Exact & compatibility mode supported. See detailed docs_.    |
+----------------------+----------------+--------------------------------------------------------------+
| Django 1.8+          | python-django_ | As ``jsonplus`` + database model field ``JSONPlusField``.    |
+----------------------+----------------+--------------------------------------------------------------+
| Flask 0.10+          | python-flask_  | Using ``jsonplus`` as the default Flask (de-)serializator.   |
+----------------------+----------------+--------------------------------------------------------------+
| JavaScript           | n/a            | TODO                                                         |
+----------------------+----------------+--------------------------------------------------------------+

.. _specs: https://tools.ietf.org/html/rfc7159.html
.. _docs: https://github.com/randomir/jsonplus/tree/master/python
.. _Python: https://github.com/randomir/jsonplus/tree/master/python
.. _python: https://github.com/randomir/jsonplus/tree/master/python
.. _Flask: https://github.com/randomir/jsonplus/tree/master/python-flask
.. _python-flask: https://github.com/randomir/jsonplus/tree/master/python-flask
.. _Django: https://github.com/randomir/jsonplus/tree/master/python-django
.. _python-django: https://github.com/randomir/jsonplus/tree/master/python-django
