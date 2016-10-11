"""Custom datatypes (like datetime) serialization to/from JSON."""

import simplejson as json
from datetime import datetime, timedelta, date, time
from dateutil.parser import parse as parse_datetime
from functools import wraps, partial
from operator import methodcaller


def getattrs(value, attrs):
    return {attr: getattr(value, attr) for attr in attrs}

def _json_default(obj):
    classname = type(obj).__name__
    handlers = {
        'datetime': methodcaller('isoformat'),
        'date': methodcaller('isoformat'),
        'time': methodcaller('isoformat'),
        'timedelta': partial(getattrs, attrs=['days', 'seconds', 'microseconds']),
        'set': list,
        'complex': partial(getattrs, attrs=['real', 'imag'])
    }
    if classname in handlers:
        return {"__class__": classname,
                "__value__": handlers[classname](obj)}
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
        'time': lambda v: parse_datetime(v).timetz(),
        'set': set,
        'complex': kwargified(complex)
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
