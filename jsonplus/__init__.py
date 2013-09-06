"""Custom datatypes (like datetime) serialization to/from JSON."""

__version__ = '0.1'
__author__ = 'Radomir Stevanovic'


import simplejson as json
from datetime import datetime
from dateutil.parser import parse as parse_datetime


def _datetime_for_json(value):
    return {"__class__": type(value).__name__,
            "__value__": value.isoformat()}


def _json_default(obj):
    if isinstance(obj, datetime):
        return _datetime_for_json(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")


def _json_object_hook(dict):
    classname = dict.get('__class__')
    handlers = {
        'datetime': parse_datetime
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
