"""Custom datatypes (like datetime) serialization to/from JSON."""

# TODO: handle environments without threads
# (Python compiled without thread support)

import simplejson as json
from datetime import datetime, timedelta, date, time
from dateutil.parser import parse as parse_datetime
from functools import wraps, partial
from operator import methodcaller
from decimal import Decimal
from fractions import Fraction
from collections import namedtuple
import threading
import uuid

__all__ = ["loads", "dumps", "pretty",
           "json_loads", "json_dumps", "json_prettydump"]


# Should we aim for the *exact* reproduction of Python types,
# or for maximum *compatibility* when (de-)serializing?
#
# By default, we prefer the exactness of reproduction.
# For example, `tuple`, `namedtuple`, `Decimal`, or `datetime` will all be
# restored to the appropriate type (same as the starting type -- even the
# custom class for the `namedtuple` is recreated).
# When compatible coding if turned on, we shall fallback to standard JSON
# types, and values from the example above will be serialized as
# `list` (`Array`), `dict` (`Object`), `Number` and `ISO8601 timestamp string`,
# respectively.
#
# Please note:
#  - `compat` mode is lossy -- `namedtuple` serialized as `dict`/`Object`
#    can never be deserialized as `namedtuple`.
#  - `exact` mode is verbose -- and if you have a standard JSON decoder on
#    the other end, all that additional type info is useless/discared.
#
# To switch between representation styles, use `jsonplus.prefer(coding)`,
# where `coding` is `jsonplus.EXACT` or `jsonplus.COMPAT`. Another way, maybe
# simpler, is to use `jsonplus.prefer_exact()` and `jsonplus.prefer_compat()`.
#
# The preference is stored thread-local.

EXACT = 1
COMPAT = 2
CODING_DEFAULT = EXACT

_local = threading.local()

def prefer(coding):
    _local.coding = coding

def prefer_exact():
    prefer(EXACT)

def prefer_compat():
    prefer(COMPAT)


def _dump_namedtuple(classname, obj):
    return {"name": classname, "fields": list(obj._fields), "values": list(obj)}


def _load_namedtuple(val):
    cls = namedtuple(val['name'], val['fields'])
    return cls(*val['values'])


def getattrs(value, attrs):
    return {attr: getattr(value, attr) for attr in attrs}


def _json_default_exact(obj):
    """Serialization handlers for types unsupported by `simplejson` 
    that try to preserve the exact data types.
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
        'UUID': partial(getattrs, attrs=['hex']),
    }
    if classname in handlers:
        return {"__class__": classname,
                "__value__": handlers[classname](obj)}
    elif isinstance(obj, tuple) and classname != 'tuple':
        return {"__class__": "namedtuple",
                "__value__": _dump_namedtuple(classname, obj)}
    raise TypeError(repr(obj) + " is not JSON serializable")


def _json_default_compat(obj):
    classname = type(obj).__name__
    handlers = {
        'datetime': methodcaller('isoformat'),
        'date': methodcaller('isoformat'),
        'time': methodcaller('isoformat'),
        'timedelta': methodcaller('total_seconds'),
        'set': list,
        'frozenset': list,
        'complex': partial(getattrs, attrs=['real', 'imag']),
        'Fraction': partial(getattrs, attrs=['numerator', 'denominator']),
        'UUID': str
    }
    if classname in handlers:
        return handlers[classname](obj)
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
        'UUID': kwargified(uuid.UUID)
    }
    if classname:
        constructor = handlers.get(classname)
        value = dict.get('__value__')
        if constructor:
            return constructor(value)
        raise TypeError("Unknown class: '%s'" % classname)
    return dict



def _encoder_default_args(kw):
    """Shape default arguments for encoding functions."""
    
    # manual override of the preferred coding with `exact=False`
    if kw.pop('exact', getattr(_local, 'coding', CODING_DEFAULT) == EXACT):
        # settings necessary for the "exact coding"
        kw.update({
            'default': _json_default_exact,
            'use_decimal': False,           # don't encode `Decimal` as JSON's `Number`
            'tuple_as_array': False,        # don't encode `tuple` as `Array`
            'namedtuple_as_object': False   # don't call `_asdict` on `namedtuple`
        })
    else:
        # settings for the "compatibility coding"
        kw.update({
            'default': _json_default_compat,
            'ignore_nan': True      # be compliant with the ECMA-262 specification:
                                    # serialize nan/inf as null
        })

    # NOTE: if called from ``simplejson.dumps()`` with ``cls=JSONEncoder``,
    # we will receive all kw set to simplejson defaults -- and our defaults for
    # ``separators`` and ``for_json`` will not be applied. In contrast, they
    # are applied when called from ``jsonplus.dumps()``, unless user explicitly
    # sets some of those.
    # This causes inconsistent behaviour between ``dumps()`` and ``JSONEncoder()``.

    # prefer compact json repr
    kw.setdefault('separators', (',', ':'))

    # allow objects to provide json serialization on its behalf
    kw.setdefault('for_json', True)


def _decoder_default_args(kw):
    """Shape default arguments for decoding functions."""

    kw.update({'object_hook': _json_object_hook})



class JSONEncoder(json.JSONEncoder):
    def __init__(self, **kw):
        """Constructor for simplejson.JSONEncoder, with defaults overriden
        for jsonplus.
        """
        _encoder_default_args(kw)
        super(JSONEncoder, self).__init__(**kw)


class JSONDecoder(json.JSONDecoder):
    def __init__(self, **kw):
        """Constructor for simplejson.JSONDecoder, with defaults overriden
        for jsonplus.
        """
        _decoder_default_args(kw)
        super(JSONDecoder, self).__init__(**kw)



def dumps(*pa, **kw):
    _encoder_default_args(kw)
    return json.dumps(*pa, **kw)


def loads(*pa, **kw):
    _decoder_default_args(kw)
    return json.loads(*pa, **kw)


def pretty(x, sort_keys=True, indent=4*' ', separators=(',', ': '), **kw):
    kw.setdefault('sort_keys', sort_keys)
    kw.setdefault('indent', indent)
    kw.setdefault('separators', separators)
    return dumps(x, **kw)



json_dumps = dumps
json_loads = loads
json_prettydump = pretty
