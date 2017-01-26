#!/usr/bin/env python
# encoding: utf8
import os
import sys
sys.path.append(os.pardir)

import unittest
import jsonplus as json
import textwrap
import math

from datetime import datetime, timedelta, date, time
from decimal import Decimal
from fractions import Fraction
from collections import namedtuple
import uuid


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

        self.ts = datetime.now()

    def dump_and_load(self, val, **kwargs):
        return json.loads(json.dumps(val, **kwargs))
    
    def test_basic_dumps(self):
        self.assertEqual(json.dumps(self.basic, sort_keys=True), self.basic_dumps)
    
    def test_basic_loads(self):
        self.assertEqual(json.loads(self.basic_dumps), self.basic)

    def test_basic_pretty(self):
        self.assertEqual(json.pretty(self.basic, sort_keys=True), self.basic_pretty)

    def test_basic_loads_dumps(self):
        basic = json.loads(self.basic_dumps)
        self.assertEqual(json.dumps(basic, sort_keys=True), self.basic_dumps)

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
        x = Fraction(math.cos(math.pi/3))
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
        self.assertEqual(self.dump_and_load(x), x)

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

if __name__ == '__main__':
    unittest.main()
