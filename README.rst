JSON+
=====

Serialization of Python types to JSON done right.

Examples
--------

.. code-block:: python

    >>> from jsonplus import json_loads, json_dumps
    
    >>> from datetime import datetime
    >>> json_dumps({
    ...     "x": [4,3],
    ...     "t": datetime.now()
    ... })
    '{"x":[4,3],"t":{"__class__":"datetime","__value__":"2013-09-06T23:38:55.819791"}}'
    
    >>> json_loads(_)
    {u'x': [4, 3], u't': datetime.datetime(2013, 9, 6, 23, 38, 55, 819791)}
