#!/usr/bin/env python
# encoding: utf8
import os
import sys
sys.path.append(os.pardir)

import unittest
import jsonplus as json
import textwrap

from datetime import datetime, timedelta, date, time


class TestJSONPlus(unittest.TestCase):
    def setUp(self):
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


if __name__ == '__main__':
    unittest.main()
