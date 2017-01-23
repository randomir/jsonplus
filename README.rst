JSON+
=====

Serialization of Python types to JSON done right.

No more errors like::

    TypeError: datetime.datetime(...) is not JSON serializable

In addition to (de-)serialization of basic types (provided by simplejson_), jsonplus_
provides support for **exact** (de-)serialization of other commonly used types, like:
``tuple``/``namedtuple``, ``set``/``frozenset``, ``complex``/``decimal.Decimal``/``fractions.Fraction``,
and ``datetime``/``date``/``time``/``timedelta``.

.. _simplejson: https://simplejson.readthedocs.io/en/latest/#encoders-and-decoders
.. _jsonplus: https://pypi.python.org/pypi/jsonplus/


Installation
------------

``jsonplus`` is available as Python package. To install, simply type::

    $ pip install jsonplus


Usage
-----

You can treat ``jsonplus`` as a friendly *drop-in* replacement for ``json``/``simplejson``.

.. code-block:: python

    >>> import jsonplus as json
    >>>
    >>> x = json.loads('{"a":1,"b":2}')
    >>> y = json.dumps(x, indent=4)
    >>> z = json.pretty(x)


Examples
--------

Let's start with that beloved ``datetime``.

.. code-block:: python

    >>> import jsonplus as json

    >>> from datetime import datetime
    >>> json.dumps({
    ...     "x": [4,3],
    ...     "t": datetime.now()
    ... })
    '{"x":[4,3],"t":{"__class__":"datetime","__value__":"2013-09-06T23:38:55.819791"}}'
    
    >>> json.loads(_)
    {u'x': [4, 3], u't': datetime.datetime(2013, 9, 6, 23, 38, 55, 819791)}

Similarly for other ``datetime.*`` types, like ``timedelta``, ``date``, and ``time``:

.. code-block:: python

    >>> from datetime import timedelta, date, time
    >>> print json.pretty({"dt": timedelta(0, 1234567, 123), "d": date.today(), "t": datetime.now().time()})
    {
        "d": {
            "__class__": "date",
            "__value__": "2013-09-22"
        },
        "dt": {
            "__class__": "timedelta",
            "__value__": {
                "days": 14,
                "microseconds": 123,
                "seconds": 24967
            }
        },
        "t": {
            "__class__": "time",
            "__value__": "23:33:16.335360"
        }
    }

Also, ``set`` and ``complex``:

.. code-block:: python

    >>> json.dumps([set(range(3)), 1+2j])
    '[{"__class__":"set","__value__":[0,1,2]},{"__class__":"complex","__value__":{"real":1.0,"imag":2.0}}]'
    
    >>> json.loads(_)
    [set([0, 1, 2]), (1+2j)]

