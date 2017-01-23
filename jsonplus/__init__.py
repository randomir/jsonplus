"""Custom datatypes (like datetime) serialization to/from JSON."""

# TODO: introduce options to prefer: (a) exact coding *or* 
# (b) cross-compat coding. Think of ``tuple`` and ``Decimal``.

import simplejson as json
from datetime import datetime, timedelta, date, time
from dateutil.parser import parse as parse_datetime
from functools import wraps, partial
from operator import methodcaller
from decimal import Decimal
from fractions import Fraction
from collections import namedtuple

__all__ = ["loads", "dumps", "pretty",
           "json_loads", "json_dumps", "json_prettydump"]


def _dump_namedtuple(classname, obj):
    return {"name": classname, "fields": list(obj._fields), "values": list(obj)}

def _load_namedtuple(val):
    cls = namedtuple(val['name'], val['fields'])
    return cls(*val['values'])


def getattrs(value, attrs):
    return {attr: getattr(value, attr) for attr in attrs}

def _json_default(obj):
    """Serialization handlers for types unsupported by `simplejson`.
    """
    classname = type(obj).__name__
    handlers = {
        'datetime': methodcaller('isoformat'),
        'date': methodcaller('isoformat'),
        'time': methodcaller('isoformat'),
        'timedelta': partial(getattrs, attrs=['days', 'seconds', 'microseconds']),
        'tuple': list,
        'set': list,
        'frozenset': list,
        'complex': partial(getattrs, attrs=['real', 'imag']),
        'Decimal': str,
        'Fraction': partial(getattrs, attrs=['numerator', 'denominator']),
    }
    if classname in handlers:
        return {"__class__": classname,
                "__value__": handlers[classname](obj)}
    elif isinstance(obj, tuple) and classname != 'tuple':
        return {"__class__": "namedtuple",
                "__value__": _dump_namedtuple(classname, obj)}
    raise TypeError(repr(obj) + " is not JSON serializable")


def kwargified(constructor):
    @wraps(constructor)
    def kwargs_constructor(kwargs):
        return constructor(**kwargs)
    return kwargs_constructor

def _json_object_hook(dict):
    """Deserialization handlers for types unsupported by `simplejson`.
    """
    classname = dict.get('__class__')
    handlers = {
        'datetime': parse_datetime,
        'date': lambda v: parse_datetime(v).date(),
        'time': lambda v: parse_datetime(v).timetz(),
        'timedelta': kwargified(timedelta),
        'tuple': tuple,
        'set': set,
        'frozenset': frozenset,
        'complex': kwargified(complex),
        'Decimal': Decimal,
        'Fraction': kwargified(Fraction),
        'namedtuple': _load_namedtuple,
    }
    if classname:
        constructor = handlers.get(classname)
        value = dict.get('__value__')
        if constructor:
            return constructor(value)
        raise TypeError("Unknown class: '%s'" % classname)
    return dict


def json_dumps(*pa, **kw):
    # set ``tuple_as_array=False`` to support exact tuple serialization
    # set ``namedtuple_as_object=False`` *and* ``tuple_as_array=False`` to support exact namedtuple serialization
    kwupt = {'separators': (',', ':'), 'for_json': True, 'default': _json_default,
             'use_decimal': False}
    kwupt.update(kw)
    return json.dumps(*pa, **kwupt)

def json_loads(*pa, **kw):
    kwupt = {'object_hook': _json_object_hook}
    kwupt.update(kw)
    return json.loads(*pa, **kwupt)

def json_prettydump(x, sort_keys=True):
    return json_dumps(x, sort_keys=sort_keys, indent=4*' ', separators=(',', ': '))


dumps = json_dumps
loads = json_loads
pretty = json_prettydump
