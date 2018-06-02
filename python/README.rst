JSON+
=====

.. image:: https://img.shields.io/pypi/v/jsonplus.svg
    :target: https://pypi.python.org/pypi/jsonplus

.. image:: https://img.shields.io/pypi/l/jsonplus.svg
    :target: https://pypi.python.org/pypi/jsonplus

.. image:: https://img.shields.io/pypi/wheel/jsonplus.svg
    :target: https://pypi.python.org/pypi/jsonplus

.. image:: https://img.shields.io/pypi/pyversions/jsonplus.svg
    :target: https://pypi.python.org/pypi/jsonplus

.. image:: https://api.travis-ci.org/randomir/jsonplus.svg?branch=master
    :target: https://travis-ci.org/randomir/jsonplus


Serialization of Python types to JSON that "just works".

Forget errors like::

    TypeError: datetime.datetime(...) is not JSON serializable

In addition to (de-)serialization of basic types (provided by simplejson_), jsonplus_
provides support for **exact** (de-)serialization of other commonly used types, like:
``tuple``/``namedtuple``, ``set``/``frozenset``, ``complex``/``decimal.Decimal``/``fractions.Fraction``,
and ``datetime``/``date``/``time``/``timedelta``.

If the exact representation of types is not your cup of tea, and all you wish
for is the ``json.dumps`` to work on your data structure with non-basic types,
accepting the loss of "type-precision" along the way, than you can use the
**compatibility** mode (thread-local ``jsonplus.prefer_compat()``, or
per-call override ``jsonplus.dumps(..., exact=False)``).

.. _simplejson: https://simplejson.readthedocs.io/en/latest/#encoders-and-decoders
.. _jsonplus: https://pypi.python.org/pypi/jsonplus/


Installation
------------

``jsonplus`` is available as a Python package. To install it, simply type::

    $ pip install jsonplus


Usage
-----

You can treat ``jsonplus`` as a friendly *drop-in* replacement for ``json``/``simplejson``.

.. code-block:: python

    >>> import jsonplus as json

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
    >>> print(json.pretty({"dt": timedelta(0, 1234567, 123), "d": date.today(), "t": datetime.now().time()}))
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

``tuple`` and ``namedtuple`` are also preserved:

.. code-block:: python

    >>> from collections import namedtuple
    >>> Point = namedtuple('Point', ['x', 'y'])

    >>> data = json.pretty({"vect": (1, 2, 3), "dot": Point(3, 4)})
    >>> print(data)
    {
        "dot": {
            "__class__": "namedtuple",
            "__value__": {
                "fields": [
                    "x",
                    "y"
                ],
                "name": "Point",
                "values": [
                    3,
                    4
                ]
            }
        },
        "vect": {
            "__class__": "tuple",
            "__value__": [
                1,
                2,
                3
            ]
        }
    }

    >>> json.loads(data)
    {'vect': (1, 2, 3), 'dot': Point(x=3, y=4)}


Compatibility mode
------------------

All types supported in the exact mode are also supported in the compatibility
mode. JSON representation differs, however.

In the exact mode, *type* and *value* are encoded with ``JSON Object``'s
``__class__`` and ``__value__`` keys, while in the compatibility mode, 
**values are "rounded off" to the closest JSON type**.

For example, ``tuple`` and ``set`` are represented with ``JSON Array``, and
``namedtuple`` is coded as a plain ``JSON Object``. ``Decimal`` is
represented as ``JSON Number`` with arbitrary precision (which is lost if
decoded as ``float``).

To switch between the **exact** and **compatibility** modes, use the 
(thread-local) functions ``prefer_exact()`` and ``prefer_compat()``, or call
``dumps(..., exact=False)``:

.. code-block:: python

    >>> import jsonplus as json

    >>> json.prefer_compat()
    # or:
    >>> json.prefer(json.COMPAT)
    # per-instance override:
    >>> json.dumps(obj, exact=False)

    # to go back to (default) exact coding:
    >>> json.prefer_exact()

The above ``tuple``/``namedtuple``/``datetime`` examples run in the compatibility 
coding mode result with:

.. code-block:: python

    >>> json.prefer_compat()

    >>> print(json.pretty({"vect": (1, 2, 3), "dot": Point(3, 4)}))
    {
        "point": {
            "x": 3,
            "y": 4
        },
        "vector": [
            1,
            2,
            3
        ]
    }

    >>> json.dumps({"now": datetime.now()})
    '{"now":"2017-01-26T00:37:40.293963"}'

So, to be able to properly decode values in the compatibility mode, some 
additional context will have to be provided to the decoder.


Adding user types
-----------------

Support for user/custom types can easily be added with ``@jsonplus.encoder`` and
``@jsonplus.decoder`` decorators.

For example, to enable serialization of your type named ``mytype`` in exact mode
(to add compat-mode serialization, append ``exact=False`` in decorator):

.. code-block:: python

    @jsonplus.encoder('mytype')
    def mytype_exact_encoder(myobj):
        return myobj.to_json()

.. code-block:: python

    @jsonplus.decoder('mytype')
    def mytype_decoder(value):
        return mytype(value, reconstruct=True, ...)

If detection of object class is more complex than a simple classname comparison,
you'll need to use a **predicate** function: simply add ``predicate=...`` to the ``encoder``
decorator. For example:

.. code-block:: python

    @jsonplus.encoder('BaseClass', predicate=lambda obj: isinstance(obj, BaseClass))
    def all_derived_classes_encoder(derived):
        return derived.base_encoder()

To control the order in which predicates are tested, use ``priority`` keyword argument.
First predicated encoder has priority of 1000, and if not explicitly given, each new encoder
is appended with priority ``last+100``. A lower priority predicate is tested before a higher
priority predicate.

Classname-based (en/de)coders are tested *after* all predicate-based ones.
Classname lookup has a constant amortized time, but predicates have to be tested (executed)
one by one. Hence, in interest of performance, minimize the number of predicate-based
coders, and try using classname-based ones (if possible).
