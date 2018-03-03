#!/usr/bin/env python
# encoding: utf8
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import unittest
import jsonplus
import simplejson as json

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

    def test_encoder_predicates(self):
        class mycls1(object):
            snowflake = 313

        class mycls2(object):
            bulldozer = 131

        @jsonplus.encoder('mycls1', lambda obj: hasattr(obj, 'snowflake'))
        def mycls1_encoder(obj):
            return obj.snowflake

        @jsonplus.encoder('mycls2', lambda obj: hasattr(obj, 'bulldozer'))
        def mycls2_encoder(obj):
            return obj.bulldozer

        a = [mycls2(), mycls1()]
        b = json.loads(jsonplus.dumps(a, exact=True))

        self.assertEqual(b[0]['__value__'], a[0].bulldozer)
        self.assertEqual(b[1]['__value__'], a[1].snowflake)

    def test_encoder_predicate_over_classname(self):
        class mycls(object):
            uniq = 313

        @jsonplus.encoder('mycls')
        def mycls_encoder_1(obj):
            return None

        @jsonplus.encoder('mycls', lambda obj: hasattr(obj, 'uniq'))
        def mycls_encoder_2(obj):
            return obj.uniq

        # classname-based encoder is tested after the predicate-based one
        a = mycls()
        b = json.loads(jsonplus.dumps(a, exact=True))

        self.assertEqual(b['__class__'], type(a).__name__)
        self.assertEqual(b['__value__'], a.uniq)

    def test_encoder_priority(self):
        class mycls(object):
            pass

        @jsonplus.encoder('mycls', lambda obj: isinstance(obj, mycls))
        def _enc1(obj):
            return 'invalid-priority-1000'

        @jsonplus.encoder('mycls', lambda obj: isinstance(obj, mycls), priority=500)
        def _enc2(obj):
            return 'valid'

        r = json.loads(jsonplus.dumps(mycls(), exact=True))

        self.assertEqual(r['__class__'], 'mycls')
        self.assertEqual(r['__value__'], 'valid')


if __name__ == '__main__':
    unittest.main()
