JSON+
=====

Serialization of Python types to JSON done right.

Examples
--------

Let's start with `datetime`.

.. code-block:: python

    >>> from jsonplus import json_loads, json_dumps, json_prettydump
    
    >>> from datetime import datetime
    >>> json_dumps({
    ...     "x": [4,3],
    ...     "t": datetime.now()
    ... })
    '{"x":[4,3],"t":{"__class__":"datetime","__value__":"2013-09-06T23:38:55.819791"}}'
    
    >>> json_loads(_)
    {u'x': [4, 3], u't': datetime.datetime(2013, 9, 6, 23, 38, 55, 819791)}

Continue with other `datetime.*` types, like `timedelta`, `date`, and `time`.

.. code-block:: python

    >>> from datetime import timedelta, date, time
    >>> print json_prettydump({"dt": timedelta(0, 1234567, 123), "d": date.today(), "t": datetime.now().time()})
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

Also, `set` and `complex`:

.. code-block:: python

    >>> json_dumps([set(range(3)), 1+2j])
    '[{"__class__":"set","__value__":[0,1,2]},{"__class__":"complex","__value__":{"real":1.0,"imag":2.0}}]'
    
    >>> json_loads(_)
    [set([0, 1, 2]), (1+2j)]
