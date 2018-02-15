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
        json.prefer_compat()
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
            '["2017-02-17T02:41:04.390605","2017-02-17","02:41:04.390605",'\
            '864000.0,[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9],'\
            '{"imag":2.0,"real":1.0},3.14,{"denominator":3,"numerator":1},'\
            '[1,2,3],"16ebeeb6-fc5f-4266-a3a9-50c320d87810"]'


    def dump_and_load(self, val, **kwargs):
        return json.loads(json.dumps(val, **kwargs))
    
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

    def test_plus_dumps(self):
        self.assertEqual(json.dumps(self.plus, sort_keys=True), self.plus_dumps)
    
    def test_plus_encode(self):
        # specify separators manually, because JSONEncoder already receives 
        # separators set from simplejson.dumps() to a different default 
        # than we use in jsonplus.dumps()
        self.assertEqual(
            simplejson.dumps(self.plus, sort_keys=True, separators=(',', ':'), cls=json.JSONEncoder),
            json.dumps(self.plus, sort_keys=True))

    
    def test_datetime(self):
        self.assertEqual(self.dump_and_load(self.ts), self.ts.isoformat())

    def test_date(self):
        date = self.ts.date()
        self.assertEqual(self.dump_and_load(date), date.isoformat())
    
    def test_time(self):
        time = self.ts.time()
        self.assertEqual(self.dump_and_load(time), time.isoformat())
    
    def test_timedelta(self):
        dt = timedelta(0, 1234567, 123)
        total_seconds = json._timedelta_total_seconds(dt)
        self.assertEqual(self.dump_and_load(dt), total_seconds)

    def test_set(self):
        s = set(range(10))
        self.assertEqual(self.dump_and_load(s), list(s))

    def test_frozenset(self):
        f = frozenset(range(10))
        self.assertEqual(self.dump_and_load(f), list(f))

    def test_complex(self):
        c = 1 + 2j
        self.assertEqual(self.dump_and_load(c), {"real": c.real, "imag": c.imag})

    def test_decimal_normal(self):
        x = Decimal('1.23')
        self.assertEqual(self.dump_and_load(x), float(x))

    def test_decimal_inf(self):
        x = Decimal('Infinity')
        self.assertTrue(math.isinf(self.dump_and_load(x)))

    def test_decimal_nan(self):
        x = Decimal('Nan')
        self.assertTrue(math.isnan(self.dump_and_load(x)))

    def test_fraction_normal(self):
        x = Fraction.from_float(math.cos(math.pi/3))
        self.assertEqual(self.dump_and_load(x), {'denominator': 9007199254740992, 'numerator': 4503599627370497})

    def test_tuple_explicit(self):
        x = (1, 2, 3)
        self.assertEqual(self.dump_and_load(x), list(x))

    def test_tuple_explicit_empty(self):
        x = tuple()
        self.assertEqual(self.dump_and_load(x), [])

    def test_namedtuple(self):
        Point = namedtuple('Point', 'x y')
        x = Point(3, 4)
        self.assertEqual(self.dump_and_load(x), x._asdict())

    def test_uuid1(self):
        x = uuid.uuid1()
        self.assertEqual(self.dump_and_load(x), str(x))

    def test_uuid4(self):
        x = uuid.uuid4()
        self.assertEqual(self.dump_and_load(x), str(x))

    def test_inf_representation(self):
        a = json.dumps(float("inf"))
        b = 'null'
        self.assertEqual(b, a)

    def test_money(self):
        x = Money(amount='3.14', currency='USD')
        self.assertEqual(self.dump_and_load(x), str(x))

    def test_user_encoder_compat(self):
        @json.encoder('mytype', exact=False)
        def mytype_encoder(obj):
            return obj.y
        class mytype(object):
            y = 313
        self.assertEqual(json.dumps(mytype(), sort_keys=True, exact=False),
                         '313')


if __name__ == '__main__':
    unittest.main()
