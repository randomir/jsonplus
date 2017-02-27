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

(in addition to basic JSON types).


.. _specs: https://tools.ietf.org/html/rfc7159.html
.. _Python: https://github.com/randomir/jsonplus/tree/master/python
.. _Flask: https://github.com/randomir/jsonplus/tree/master/python-flask
.. _Django: https://github.com/randomir/jsonplus/tree/master/python-django
