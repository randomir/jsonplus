"""Custom datatypes (like datetime) serialization to/from JSON."""

__version__ = '0.2'
__author__ = 'Radomir Stevanovic'
__author_email__ = 'radomir.stevanovic@gmail.com'
__copyright__ = 'Copyright 2013 Radomir Stevanovic'
__license__ = 'MIT'


import simplejson as json
from datetime import datetime, timedelta, date, time
from dateutil.parser import parse as parse_datetime
from functools import wraps


def _isoformat_for_json(value):
    return {"__class__": type(value).__name__,
            "__value__": value.isoformat()}

def _timedelta_for_json(value):
    return {"__class__": type(value).__name__,
            "__value__": {"days": value.days,
                          "seconds": value.seconds,
                          "microseconds": value.microseconds}}

def _json_default(obj):
    if isinstance(obj, datetime) or isinstance(obj, date) or isinstance(obj, time):
        return _isoformat_for_json(obj)
    elif isinstance(obj, timedelta):
        return _timedelta_for_json(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")


def kwargified(constructor):
    @wraps(constructor)
    def kwargs_constructor(kwargs):
        return constructor(**kwargs)
    return kwargs_constructor

def _json_object_hook(dict):
    classname = dict.get('__class__')
    handlers = {
        'datetime': parse_datetime,
        'timedelta': kwargified(timedelta),
        'date': lambda v: parse_datetime(v).date(),
        'time': lambda v: parse_datetime(v).timetz()
    }
    if classname:
        constructor = handlers.get(classname)
        value = dict.get('__value__')
        if constructor:
            return constructor(value)
        raise TypeError("Unknown class: '%s'" % classname)
    return dict


def json_dumps(*pa, **kw):
    kwupt = {'separators': (',', ':'), 'for_json': True, 'default': _json_default}
    kwupt.update(kw)
    return json.dumps(*pa, **kwupt)

def json_loads(*pa, **kw):
    kwupt = {'object_hook': _json_object_hook}
    kwupt.update(kw)
    return json.loads(*pa, **kwupt)

def json_prettydump(x, sort_keys=True):
    return json_dumps(x, sort_keys=sort_keys, indent=4*' ', separators=(',', ': '))
