#!/usr/bin/env python
# encoding: utf8
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import unittest
import jsonplus as json
import simplejson
import textwrap
import math

from datetime import datetime, timedelta, date, time
from decimal import Decimal
from fractions import Fraction
from collections import namedtuple
import uuid

from moneyed import Money, Currency


class TestJSONPlus(unittest.TestCase):
    def setUp(self):
        json.prefer_exact()
        self.basic = {
            "a": "str",
            "i": 123,
            "f": 1.23,
            "l": [4, 3],
            "ll": [{"x": 1}, 2],
            "d": {
                "a": 1,
                "b": 2
            }
        }
        self.basic_dumps = '{"a":"str","d":{"a":1,"b":2},"f":1.23,"i":123,"l":[4,3],"ll":[{"x":1},2]}'
        self.basic_pretty = textwrap.dedent("""\
            {
                "a": "str",
                "d": {
                    "a": 1,
                    "b": 2
                },
                "f": 1.23,
                "i": 123,
                "l": [
                    4,
                    3
                ],
                "ll": [
                    {
                        "x": 1
                    },
                    2
                ]
            }""")

        self.ts = datetime(2017, 2, 17, 2, 41, 4, 390605)

        self.plus = [
            self.ts, self.ts.date(), self.ts.time(), timedelta(10),
            set(range(10)), frozenset(range(10)), 1+2j, 
            Decimal('3.14'), Fraction(1, 3),
            (1, 2, 3),
            uuid.UUID('16ebeeb6-fc5f-4266-a3a9-50c320d87810')
        ]
        self.plus_dumps = \
            '[{"__class__":"datetime","__value__":"2017-02-17T02:41:04.390605"},'\
            '{"__class__":"date","__value__":"2017-02-17"},'\
            '{"__class__":"time","__value__":"02:41:04.390605"},'\
            '{"__class__":"timedelta","__value__":{"days":10,"microseconds":0,"seconds":0}},'\
            '{"__class__":"set","__value__":[0,1,2,3,4,5,6,7,8,9]},'\
            '{"__class__":"frozenset","__value__":[0,1,2,3,4,5,6,7,8,9]},'\
            '{"__class__":"complex","__value__":{"imag":2.0,"real":1.0}},'\
            '{"__class__":"Decimal","__value__":"3.14"},'\
            '{"__class__":"Fraction","__value__":{"denominator":3,"numerator":1}},'\
            '{"__class__":"tuple","__value__":[1,2,3]},'\
            '{"__class__":"UUID","__value__":{"hex":"16ebeeb6fc5f4266a3a950c320d87810"}}]'


    def dump_and_load(self, val, **kwargs):
        return json.loads(json.json.dumps(val, cls=json.JSONEncoder, **kwargs))

    def encode_and_decode(self, val, **kwargs):
        return json.loads(simplejson.dumps(val, cls=json.JSONEncoder, **kwargs), cls=json.JSONDecoder)


    def test_basic_dumps(self):
        self.assertEqual(json.dumps(self.basic, sort_keys=True), self.basic_dumps)

    def test_basic_encode(self):
        self.assertEqual(
            simplejson.dumps(self.basic, sort_keys=True, cls=json.JSONEncoder),
            simplejson.dumps(self.basic, sort_keys=True))
    
    def test_basic_loads(self):
        self.assertEqual(json.loads(self.basic_dumps), self.basic)

    def test_basic_decode(self):
        self.assertEqual(simplejson.loads(self.basic_dumps, cls=json.JSONDecoder), self.basic)

    def test_basic_pretty(self):
        self.assertEqual(json.pretty(self.basic, sort_keys=True), self.basic_pretty)

    def test_basic_loads_dumps(self):
        basic = json.loads(self.basic_dumps)
        self.assertEqual(json.dumps(basic, sort_keys=True), self.basic_dumps)


    def test_basic_cycle(self):
        self.assertEqual(self.dump_and_load(self.basic), self.basic)
    
    def test_plus_cycle(self):
        self.assertEqual(self.encode_and_decode(self.plus), self.plus)


    def test_plus_dumps(self):
        self.assertEqual(json.dumps(self.plus, sort_keys=True), self.plus_dumps)
    
    def test_plus_encode(self):
        # specify separators manually, because JSONEncoder already receives 
        # separators set from simplejson.dumps() to a different default 
        # than we use in jsonplus.dumps()
        self.assertEqual(
            simplejson.dumps(self.plus, sort_keys=True, separators=(',', ':'), cls=json.JSONEncoder), 
            json.dumps(self.plus, sort_keys=True))
    
    def test_plus_loads(self):
        self.assertEqual(json.loads(self.plus_dumps), self.plus)
    
    def test_plus_decode(self):
        self.assertEqual(simplejson.loads(self.plus_dumps, cls=json.JSONDecoder), self.plus)


    def test_datetime(self):
        self.assertEqual(self.dump_and_load(self.ts), self.ts)

    def test_date(self):
        date = self.ts.date()
        self.assertEqual(self.dump_and_load(date), date)
    
    def test_time(self):
        time = self.ts.time()
        self.assertEqual(self.dump_and_load(time), time)
    
    def test_timedelta(self):
        dt = timedelta(0, 1234567, 123)
        self.assertEqual(self.dump_and_load(dt), dt)

    def test_set(self):
        s = set(range(10))
        self.assertEqual(self.dump_and_load(s), s)

    def test_frozenset(self):
        f = frozenset(range(10))
        self.assertEqual(self.dump_and_load(f), f)

    def test_complex(self):
        c = 1 + 2j
        self.assertEqual(self.dump_and_load(c), c)

    def test_decimal_normal(self):
        x = Decimal('1.23')
        self.assertEqual(x.compare_total(self.dump_and_load(x)), Decimal('0'))

    def test_decimal_inf(self):
        x = Decimal('Infinity')
        self.assertEqual(x.compare_total(self.dump_and_load(x)), Decimal('0'))

    def test_decimal_nan(self):
        x = Decimal('Nan')
        self.assertEqual(x.compare_total(self.dump_and_load(x)), Decimal('0'))

    def test_fraction_normal(self):
        x = Fraction.from_float(math.cos(math.pi/3))
        self.assertEqual(self.dump_and_load(x), x)

    def test_tuple_explicit(self):
        x = (1, 2, 3)
        self.assertEqual(self.dump_and_load(x), x)

    def test_tuple_explicit_empty(self):
        x = tuple()
        self.assertEqual(self.dump_and_load(x), x)

    def test_namedtuple(self):
        Point = namedtuple('Point', 'x y')
        x = Point(3, 4)
        y = self.dump_and_load(x)
        self.assertEqual(x, y)
        self.assertEqual(y.x, 3)
        self.assertEqual(y.y, 4)

    def test_namedtuple_priority(self):
        mytuple = namedtuple('tuple', 'x y')
        x = mytuple(3, 4)
        y = self.dump_and_load(x)
        self.assertEqual(x, y)
        self.assertEqual(y.x, 3)
        self.assertEqual(y.y, 4)

    def test_uuid1(self):
        a = uuid.uuid1()
        b = self.dump_and_load(a)
        self.assertEqual(b, a)
        self.assertEqual(b.version, 1)

    def test_uuid4(self):
        a = uuid.uuid4()
        b = self.dump_and_load(a)
        self.assertEqual(b, a)
        self.assertEqual(b.version, 4)

    def test_inf_representation(self):
        a = json.dumps(float("inf"))
        # TODO: we want this:
        #b = '{"__class__":"float","__value__":"inf"}'
        # unfortunately, with current version of simplejson, all we can get is:
        b = 'Infinity'
        self.assertEqual(b, a)

    def test_inf_reconstruction(self):
        a = float("inf")
        b = self.dump_and_load(a)
        self.assertEqual(b, a)

    def test_money(self):
        from moneyed import USD
        a = Money(amount='3.14', currency='USD')
        b = self.dump_and_load(a)
        self.assertEqual(b, a)
        self.assertEqual(b.currency.code, USD.code)

    def test_currency_std(self):
        from moneyed import get_currency
        a = get_currency('USD')
        b = self.dump_and_load(a)
        self.assertEqual(b.numeric, a.numeric)

    def test_currency_user(self):
        a = Currency(code='AAA', numeric=9999, name='test')
        b = self.dump_and_load(a)
        self.assertEqual(b.code, a.code)
        self.assertEqual(b.numeric, a.numeric)
        self.assertEqual(b.name, a.name)


if __name__ == '__main__':
    unittest.main()
