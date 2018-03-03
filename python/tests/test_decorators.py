#!/usr/bin/env python
# encoding: utf8
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import unittest
import jsonplus

class TestDecorators(unittest.TestCase):

    def dump_and_load(self, val, **kwargs):
        return jsonplus.loads(jsonplus.json.dumps(val, cls=jsonplus.JSONEncoder, **kwargs))

    def test_user_encoder_exact(self):
        class mytype1(object):
            x = 313

        @jsonplus.encoder('mytype1', exact=True)
        def mytype_encoder(obj):
            return obj.x

        self.assertEqual(jsonplus.dumps(mytype1(), sort_keys=True, exact=True),
                         '{"__class__":"mytype1","__value__":313}')

    def test_user_encoder_compat(self):
        class mytype1(object):
            x = 313

        @jsonplus.encoder('mytype1', exact=False)
        def mytype_encoder(obj):
            return obj.x

        self.assertEqual(jsonplus.dumps(mytype1(), sort_keys=True, exact=False),
                         '313')

    def test_user_decoder_exact(self):
        class mytype2(object):
            def __init__(self, val):
                self.val = val

        @jsonplus.encoder('mytype2')
        def mytype_encoder(obj):
            return obj.val

        @jsonplus.decoder('mytype2')
        def mytype_decoder(val):
            return mytype2(val)

        a = mytype2(313)
        b = self.dump_and_load(a, exact=True)
        self.assertEqual(a.val, b.val)

    def test_user_decoder_compat(self):
        class mytype2(object):
            def __init__(self, val):
                self.val = val

        @jsonplus.encoder('mytype2', exact=False)
        def mytype_encoder(obj):
            return obj.val

        a = mytype2(313)
        b = self.dump_and_load(a, exact=False)
        self.assertEqual(a.val, b)


if __name__ == '__main__':
    unittest.main()
